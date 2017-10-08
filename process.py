# Given a sfm_data.json, run the SfM algo to get features, matches, and create a reconstruction with a json file
# Trey Fortmuller

import os
import subprocess

# OPENMVG CONSTANTS
# indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/greg/openMVG_Build/Linux-x86_64-RELEASE"
OPENMVS_SFM_BIN = "/home/greg/openMVS_build/bin"
# indicate the the camera sensor width database directory,
# must be included as a required param of the ImageListing, not used by our algo with defined intrinsics
CAMERA_SENSOR_WIDTH_DIRECTORY = '/home/greg/openMVG/src/openMVG/exif/sensor_width_database'


# PROJECT CONSTANTS
# indicate the project directory, the directory where the python scripts reside
PROJECT_DIR = input_eval_dir = os.path.dirname(os.path.abspath(__file__))

# define a directory to indicate the name's of our directories in our file structure relative to project directory
file_struct = {"input": "/input",
               "output": "/output",
               "matches": "/output/matches",
               "reconstruction": "/output/reconstruction"}

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
                              "-p", "NORMAL"])  # NORMAL, HIGH, ULTRA (high recommended for global pipeline)
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


print("EXPORT CAM FRUSTUMS")
# https://github.com/openMVG/openMVG/blob/master/src/software/SfM/main_ExportCameraFrustums.cpp
pExport = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ExportCameraFrustums"),
                            "-i", matches_dir + "/sfm_data.json",
                            "-o", reconstruction_dir + "/frustums.ply"])
pExport.wait()


print("STORE POINT CLOUD DATA AS JSON")
pChange = subprocess.Popen([os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ConvertSfM_DataFormat"),
                            "-i", os.path.join(reconstruction_dir, "reconstruction.bin"),
                            "-o", reconstruction_dir + "/point_cloud.json"])
pChange.wait()





#######################
###### OPEN MVS ######
#######################



# print("CONVERT MVG TO MVS")
# pConvert = subprocess.Popen([os.path.join(OPENMVG_BIN,"openMVG_main_openMVG2openMVS"),
#                              "-i", "sfm_data.bin", 
#                              "-o", "scene.mvs"])
# pConvert.wait()


# print("DENSIFY POINT CLOUD")
# pDensify = subprocess.Popen([os.path.join(OPENMVS_BIN,"DensifyPointCloud"),
#                              "scene.mvs"])
# pDensify.wait()


# print("RECONSTRUCTION OF MESH")
# pReconMesh = subprocess.Popen([os.path.join(OPENMVS_BIN,"ReconstructMesh"),
#                                "scene_dense.mvs"])
# pReconMesh.wait()


# print("MESH REFINEMENT")
# pMeshRefine = subprocess.Popen([os.path.join(OPENMVS_BIN,"RefineMesh"),
#                                 "scene_mesh.mvs"])
# pMeshRefine.wait()


# print("TEXTURE THE MESH")
# pTextureMesh = subprocess.Popen([os.path.join(OPENMVS_BIN,"TextureMesh"),
#                                  "scene_dense_mesh.mvs"])
# pTextureMesh.wait()
