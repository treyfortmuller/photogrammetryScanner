# given an image dataset create a sfm_data.json file to run the algo on
# Trey Fortmuller

import os
import subprocess

# OPENMVG CONSTANTS
# indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/trey.fortmuller/openMVG_Build/Linux-x86_64-RELEASE"

# indicate the the camera sensor width database directory,
# must be included as a required param of the ImageListing, not used by our algo with defined intrinsics
CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/trey.fortmuller/openMVG/src/openMVG/exif/sensor_width_database"

# PROJECT CONSTANTS
# indicate the project directory, the directory where the python scripts reside
PROJECT_DIR = input_eval_dir = os.path.dirname(os.path.abspath(__file__))

# define a directory to indicate the name's of our directories in our file structure relative to project directory
file_struct = {"input": "/sfm_in",
               "output": "/sfm_out",
               "matches": "/sfm_out/sfm_matches",
               "reconstruction": "/sfm_out/sfm_reconstruction"}

# define all the relevant directories
input_dir = PROJECT_DIR + file_struct["input"]
output_dir = PROJECT_DIR + file_struct["output"]
matches_dir = PROJECT_DIR + file_struct["matches"]
reconstruction_dir = PROJECT_DIR + file_struct["reconstruction"]
camera_file_params = CAMERA_SENSOR_WIDTH_DIRECTORY + "/sensor_width_camera_database.txt"

# first we create an sfm_data.json file establishing our views and spit it out to sfm_matches,
# utilizing "-k", "350;0;240;0;350;360;0;0;1"
# if we know exactly how long the pivot takes then we can eliminate this and always use the same sfm_data.json file
print("INIT IMAGE LISTING")  # http://openmvg.readthedocs.io/en/latest/software/SfM/SfMInit_ImageListing/
pIntrisics = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),
                               "-i", input_dir,
                               "-o", matches_dir,
                               "-d", camera_file_params,
                               # intrinsics camera calib goes here in the form of a K matrix deconstructed row-wise
                               # focal, 0, pp_x, 0, focal, pp_y, 0, 0, 1
                               # 18mm focal length with a 4.68 micron pixel to get focal length in pixels
                               "-k", "3846.154; 0; 2542; 0; 250; 3846.154; 0; 0; 1"])
pIntrisics.wait()

