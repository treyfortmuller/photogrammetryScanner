# 5 frame test rig for SfM from webcam on rule on hobby servo
# Trey Fortmuller

# CLEAN UP THIS SCRIPT WITH STRING STREAMS

import serial
import time
import cv2
import os

# CONSTANTS
move_wait = 2  # seconds to wait for the servo to turn
frame_wait = 2  # seconds to wait for the webcam to capture a frame

# degree dictionary, the angle of the camera rig at each frame
deg_dict = {1: '60\n',
            2: '65\n',
            3: '70\n',
            4: '75\n',
            5: '80\n',
            6: '85\n',
            7: '90\n',
            8: '95\n',
            9: '100\n',
            10: '105\n',
            11: '110\n',
            12: '115\n',
            13: '120\n'}

frame_path = '/home/trey.fortmuller/Desktop/sfm/sfm_test/'
dest_path = '/home/trey.fortmuller/Desktop/sfm/sfm_test/sfm_in/'

ser = serial.Serial('/dev/ttyACM0', 9600)  # open serial communication at 9600 baud to the arduino
print("initializing...")
time.sleep(7)  # wait for initialization of the serial communication to Arduino

print("FRAME 1")
ser.write(deg_dict[1])
time.sleep(move_wait)
cam1 = cv2.VideoCapture(0)
s1, im1 = cam1.read()
cv2.imwrite("im1.jpg", im1)
cam1.release()
os.rename(frame_path + 'im1.jpg', dest_path + 'im1.jpg')

print("FRAME 2")
ser.write(deg_dict[2])
time.sleep(move_wait)
cam2 = cv2.VideoCapture(0)
s2, im2 = cam2.read()
cv2.imwrite("im2.jpg", im2)
cam2.release()
os.rename(frame_path + 'im2.jpg', dest_path + 'im2.jpg')

print("FRAME 3")
ser.write(deg_dict[3])
time.sleep(move_wait)
cam3 = cv2.VideoCapture(0)
s3, im3 = cam3.read()
cv2.imwrite("im3.jpg", im3)
cam3.release()
os.rename(frame_path + 'im3.jpg', dest_path + 'im3.jpg')

print("FRAME 4")
ser.write(deg_dict[4])
time.sleep(move_wait)
cam4 = cv2.VideoCapture(0)
s4, im4 = cam4.read()
cv2.imwrite("im4.jpg", im4)
cam4.release()
os.rename(frame_path + 'im4.jpg', dest_path + 'im4.jpg')

print("FRAME 5")
ser.write(deg_dict[5])
time.sleep(move_wait)
cam5 = cv2.VideoCapture(0)
s5, im5 = cam5.read()
cv2.imwrite("im5.jpg", im5)
cam5.release()
os.rename(frame_path + 'im5.jpg', dest_path + 'im5.jpg')

print("FRAME 6")
ser.write(deg_dict[6])
time.sleep(move_wait)
cam6 = cv2.VideoCapture(0)
s6, im6 = cam6.read()
cv2.imwrite("im6.jpg", im6)
cam6.release()
os.rename(frame_path + 'im6.jpg', dest_path + 'im6.jpg')

print("FRAME 7")
ser.write(deg_dict[7])
time.sleep(move_wait)
cam7 = cv2.VideoCapture(0)
s7, im7 = cam7.read()
cv2.imwrite("im7.jpg", im7)
cam7.release()
os.rename(frame_path + 'im7.jpg', dest_path + 'im7.jpg')

print("FRAME 8")
ser.write(deg_dict[8])
time.sleep(move_wait)
cam8 = cv2.VideoCapture(0)
s8, im8 = cam8.read()
cv2.imwrite("im8.jpg", im8)
cam8.release()
os.rename(frame_path + 'im8.jpg', dest_path + 'im8.jpg')

print("FRAME 9")
ser.write(deg_dict[9])
time.sleep(move_wait)
cam9 = cv2.VideoCapture(0)
s9, im9 = cam9.read()
cv2.imwrite("im9.jpg", im9)
cam9.release()
os.rename(frame_path + 'im9.jpg', dest_path + 'im9.jpg')

print("FRAME 10")
ser.write(deg_dict[10])
time.sleep(move_wait)
cam10 = cv2.VideoCapture(0)
s10, im10 = cam10.read()
cv2.imwrite("im10.jpg", im10)
cam10.release()
os.rename(frame_path + 'im10.jpg', dest_path + 'im10.jpg')

print("FRAME 11")
ser.write(deg_dict[11])
time.sleep(move_wait)
cam11 = cv2.VideoCapture(0)
s11, im11 = cam11.read()
cv2.imwrite("im11.jpg", im11)
cam11.release()
os.rename(frame_path + 'im11.jpg', dest_path + 'im11.jpg')

print("FRAME 12")
ser.write(deg_dict[12])
time.sleep(move_wait)
cam12 = cv2.VideoCapture(0)
s12, im12 = cam11.read()
cv2.imwrite("im12.jpg", im12)
cam12.release()
os.rename(frame_path + 'im12.jpg', dest_path + 'im12.jpg')

print("FRAME 13")
ser.write(deg_dict[13])
time.sleep(move_wait)
cam13 = cv2.VideoCapture(0)
s13, im13 = cam13.read()
cv2.imwrite("im13.jpg", im13)
cam13.release()
os.rename(frame_path + 'im13.jpg', dest_path + 'im13.jpg')

print("return to home...")
ser.write('90\n')  # reset to original position
