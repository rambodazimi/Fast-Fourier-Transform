#fft application
#Authors: 
#Rambod Azimi 
#Saghar Sahebi
# ECSE 316 - Assignment 2 - Winter 2023
# Group 39

"""
• Performs DFT both with the naïve algorithm and the FFT algorithm
• Performs the inverse operation. For the inverse just worry about the FFT implementation.
• Handles 2D Fourier Transforms (2d-FFT) and its inverse.
• Plots the resulting 2D DFT on a log scale plot.
the syntax for running the app is: 
python3 fft.py [-m mode] [-i image]
"""
import numpy as np
import matplotlib.pyplot as plot
import matplotlib.colors as colors
import time
import sys 
import argparse

#default values for argument 
default_mode = 1
default_image = "moonlanding.png"

def __main__ ():
    parse = argparse.ArgumentParser()

    parse.add_argument("-m", dest="mode" ,type= int, default= default_mode, help= "the value must be between 1 and 4")
    parse.add_argument("-i", dest="image" ,type=str, default=default_image, help="the file needs to be an image")

    arguments = parse.parse_args()
    mode = arguments.mode
    if (mode == 1):
            mode1()
    elif (mode == 2):
            mode2()
    elif (mode == 3):
            mode3()
    elif (mode == 4):
            mode4()
    else:
          invalid_type_error()
def mode1():
      pass
def mode2():
      pass
def mode3():
      pass
def mode4():
      pass
def invalid_type_error():
    print("ERROR, invalid argument")
    exit(1)