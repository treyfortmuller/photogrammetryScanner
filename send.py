import numpy as np
import serial
import time
import os

import cv2

import rospy
import message_filters
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError

from threading import Thread

def deg_to_rad(deg):
    rad = (np.pi / 180) * deg
    return rad


def get_x_coord(r, ang):
    x = r * np.cos(deg_to_rad(ang))
    return x


def get_y_coord(r, ang):
    y = r * np.sin(deg_to_rad(ang))
    return y

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


def update_ros():
	rospy.spin()


currLeft = None
currRight = None

def image_callback(left, left_info, right, right_info):
	# print('IMAGE RECEIVED!!!')
	bridge = CvBridge()
	global currLeft
	global currRight
	try:
		currLeft = bridge.imgmsg_to_cv2(left, "bgr8")
		currRight = bridge.imgmsg_to_cv2(right, "bgr8")

		# out = cv2.cvtColor(currLeft, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("Left Image", currLeft)
		# cv2.imshow("Right Image", currRight)
		# cv2.waitKey(1)
	except CvBridgeError as e:
		print(e)

### calculates new rotation states, changes arduino stepper motor
###
### PARAMATERS:
###				iterations - number of images
###				angle - rotation of camera pose/rotation of turntable
###				translation - change in height of camera
###				wait_time - time delay for arduino process
###				frame_path - frame destination
###				dest_path - path destination
###
### RETURNS -  Rotation matrices for extrinsics
def greg(iterations, angle, translation, wait_time, wait_stepper, image_path, dest_path):


	rospy.init_node('ArduinoTalker', anonymous=True)

	# cv2.startWindowThread()
	# cv2.namedWindow("Left Image", cv2.WINDOW_NORMAL)
	# cv2.namedWindow("Right Image", cv2.WINDOW_NORMAL)

	##ROS##
	left_cam = message_filters.Subscriber('/zed/left/image_raw_color', Image)
	left_info = message_filters.Subscriber('/zed/left/camera_info', CameraInfo)
	right_cam = message_filters.Subscriber('/zed/right/image_raw_color', Image)
	right_info = message_filters.Subscriber('/zed/right/camera_info', CameraInfo)

	ts = message_filters.ApproximateTimeSynchronizer([left_cam, left_info, right_cam, right_info], 10, 0.1)
	ts.registerCallback(image_callback)

	update = Thread(target = update_ros)
	update.start()

	## SERIAL ##

	ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial communication at 9600 baud to the arduino
	print("initializing...")
	time.sleep(5)  # wait for initialization of the serial communication to Arduino

	def arduino_message(rotation, translation, wait_time):
		###Turntable change
		ser.write(str(-rotation) + "\n")
		time.sleep(wait_time)

		###Camera height change
		ser.write(str(translation) + "\n")
		time.sleep(wait_time)
		### Add arduino call back message for debugging


	# ### List of rotation matrices for pose and orientation
	# rotations = []

	# ### matrix of height axis transformation
	# height = np.array([[0, 0, 0],
	# 				   [0, 0, 0],
	# 				   [0, 0, 1]])

	print("ROS & SERIAL UP: Beginning Iterations ")
	for i in range(iterations):

		print('---- ITERATION %d ----' % i)

		###message sent to arduino stepper motor; rotates turntable and adjust camera height
		###send negative of angle because of turntable design

		#capture current image
		if currRight is None or currLeft is None:
			print("--> Some pictures missing - skipping save on iteration %d" % i)
		else:
			cv2.imwrite(os.path.join(image_path, "imm%d_left.jpg" % i), currLeft)
			cv2.imwrite(os.path.join(image_path, "imm%d_right.jpg" % i), currRight)
		
		arduino_message(angle, translation, wait_time)

		time.sleep(wait_stepper)


		# ###Get rotation matrix in XY plane, and then add height translation
		# new_state = rot_matrix(deg_to_rad(theta), "Rz") + i*translation*height 

		# ###Appending each rotation matrix for extrinsics

		# rotations.append(new_state)



		####################
		###ROS CODE HERE###
		####################
		



		###CV code taken from trey's Faraday Future's python script
		# camera = cv2.VideoCapture(0)
		# s1, im1 = camera.read()
		# image_number = "im" + str(i) + ".jpg"
		# cv2.imwrite(image_number, im1)
		# camera.release()


		#####################
		#####################

	#we travel iterations * translation up, and iterations * angle % 360 in angle
	#move back!!
	if i >= iterations - 1:
		print("===== MOVING DOWN =====")
		arduino_message(-(angle * iterations) % 360, - translation * iterations + H_OFFSET, wait_time)

		time.sleep(5)

	#release the stepper motors
	ser.write("release\n")
	time.sleep(wait_time)
	print('Done')

	rospy.signal_shutdown("End")
	update.join()
	# return rotations




###Rotation parameters
theta = 18
del_height = 5 ##5mm ###for changing scaling, adjust code in arduino stepper file
img_num = 20
### 


# CONSTANTS
move_wait = 0.03
# seconds to wait for the stepper to turn
stepper_wait = 1

H_OFFSET = 2 #mm from base to prevent crashing
# frame_wait = 2  # seconds to wait for the webcam to capture a frame
# iterations = 32

###File input/output destination
image_path = '/home/greg/images/'
dest_path = '/home/greg/images/out/'



if __name__ == '__main__':
	greg(img_num, theta, del_height, move_wait, stepper_wait, image_path, dest_path)
