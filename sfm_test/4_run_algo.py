# Given a sfm_data.json, run the SfM algo to get features, matches, and create a reconstruction with a json file
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

# check computeFeatures flags, looks like we're detecting matches in two separate ways, also called descriptions
# in the OpenMVG docs
print("FIND FEATURES")  # http://openmvg.readthedocs.io/en/latest/software/SfM/ComputeFeatures/
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
                             # nearest neighbor distance ratio
                             # (0.8 recommended for global pipeline, less is more restrictive)
                             "-r", "0.8",
                             "-g", "e",
                             "-f", "1"])
pMatches.wait()

print("STRUCTURE FROM KNOWN POSES")
pRecons = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),

                            # switch between using the bin constructed from the global pipeline or our own poses in json
                            # "-i", reconstruction_dir + "/sfm_data.bin",
                            "-i", matches_dir + "/sfm_data.json",
                            "-m", matches_dir,
                            "-f", matches_dir + "/matches.e.bin",
                            "-o", os.path.join(reconstruction_dir, "reconstruction.bin"),
                            # "-b",  # perform a bundle adjustment on this data
                            "-r", "4.0",  # maximum pixel reprojection error to use for triangulation (4.0 default)
                            "-d"
                            ])
pRecons.wait()

print("STORE POINT CLOUD DATA AS JSON")
pChange = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ConvertSfM_DataFormat"),
                            "-i", os.path.join(reconstruction_dir, "reconstruction.bin"),
                            "-o", reconstruction_dir + "/point_cloud.json"])
pChange.wait()
