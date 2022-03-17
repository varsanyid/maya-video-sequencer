# Maya Video Sequencer

A thin layer on top of ffmpeg to easily turn videos into image sequences

## How to use

* Type `VideoSequencer` into the MEL script editor tab
* Select the input video, the output directory for the generated image frames and the camera you want to add a new plane to

The plug-in will use your current fps settings to generate the appropriate image sequence. Currently limited to jpeg

## Install

Install script WIP

### Current manual steps
 * Install ffmpeg
 * Add ffmpeg bin to $PATH
 * Run mayapy.exe -m pip install ffmpeg-python
 * Run getenv MAYA_PLUG_IN_PATH in script editor to get your directory for maya plugins
 * Copy video_sequencer.py to the plugin directory
 * Load plugin via the Maya Plug-in Manager