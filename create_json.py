import numpy as np
import json
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
               "reconstruction": "/sfm_out/reconstruction"}

# define all the relevant directories
input_dir = PROJECT_DIR + file_struct["input"]
output_dir = PROJECT_DIR + file_struct["output"]
matches_dir = PROJECT_DIR + file_struct["matches"]
reconstruction_dir = PROJECT_DIR + file_struct["reconstruction"]
camera_file_params = CAMERA_SENSOR_WIDTH_DIRECTORY + "/sensor_width_camera_database.txt"


def deg_to_rad(deg):
    rad = (np.pi / 180) * deg
    return rad


def rot_matrix(theta, axis):
	if axis == "Rx":
		#Rotation about x axis; yz plane yz plane unit circle
		Rx = np.matrix([[1, 0, 0], 
						[0, np.cos(theta), -np.sin(theta)], 
               			[0, np.sin(theta), np.cos(theta)]])
		return Rx
	elif axis == "Ry":
		#Rotation about y axis; xz plane xz plane unit circle
		Ry = np.matrix([[np.cos(theta), 0, np.sin(theta)], 
               			[0, 1, 0], 
               			[-np.sin(theta), 0, np.cos(theta)]])
		return Ry
	elif axis == "Rz":
		#Rotation about z axis; xy plane unit circle
		Rz = np.matrix([[np.cos(theta), -np.sin(theta), 0], 
               			[np.sin(theta), np.cos(theta), 0],
               			[0, 0, 1]])
		return Rz

def package_data(center, rotation, num_frames):
    # package the extrinsics information in the proper json form that openMVG takes for extrinsics data in sfm_data.json
    extrinsics_data = []
    for i in np.arange(num_frames):

        # the json module only likes lists not numpy arrays so we change them
        ith_rot_mtx = rotation[i].tolist()  # change the ith rotation matrix from a np array to a python list
        ith_center = [center[i].tolist()[0][0], center[i].tolist()[1][0], center[i].tolist()[2][0]]  # change the ith center coords from a np array to a python list

        # this is the weird form factor the data should take for openMVG
        extrinsics_data.append({"key": i, "value": {"rotation": ith_rot_mtx, "center": ith_center}})

    return extrinsics_data

### absolute file path to sfm_data.json file
json_file_path = '/home/greg/greg/output/matches/sfm_data.json'


### Iteration 0 vectors
# R = np.array([[306], [60], [35.0428]]) ### Original vector corresponding to the right camera
# L = np.array([[306], [-60], [35.0428]]) ### Original vector corresponding to the right camera


###Rotation parameters
theta = 30
del_height = 15 ##5mm ###for changing scaling, adjust code in arduino stepper file
img_num = 20
### 

RADIUS = 306

### List of rotation matrices for pose and orientation
rotations = []
### List of transformed coordinates
all_coordinates = []

### matrix of height axis transformation
height = np.array([[0, 0, 0],
				   [0, 0, 0],
				   [0, 0, 0]])


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
                               "-k", "699.34; 0; 661.28; 0; 699.34; 333.51; 0; 0; 1"])

pIntrisics.wait()

for i in range(img_num):
	# height[2][2] += del_height
	# new_state = rot_matrix(deg_to_rad(theta), "Rz")

  c_x = RADIUS * np.cos(i * theta)
  c_y = - RADIUS * np.sin(i * theta)

  l_x = c_x - 60 * np.sin(i * theta)
  l_y = c_y - 60 * np.cos(i * theta)
  r_x = c_x + 60 * np.sin(i * theta)
  r_y = c_y + 60 * np.cos(i * theta)

  L = np.array([[l_x], [l_y], [i * del_height]])
  R = np.array([[r_x], [r_y], [i * del_height]])

  rotations.append(rot_matrix(deg_to_rad(theta), "Rz"))
  rotations.append(rot_matrix(deg_to_rad(theta), "Rz"))


  # R = np.matmul(new_state, R)
  # L = np.matmul(new_state, L)
  all_coordinates.append(L)
  all_coordinates.append(R)





print(all_coordinates)

# write the data to the json file
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)
    json_data['extrinsics'] = package_data(all_coordinates, rotations, 2*img_num)

with open(json_file_path, 'w') as json_file:
    json_file.write(json.dumps(json_data, indent=4))





