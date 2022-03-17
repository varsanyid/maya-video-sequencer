import maya.api.OpenMaya as om
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import ffmpeg

def maya_useNewApi():
    """
        Tell Maya this plugin uses the Python API 2.0.
    """
    pass


def initializePlugin(plugin):
    vendor = "Daniel Varsanyi"
    version = "0.1.0"
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerCommand(VideoSequencerCmd.COMMAND_NAME, 	VideoSequencerCmd.creator)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format(VideoSequencerCmd))


def uninitializePlugin(plugin):
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(VideoSequencerCmd.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to deregister command: {0}".format(VideoSequencerCmd))


class VideoSequencerCmd(OpenMayaMPx.MPxCommand):

    COMMAND_NAME = "VideoSequencer"

    def __init__(self, input_video = None, output_dir = None, camera = None):
        super(VideoSequencerCmd, self).__init__()
        self.input_video = input_video
        self.output_dir = output_dir
        self.camera = camera
        self.fps_map = {
            "game": 15,
            "film": 24,
            "pal": 25,
            "ntsc": 30,
            "show": 48,
            "palf": 50, 
            "ntscf": 60
        }

    def select_input_video(self,*args):
        self.input_video = cmds.fileDialog2(fileMode=1,fileFilter="All Files (*.*)", dialogStyle=1, caption="Select Video Input")
        cmds.textFieldGrp('Input Video', text = self.input_video[0], editable = False)

    def select_output_dir(self,*args):
        self.output_dir = cmds.fileDialog2(fileMode=3,fileFilter="All Files (*.*)", dialogStyle=1, caption="Select Output Directory")
        cmds.textFieldGrp('Output Dir', text = self.output_dir[0],  editable = False)

    def select_camera(self, *args):
        print(args)
        self.camera = args[0]

    def render_image_sequence(self,*args):
        try:
            input = self.input_video[0]
            output = self.output_dir[0] + '/frame_%d.jpg'
            fps = self.fps_map[cmds.currentUnit(query=True, time=True)]
            ffmpeg.input(input).filter('fps', fps=fps).output(output, start_number=0).run(capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as e:
            print('stdout:', e.stdout.decode('utf8'))
            print('stderr:', e.stderr.decode('utf8'))
            return
        file = str(self.output_dir[0] + '/frame_' + str(int(cmds.currentTime( query=True ))) + '.jpg')
        cmds.imagePlane(camera = self.camera, fileName = file)
        plane_name = cmds.imagePlane(query = True, name = True)[0]
        cmds.expression(o=plane_name, s='{}.fe = frame;'.format(plane_name))


    def doIt(self, args):
        window = cmds.window(title="Video Sequencer", widthHeight=(300, 400))
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label='Video', command=self.select_input_video)
        cmds.button(label='Output Directory', command=self.select_output_dir)
        cmds.optionMenu(label = 'Cameras', changeCommand = self.select_camera)
        for camera in cmds.listCameras(p = True):
            cmds.menuItem(label=camera)
        cmds.button(label='Render Sequence', command=self.render_image_sequence)
        cmds.setParent('..')
        cmds.showWindow(window)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(VideoSequencerCmd())
