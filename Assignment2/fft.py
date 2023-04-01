# fft application
# Authors: 
# Rambod Azimi 
# Saghar Sahebi
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
import os
import argparse
import cv2

# default values for argument 
default_mode = 1
default_image = "moonlanding.png"

"""
Error handlers
"""

def invalid_type_error():
    print("ERROR! Invalid argument. Please check the arguments")
    exit(1)

def invalid_image_error():
    print("ERROR! Invalid image. Please check the filename")
    exit(1)

"""
all definitions for different DFTs and FFTs
"""
# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.02-Discrete-Fourier-Transform.html
# DFT of a 1D signal value x
def DFT_naive(x):
    # length of signal x
    N = len(x)
    # return evenly spaced values within a given interval
    n = np.arange(N)
    k = n.reshape((N, 1))
    # DFT exponential part 
    e = np.exp((-1j * 2 * np.pi * k * n)/N)
    # the dot product
    X = np.dot(e, x)
    return X

# Inverse DFT of a 1D signal value x
def DFT_naive_inverse(x): 
    N = len(x)
    # return evenly spaced values within a given interval
    n = np.arange(N)
    k = n.reshape((N, 1))
    # DFT exponential part 
    e = np.exp((1j * 2 * np.pi * k * n)/N)
    # the dot product
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

# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter24.03-Fast-Fourier-Transform.html
# 1D FFT with an input signal x of a length of power of 2
def FFT(x):
    N = len(x)
    if N == 1:
        return x
    
    n = np.arange(N) # n = evenly spaced values within the interval
    X_even = FFT(x[0::2]) # recursively call FFT on the even inputs of x
    X_odd = FFT(x[1::2]) # recursively call FFT on the odd inputs of x

    e = np.exp((-1j * 2 * np.pi * n)/N) # Math part
    X = np.concatenate([X_even + e[:int(N/2)] * X_odd, X_even + e[int(N/2):] * X_odd])
    return X

# 1D inverse FFT with an input signal x of a length of power of 2
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
def FFT_2D(image: np.ndarray):

    M = len(image)
    N = len(image[0])
    X = np.zeros([M,N], dtype='complex_')

    for i, row in enumerate(image): # call the FFT on each row of image
        X[i] = FFT(row)

    X2 = np.zeros([N,M], dtype='complex_')
    for i, col in enumerate(X.T): # call the FFT on each column of image
        X2[i] = FFT(col)

    return X2.T

# inverse FFT of a 2D array
def FFT_2D_inverse(y):
    M = len(y)
    N = len(y[0])
    X = np.empty([M,N], dtype='complex_')
    for i, row in enumerate(y): # apply the FFT_inverse on each row of image y
        X[i] = FFT_inverse(row)

    X2 = np.empty([N,M], dtype='complex_')
    for i, col in enumerate(X.T): # apply the FFT_inverse on each column of image y
        X2[i] = FFT_inverse(col)

    return X2.T

"""
adjusting and resizing the input image if necessary (not power of two already)
"""
def resizeImg(img):
    image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    height = len(image)
    width = len(image[0])

    if height != 2 ** (int(np.log2(height))):
        height = 2 ** (int(np.log2(height))+1)

    if width != 2 ** (int(np.log2(width))):
        width = 2 ** (int(np.log2(width))+1)
    final_image = cv2.resize(image,(width,height))
   
    return final_image

"""
Compression with a specified rate for mode 3
"""
def compression(img, rate):
    size = (img.shape[0] * img.shape[1]) * rate //100
    temp = img.flatten()
   # for i in range(int(size)):
   #    temp[(np.argpartition(np.abs(img), size))[i]]=0
    
    compressed_image = np.reshape(temp, img.shape)
    np.savez_compressed('compression-'+str(rate), compressed_image)

    return compressed_image

"""
Different modes of the argument passed
"""
def mode1(img):
    FFT_image = np.abs(FFT_2D(img)) # calling FFT_2D function and save the result in FFT_image
    
    # one by two subplot of the original image 
    plot.subplot(1,2,1)
    plot.imshow(img, cmap= 'gray')
    plot.title("(Before FFT)")

    #one by two subplot of the FFT image
    plot.subplot(1,2,2)
    plot.imshow(FFT_image, norm=colors.LogNorm())
    plot.title("(After FFT)")

    plot.show()

def mode2(img):
    print("Mode 2 is running...")
    # the denoise factor, we chose to go with 0.4
    denoise_factor = 0.4
    FFT_image = FFT_2D(img)
    # count the non zero for later when calculating the fraction 
    before_zero = np.count_nonzero(FFT_image)
    # setting the high frequencies to 0 
    # width 
    FFT_image[:, int(denoise_factor * FFT_image.shape[1]) : int(FFT_image.shape[1] * (1-denoise_factor))] = 0 
    # height
    FFT_image[int(denoise_factor * FFT_image.shape[0]) : int(FFT_image.shape[1] * (1-denoise_factor))] = 0

    # count the new non zero 
    after_zero = np.count_nonzero(FFT_image)

    inverse_FFT_image = FFT_2D_inverse(FFT_image).real
    # as asked in the assignment printing the fraction and non-zeros 
    fraction = (after_zero/before_zero)
    print(f"The number of non-zeros are: {after_zero}")
    print(f"The fraction they represent of the original Fourier coefficients: {fraction}")
    # before
    plot.subplot(1,2,1)
    plot.imshow(img, cmap= 'gray')
    plot.title("(Before denoising)")
    # after
    plot.subplot(1,2,2)
    plot.imshow(inverse_FFT_image, cmap= 'gray')
    plot.title("(After denoising)")
    plot.show()

