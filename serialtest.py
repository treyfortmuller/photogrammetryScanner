import serial
import time
import os

from threading import Thread 


ser = serial.Serial("/dev/ttyACM0", 9600)  # open serial communication at 9600 baud to the arduino
print("initializing...")
time.sleep(7)  # wait for initialization of the serial communication to Arduino

def write():
	theta = 1
	for i in range(10):
		ser.write(str(theta*i))
		time.sleep(2)

def read():
	while True:
		for line in ser.read():
			print("RECEIVED: " + str(line))


w = Thread(target=write)
w.start()
# read()
w.join()

print("DONE")