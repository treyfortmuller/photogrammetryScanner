import numpy as np
import json



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


### Iteration 0 vectors
R = np.array([[306], [60], [35.0428]]) ### Original vector corresponding to the right camera
L = np.array([[306], [-60], [35.0428]]) ### Original vector corresponding to the right camera


###Rotation parameters
theta = 30
del_height = 5 ##5mm ###for changing scaling, adjust code in arduino stepper file
img_num = 5
### 


### List of rotation matrices for pose and orientation
rotations = []
### List of transformed coordinates
coordinates = []

### matrix of height axis transformation
height = np.array([[0, 0, 0],
				   [0, 0, 0],
				   [0, 0, 1]])

for i in range(img_num):

	new_state = rot_matrix(deg_to_rad(theta*i), "Rz") + i*del_height*height


	rotations.append(new_state)

	R = np.matmul(new_state, R)
	L = np.matmul(new_state, L)
	coordinates.append([R, L])

print("rotations")
print(rotations)
print("coordinates")
print(coordinates)