def mode3(img):
    print("Mode 3 is running...")
    FFT_image = FFT_2D(img)
    rate = [0, 0.2, 0.4, 0.6, 0.8, 0.95]
    # we need to perform compression
    # we will compress with 6 different levels and plot them 
    plot.subplot(2,3,1)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[0]))), cmap= 'gray')
    plot.title("0%")

    plot.subplot(2,3,2)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[1]))), cmap= 'gray')
    plot.title("20%")

    plot.subplot(2,3,3)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[2]))), cmap= 'gray')
    plot.title("40%")

    plot.subplot(2,3,4)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[3]))), cmap= 'gray')
    plot.title("60%")

    plot.subplot(2,3,5)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[4]))), cmap= 'gray')
    plot.title("80%")

    plot.subplot(2,3,6)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[5]))), cmap= 'gray')
    plot.title("95%")
    plot.show()

def mode4(img):
    print("Mode 4 is running...")
    testPlots = [np.random.rand(2 ** 5, 2 ** 5),
        np.random.rand(2 ** 6, 2 ** 6),
        np.random.rand(2 ** 7, 2 ** 7),
        np.random.rand(2 ** 8, 2 ** 8),
        np.random.rand(2 ** 9, 2 ** 9),
        np.random.rand(2 ** 10, 2 ** 10),
    ]
    #y axis for naive implementation
    naive_time = []
    #y axis for fast implementation
    fast_time =[]
    # x axis for both based on the test plots
    size_list = [2 ** 5, 2 ** 6, 2 ** 7,2 ** 8, 2 ** 9, 2 ** 10]
    #size = 2**5
    #standard daviation of naive implementation 
    naive_std = []
    #mean of naive implementation
    naive_mean =[]
    #variance of naive implementation
    naive_variance=[]
    #standard daviation of fast implementation 
    fast_std = []
    #mean of fast implementation
    fast_mean =[]
    #variance of fast implementation
    fast_variance=[]

    #iterator for printing size
    count = 0
    for element in testPlots:
        #the range is 10 based on the assignment description
        for i in range(10):
            start_time = time.time()
            DFT_naive_2D(element)
            end_time = time.time()
            duration = end_time-start_time
            naive_time.append(duration)

            start_time = time.time()
            FFT_2D(element)
            end_time = time.time()
            duration = end_time-start_time
            fast_time.append(duration)
       
        print("The size is :", size_list[count] ,"by", size_list[count] )
        count += 1
       # size_list.append(size)
       # size = size * 2
        #calculate the mean 
        naive_mean_var = np.mean(naive_time)
        fast_mean_var = np.mean(fast_time)
        print("The mean of the DFT is:", naive_mean_var )
        print("The mean of the FFT is:", fast_mean_var )
        #add to the array 
        naive_mean.append(naive_mean_var)
        fast_mean.append(fast_mean_var)

        #calculate the standard deviation 
        naive_std_var = np.std(naive_time)
        fast_std_var = np.std(fast_time)
        print("The standard deviation of the DFT is:", naive_std_var )
        print("The standard deviation of the FFT is:", fast_std_var )
        #add to the array 
        naive_std.append(naive_std_var)
        fast_std.append(fast_std_var)

        naive_variance_var = np.var(naive_time)
        fast_variance_var = np.var(fast_time)
        print("The variance of the DFT is:", naive_variance_var)
        print("The variance of the FFT is:", fast_variance_var)
        #add to the array 
        naive_variance.append(naive_variance_var)
        fast_variance.append(fast_variance_var)

    plot.title("Runtime vs Size")
    plot.xlabel("size")
    plot.ylabel("runtime (sec)")
    plot.errorbar(size_list, naive_mean, yerr=naive_std, linestyle='solid', color='yellow',label="slow")
    plot.errorbar(size_list, fast_mean, yerr=fast_std, linestyle='solid', color='green',label="fast")
    plot.show()

"""
Passing arguments
"""
def __main__ ():

    parse = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # mode with the default value of 1
    parse.add_argument("-m", dest="mode" ,type= int, default= default_mode, help= "The mode can be any number from 1 to 4")

    # image with the default value of moonlanding.png
    parse.add_argument("-i", dest="image" ,type=str, default=default_image, help="The image should be the filename of the image we wish to take the DFT of")

    # put all the parser arguments into a variable
    arguments = parse.parse_args()

    # store the mode and image arguments into variables
    mode = arguments.mode
    image = arguments.image

    if not (os.path.isfile(image)): # if the image does not exist in the current directory, print an error message
        invalid_image_error()

    if (mode == 1): # (Default) image is converted into its FFT form and displayed
        print("Mode 1 is running...")
        mode1(resizeImg(image))
    elif (mode == 2): # image is denoised by applying an FFT, truncating high frequencies and then displayed
        mode2(resizeImg(image))
    elif (mode == 3): # for compressing and saving the image
        mode3(resizeImg(image))
    elif (mode == 4): # for plotting the runtime graphs for the report
        mode4(resizeImg(image))
    else:
        invalid_type_error() # if the mode is anything other than [1,4], print the error message

if __name__ == "__main__":
    print("Starting the software...")
    __main__()
