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
    image = arguments.image
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
    print("ERROR\n Invalid argument, check the arguments")
    exit(1)

#https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
#DFT of a 1D signal value x
def DFT_naive(x):
    #length of signal x
    N = len(x)
    #return evenly spaced values within a given interval
    n = np.arange(N)
    k = n.reshape((N, 1))
    # DFT exponential part 
    e = np.exp((-1j * 2 * np.pi * k * n)/N)
    #the dot product
    X = np.dot(e, x)
    return X

#Inverse DFT of a 1D signal value x
def DFT_naive_inverse(x): 
    N = len(x)
    #return evenly spaced values within a given interval
    n = np.arange(N)
    k = n.reshape((N, 1))
    # DFT exponential part 
    e = np.exp((1j * 2 * np.pi * k * n)/N)
    #the dot product
    X = (np.dot(e, x)/N)
    return X

# DFT of a 2D array
def DFT_naive_2D(y):
    N = len(y)
    M = len(y[0])
    X = np.empty([N,M], dtype=complex)
    for column in range(M):
        X[:, column] = DFT_naive(X[:, column])
    for row in range(N):
        X[row, :] = DFT_naive(X[row, :])
    
    return X

#https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.03-Fast-Fourier-Transform.html
#1D FFT with an input signal x of a length of power of 2
def FFT(x):
    N = len(x)
    n = np.arange(N)
  #  k = n.reshape((N, 1))
    if N == 1:
        return x
    else:
         X_even = FFT(x[::2])
         X_odd = FFT(x[1::2])
         e = np.exp((-1j * 2 * np.pi * n)/N)
         X = np.concatenate([X_even + e[:int(N/2)] * X_odd, X_even + e[int(N/2):] * X_odd])
         return X

#1D inverse FFT with an input signal x of a length of power of 2
def FFT_inverse(x):
    N = len(x)
    n = np.arange(N)
  #  k = n.reshape((N, 1))
    if N == 1:
        return x
    else:
         X_even = FFT_inverse(x[::2])
         X_odd = FFT_inverse(x[1::2])
         e = np.exp((1j * 2 * np.pi * n)/N)
         X = np.concatenate([X_even + e[:int(N/2)] * X_odd, X_even + e[int(N/2):] * X_odd])/N
         return X
   
# FFT of a 2D array
def FFT_2D(y):
    N = len(y)
    M = len(y[0])
    X = np.empty([N,M], dtype=complex)
    for column in range(M):
        X[:, column] = FFT(X[:, column])
    for row in range(N):
        X[row, :] = FFT(X[row, :])
    
    return X

# inverse FFT of a 2D array
def FFT_2D_inverse(y):
    N = len(y)
    M = len(y[0])
    X = np.empty([N,M], dtype=complex)
    for column in range(M):
        X[:, column] = FFT_inverse(X[:, column])
    for row in range(N):
        X[row, :] = FFT_inverse(X[row, :])
    
    return X

def compression():
    pass
      
