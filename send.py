import numpy as np
import serial
import time
import os

import cv2




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
		return Rx
	elif axis == "Ry":
		#Rotation about z axis; xy plane unit circle
		Rz = np.matrix([[np.cos(theta), -np.sin(theta), 0], 
               			[np.sin(theta), np.cos(theta), 0],
               			[0, 0, 1]])
		return Rx







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
def greg(iterations, angle, translation, wait_time, frame_path, dest_path):

	ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial communication at 9600 baud to the arduino
	print("initializing...")
	time.sleep(7)  # wait for initialization of the serial communication to Arduino



	def arduino_message(rotation, translation, wait_time):
		### Turntable change
		ser.write(rotation)
		time.sleep(wait_time)

		### Camera height change
		ser.write(translation)
		time.sleep(wait_time)
		### Add arduino call back message for debugging



	### List of rotation matrices for pose and orientation
	rotations = []

	### matrix of height axis transformation
	height = np.array([[0, 0, 0],
					   [0, 0, 0],
					   [0, 0, 1]])


	for i in range(iterations):

		###message sent to arduino stepper motor; rotates turntable and adjust camera height
		###send negative of angle because of turntable design
		arduino_message(-angle, translation, wait_time)



		###Get rotation matrix in XY plane, and then add height translation
		new_state = rot_matrix(deg_to_rad(theta), "Rz") + i*translation*height 

		###Appending each rotation matrix for extrinsics
		rotations.append(new_state)



		####################
		###ROSS CODE HERE###
		####################


		###CV code taken from trey's Faraday Future's python script
		camera = cv2.VideoCapture(0)
		s1, im1 = camera.read()
		image_number = "im" + str(i) + ".jpg"
		cv2.imwrite(image_number, im1)
		camera.release()
		os.rename(frame_path + image_number, dest_path + image_number)


		#####################
		#####################



	return rotations




###Rotation parameters
theta = 30
del_height = 5 ##5mm ###for changing scaling, adjust code in arduino stepper file
img_num = 32


# CONSTANTS
move_wait = 2  # seconds to wait for the stepper to turn
frame_wait = 2  # seconds to wait for the webcam to capture a frame
iterations = 32

###File input/output destination
frame_path = '/home/trey.fortmuller/Desktop/sfm/sfm_test/'
dest_path = '/home/trey.fortmuller/Desktop/sfm/sfm_test/sfm_in/'





def main():
	greg(img_num, theta, del_height, wait_time, frame_path, dest_path)



main()
