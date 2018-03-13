# scratch script to remove the exif meta data from the photo dataset in prep to send it to the sfm pipeline

import os
import subprocess

PROJECT_DIR = input_eval_dir = os.path.dirname(os.path.abspath(__file__))  # the sfm_test directory
input_dir = "/../sfm_in"  # the sfm_in directory with the photo dataset

input_dir = PROJECT_DIR + input_dir  # full path to photos

for filename in os.listdir(input_dir):
    print(filename)

