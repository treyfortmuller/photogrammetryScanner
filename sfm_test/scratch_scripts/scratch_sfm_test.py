# Structure from Motion for power door max open angle set point
# Trey Fortmuller

import os
import subprocess

# OPENMVG CONSTANTS
# indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/trey.fortmuller/openMVG_Build/Linux-x86_64-RELEASE"

# indicate the the camera sensor width database directory,
# still don't know why I need this, what does the pipeline pull from this file
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


# ------------------------------ START MAIN ALGO ------------------------------

# first we create an sfm_data.json file establishing our views, utilizing "-k", "350;0;240;0;350;360;0;0;1" didn't
# work so we use only an enforced focal length to start, we can go back and edit the json progammatically to fix
# the intrinsics and radial distortion coefficients after this step

# if we know exactly how long the pivot takes then we can eliminate this and always use the same sfm_data.json file
print("INIT IMAGE LISTING")  # http://openmvg.readthedocs.io/en/latest/software/SfM/SfMInit_ImageListing/
pIntrisics = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),
                               "-i", input_dir,
                               "-o", matches_dir,
                               "-d", camera_file_params,
                               "-k", "650;0;240;0;650;360;0;0;1"])  # this doesn't seem to be taking effect
pIntrisics.wait()

# fix the created json file so that all the parameters we want to enforce take effect.

# check computeFeatures flags, looks like we're detecting matches in two separate ways, also called descriptions
# in the OpenMVG docs
print("COMPUTE SIFT FEATURES")  # http://openmvg.readthedocs.io/en/latest/software/SfM/ComputeFeatures/
pFeatures = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),
                              "-i", matches_dir + "/sfm_data.json",
                              "-o", matches_dir,
                              "-m", "SIFT",
                              "-f", "1",
                              "-p", "ULTRA"])  # NORMAL, HIGH, ULTRA (high recommended for global pipeline)
pFeatures.wait()

# find matches between the SIFT features across frames, using essential matrix geometric filtering
# - global SfM pipeline use matches filtered by the essential matrices
# - here we reuse photometric matches and perform only the essential matrix filtering
print("COMPUTE MATCHES")  # http://openmvg.readthedocs.io/en/latest/software/SfM/ComputeMatches/
pMatches = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),
                             "-i", matches_dir + "/sfm_data.json",
                             "-o", matches_dir,
                             "-r", "0.8",  # nearest neighbor distance ratio (0.8 recommended for global pipeline)
                             "-g", "e",
                             "-f", "1"])
pMatches.wait()

# now we send the sfm_data.json and the matches between features of frames found above
# this creates a bin file that structure from known poses uses (I think the bin includes estimated camera pose).
# using the global pipeline may be unnecessary if our sfm_data.json has pose information as well.
print("GLOBAL RECONSTRUCTION")
pRecons = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),
                            "-i", matches_dir + "/sfm_data.json",
                            "-m", matches_dir,
                            "-o", reconstruction_dir,
                            "-f", "NONE"])  # intrinsic parameter refinement, consider them all constants
pRecons.wait()


print("STRUCTURE FROM KNOWN POSES")
pRecons = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),

                            # switch between using the bin constructed from the global pipeline or our own poses in json
                            # "-i", reconstruction_dir + "/sfm_data.bin",
                            "-i", matches_dir + "/sfm_data.json",

                            "-m", matches_dir,
                            "-o", os.path.join(reconstruction_dir, "robust.ply"),
                            "-b", "ON",  # perform a bundle adjustment on this data
                            "-r", "4.0"])  # maximum pixel reprojection error to use for triangulation (4.0 default)
pRecons.wait()

print("STORE POINT CLOUD DATA AS JSON")
pChange = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ConvertSfM_DataFormat"),
                            "-i", os.path.join(reconstruction_dir, "robust.ply"),
                            "-o", reconstruction_dir + "/point_cloud.json"])
pChange.wait()
