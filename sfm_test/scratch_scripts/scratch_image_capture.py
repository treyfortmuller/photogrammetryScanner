import cv2
import os
import time
import numpy as np

cam = cv2.VideoCapture(0)  # connect the video0 camera device

s, im1 = cam.read()  # captures image
cv2.imwrite("im1.jpg", im1)

os.rename('/home/trey.fortmuller/Desktop/sfm/SfM_test/im1.jpg', '/home/trey.fortmuller/Desktop/check123/im1.jpg')

for i in np.arange(5):
    print(i)
    time.sleep(1)
