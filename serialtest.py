import serial
import time
import os


ser = serial.Serial("/dev/cu.usbmodem1421", 9600)  # open serial communication at 9600 baud to the arduino
print("initializing...")
time.sleep(7)  # wait for initialization of the serial communication to Arduino


theta = 30
for i in range(10):
	ser.write(str(theta*i))
	time.sleep(2)
