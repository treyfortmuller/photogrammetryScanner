# Run the monocular structure from motion demo with the arduino/webcam test rig
# Trey Fortmuller

import os

# define file paths to the scripts we need to call in order
script1 = os.path.join(os.getcwd(), "1_create_dataset.py")
script2 = os.path.join(os.getcwd(), "2_create_image_listing.py")
script3 = os.path.join(os.getcwd(), "3_test_rig_extrinsics.py")
script4 = os.path.join(os.getcwd(), "4_run_algo.py")
script5 = os.path.join(os.getcwd(), "5_point_cloud_to_open.py")

# note os.system waits for the called script to finish before continuing
# capture new dataset, must have the arduino ready to communicate over serial on proper port and the webcam available
# comment out the following line in order to use the existing dataset to run the algo rather than use a test rig
# os.system('{} {}'.format('python', script1))

# create a sfm_data.json file containing the views and camera intrinsics
os.system('{} {}'.format('python', script2))

# calculate the extrinsics for each frame then augment the sfm_data.json by adding the extrinsics for each frame
os.system('{} {}'.format('python', script3))

# run the sfm algorithm on the sfm_data.json file and save the 3D reconstruction in a point_cloud.json file
os.system('{} {}'.format('python', script4))

# parse the point cloud and calculate a door open angle then visualize the door system and points with matplotlib
os.system('{} {}'.format('python', script5))
