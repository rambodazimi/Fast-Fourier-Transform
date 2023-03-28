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
import cv2

#default values for argument 
default_mode = 1
default_image = "moonlanding.png"


"""
Error handlers
"""

def invalid_type_error():
    print("ERROR\n Invalid argument, check the arguments")
    exit(1)


"""
all definitions for different DFTs and FFTs
"""
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



"""
adjusting and resizing the input image if necessary(not power of two already)
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
def compression(img,rate):
    size= (img.shape[0] * img.shape[1]) * rate //100
    temp = img.flatten()
    for i in range(size):
        temp[(np.argpartition(np.abs(img), size))[i]]=0
    
    compressed_image = np.reshape(temp, img.shape)
    np.savez_compressed('compression-'+rate, compressed_image )

    return compressed_image


"""
Different modes of the argument passed
"""

def mode1(img):
    FFT_image = np.abs(FFT_2D(img))
    #one by two subplot of the original image 
    plot.title("Original image --> before FFT")
    plot.subplot(1,2,1)
    plot.imshow(img, cmap= 'gray')

    #one by two subplot of the FFT image
    plot.title("transformed image --> after FFT")
    plot.subplot(1,2,2)
    plot.imshow(FFT_image, norm= colors.LogNorm())

    plot.show()

def mode2(img):
    # the denoise factor, we chose to go with 0.4
    denoise_factor = 0.4
    FFT_image = FFT_2D(img)
    #count the non zero for later when calculating the fraction 
    before_zero = np.count_nonzero(FFT_image)
    
    #setting the high frequencies to 0 
    #width 
    FFT_image[:, int(denoise_factor* FFT_image.shape[1]) : int(FFT_image.shape[1] * (1-denoise_factor))] = 0 
    #height
    FFT_image[int(denoise_factor* FFT_image.shape[0]) : int(FFT_image.shape[1] * (1-denoise_factor))] = 0

    #count the new non zero 
    after_zero = np.count_nonzero(FFT_image)
    inverse_FFT_image = FFT_2D_inverse(FFT_image).real
    #as asked in the assignment pring the fraction and non-zeros 
    fraction = (after_zero/before_zero)
    print("the number of non-zeros are:", after_zero)
    print("the fraction they represent of the original Fourier coefficients:", fraction)
    #before
    plot.title("original image --> before denoising")
    plot.subplot(1,2,1)
    plot.imshow(img, cmap= 'gray')
    # after
    plot.title("transformed image --> after denoising")
    plot.subplot(1,2,2)
    plot.imshow(inverse_FFT_image, cmap= 'gray')

    plot.show()

def mode3(img):
    FFT_image = FFT_2D(img)
    rate = [0, 0.2,0.4,0.6,0.8,0.9]
    #we need to perform compression
    # we will compress with 6 different levels and plot them 
    plot.title("0 compression")
    plot.subplot(2,3,1)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[0]))), cmap= 'gray')

    plot.title("20 percent compression")
    plot.subplot(2,3,2)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[1]))), cmap= 'gray')

    plot.title("40 percent compression")
    plot.subplot(2,3,3)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[2]))), cmap= 'gray')

    plot.title("60 percent compression")
    plot.subplot(2,3,4)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[3]))), cmap= 'gray')

    plot.title("80 percent compression")
    plot.subplot(2,3,5)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[4]))), cmap= 'gray')

    plot.title("90 percent compression")
    plot.subplot(2,3,6)
    plot.imshow(np.real(FFT_2D_inverse(compression(FFT_image.copy(), rate[5]))), cmap= 'gray')

    plot.show()

def mode4(img):
    testPlots = [
        (2 ** 5, 2 ** 5),
        (2 ** 6, 2 ** 6),
        (2 ** 7, 2 ** 7),
        (2 ** 8, 2 ** 8),
        (2 ** 9, 2 ** 9),
        (2 ** 10, 2 ** 10),
    ]
    #y axis for naive implementation
    naive_time = []
    #y axis for fast implementation
    fast_time =[]
    # x axis for both based on the test plots
    size_list = [2 ** 5, 2 ** 6, 2 ** 7,2 ** 8, 2 ** 9, 2 ** 10,]
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


    for element in testPlots:
        #the range is 10 based on the assignment description
        for test_time in range(10):
            start_time = time.time()
            DFT_naive_2D(img)
            end_time = time.time()
            duration = end_time-start_time
            naive_time.append(duration)

            start_time = time.time()
            FFT_2D(img)
            end_time = time.time()
            duration = end_time-start_time
            fast_time.append(duration)
       
        print("The size is :", element)
       # size_list.append(size)
       # size = size * 2
        #calculate the mean 
        naive_mean_var = np.mean(naive_time)
        fast_mean_var = np.mean(fast_mean)
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
    parse = argparse.ArgumentParser()

    parse.add_argument("-m", dest="mode" ,type= int, default= default_mode, help= "the value must be between 1 and 4")
    parse.add_argument("-i", dest="image" ,type=str, default=default_image, help="the file needs to be an image")

    arguments = parse.parse_args()
    mode = arguments.mode
    image = arguments.image

    if (mode == 1):
        mode1(resizeImg(image))
    elif (mode == 2):
        mode2(resizeImg(image))
    elif (mode == 3):
        mode3(resizeImg(image))
    elif (mode == 4):
        mode4(resizeImg(image))
    else:
        invalid_type_error()
      
