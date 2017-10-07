# given the parameters of the test rig, return the cartesian coordinates and rotation matrices of each frame
# with respect to a world coordinate axis centered at the pivot of the test rig. lengths in cm, angles in deg.
# then write this data to the sfm_data.json file to pass to the main algo.
# Trey Fortmuller

import numpy as np
import json

# CONSTANTS
num_frames = 13
deg_swing = 60  # deg
len_arm = 30  # centimeters

# set numpy data print options
np.set_printoptions(precision=5)
np.set_printoptions(suppress=True)

# VARIABLES
start_ang = 90 - (deg_swing / 2)  # the angle w.r.t. the x-axis of the test rig of the first frame
step_ang = deg_swing / (num_frames - 1)  # the deg of rotation (about the z-axis) between frames
coords = np.array([])
rot_mtxs = np.array([])


def deg_to_rad(deg):
    rad = (np.pi / 180) * deg
    return rad


def get_x_coord(r, ang):
    x = r * np.cos(deg_to_rad(ang))
    return x


def get_y_coord(r, ang):
    y = r * np.sin(deg_to_rad(ang))
    return y


def add_to_list_of_lists(np_array, value):
    # first append then continue by vstacking
    if len(np_array) == 0:
        np_array = np.append(np_array, [value])
    else:
        np_array = np.vstack((np_array, value))
    return np_array


def display_frame_info(coordinates, rotation_matrices):
    for i in np.arange(num_frames):
        # frame number header
        print("----- FRAME: " + str(i) + " -----")

        ith_rot_mtx = rotation_matrices[i]  # the ith frame's rotation matrix
        ith_frame_coords = coordinates[i]  # the ith frame's center coordinates

        print("ROT_MTX: ")  # row then column index selection
        # ith rotation matrix row 0
        print("[\n" + str(ith_rot_mtx[0][0]) + ",\n" + str(ith_rot_mtx[0][1]) + ",\n" + str(ith_rot_mtx[0][2]) + "\n],")
        # ith rotation matrix row 1
        print("[\n" + str(ith_rot_mtx[1][0]) + ",\n" + str(ith_rot_mtx[1][1]) + ",\n" + str(ith_rot_mtx[1][2]) + "\n],")
        # ith rotation matrix row 2
        print("[\n" + str(ith_rot_mtx[2][0]) + ",\n" + str(ith_rot_mtx[2][1]) + ",\n" + str(ith_rot_mtx[2][2]) + "\n]")

        print("\n")

        print("COORDS: ")
        print("[\n" + str(ith_frame_coords[0]) + ",\n" + str(ith_frame_coords[1]) + ",\n" + str(ith_frame_coords[2]) + "\n]")

        print("\n")


def package_data(center, rotation):
    # package the extrinsics information in the proper json form that openMVG takes for extrinsics data in sfm_data.json
    extrinsics_data = []
    for i in np.arange(num_frames):

        # the json module only likes lists not numpy arrays so we change them
        ith_rot_mtx = rotation[i].tolist()  # change the ith rotation matrix from a np array to a python list
        ith_center = center[i].tolist()  # change the ith center coords from a np array to a python list

        # this is the weird form factor the data should take for openMVG
        extrinsics_data.append({"key": i, "value": {"rotation": ith_rot_mtx, "center": ith_center}})

    return extrinsics_data


# build the coordinates list
for j in np.arange(num_frames):
    current_angle = (j * step_ang) + start_ang
    x_coord = get_x_coord(len_arm, current_angle)
    y_coord = get_y_coord(len_arm, current_angle)

    # x, y, z
    coord = [x_coord, y_coord, 0]

    # add the coordinates of this frame to the list of coordinates for all the frames
    coords = add_to_list_of_lists(coords, coord)

# build the rotation matrix list
for k in np.arange(num_frames):
    current_angle = (k * step_ang) + start_ang
    sin_ang = np.sin(deg_to_rad(current_angle))
    cos_ang = np.cos(deg_to_rad(current_angle))

    # ----- VERSION A -----
    # # arbitrary rotation matrix about the z-axis
    # # z = [[cos  -sin  0]
    # #      [sin   cos  0]
    # #      [0     0    1]]
    # rot_y_mtx = [[cos_ang, 0, sin_ang],
    #              [0, 1, 0],
    #              [-sin_ang, 0, cos_ang]]
    #
    # # rotation 90 degrees about the x-axis
    # rot_x_mtx = [[1, 0, 0],
    #              [0, 0, -1],
    #              [0, 1, 0]]
    #
    # # rotation 90 degrees about the z-axis
    # rot_z_mtx = [[0, -1, 0],
    #              [1, 0, 0],
    #              [0, 0, 1]]
    # # matrix multiplication of the two constituent rotation matrices
    # rot_temp_mtx = np.dot(rot_y_mtx, rot_x_mtx)
    # rot_mtx = [np.dot(rot_temp_mtx, rot_z_mtx)]

    # ----- VERSION B -----
    # arbitrary rotation matrix about the z-axis
    # z = [[cos  -sin  0]
    #      [sin   cos  0]
    #      [0     0    1]]
    rot_z_mtx = [[cos_ang, -sin_ang, 0],
                [sin_ang, cos_ang, 0],
                [0, 0, 1]]
    # rotation 90 degrees about the x-axis
    rot_x_mtx = [[1, 0, 0],
                 [0, 0, -1],
                 [0, 1, 0]]
    # rotation 90 degrees about the y-axis
    rot_y_mtx = [[0, 0, 1],
                 [0, 1, 0],
                 [-1, 0, 0]]
    # matrix multiplication of the two constituent rotation matrices
    rot_temp_mtx = np.dot(rot_z_mtx, rot_x_mtx)
    rot_mtx = [np.dot(rot_temp_mtx, rot_y_mtx)]

    # add the rotation matrix of this frame to the list of rotation matrices for all the frames
    if len(rot_mtxs) == 0:
        rot_mtxs = rot_mtx
    else:
        rot_mtxs = np.vstack((rot_mtxs, rot_mtx))

# display the frame information for these test rig parameters in the terminal for viewing
display_frame_info(coords, rot_mtxs)

# write the data to the json file
with open('/home/trey.fortmuller/Desktop/sfm/sfm_test/sfm_out/sfm_matches/sfm_data.json', 'r') as json_file:
    json_data = json.load(json_file)
    json_data['extrinsics'] = package_data(coords, rot_mtxs)

with open('/home/trey.fortmuller/Desktop/sfm/sfm_test/sfm_out/sfm_matches/sfm_data.json', 'w') as json_file:
    json_file.write(json.dumps(json_data, indent=4))

