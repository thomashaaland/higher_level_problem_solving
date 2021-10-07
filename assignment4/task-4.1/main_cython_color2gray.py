# -*- coding: utf-8 -*-
import numpy as np
from numba import jit
import cython
import ctypes
import cv2
import timeit
from python_color2gray import python_color2gray
from numpy_color2gray import numpy_color2gray
from numba_color2gray import numba_color2gray
from cython_color2gray import cython_color2gray

# Run this section if the program is run as main
if __name__ == "__main__":
    # Default filename, use rain.jpg for testing
    filename = "rain.jpg"
    # Write to this file for testing
    to_filename = "rain_grayscale.jpeg"
    # ready the image in a numpy array and change from BGR to RGB
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    print(f"Turning the file {filename} (dimenions: (H, W, C) = {image.shape}) to grayscale")

    # Call the function rgb_to_grayscale to create the grayscale image
    grayscale_image_cython = np.array(cython_color2gray(image), dtype="uint8")
    print(f"Image {to_filename} (dimensions: (H, W, C) = {grayscale_image_cython.shape}).")

    # write the image
    cv2.imwrite(to_filename, grayscale_image_cython)

    # Perform benchmarking

    times = timeit.repeat(stmt='python_color2gray(image)',
                          setup="from __main__ import python_color2gray, image",
                          repeat = 5,
                          number = 5)

    times_np = timeit.repeat(stmt='numpy_color2gray(image)',
                             setup="from __main__ import numpy_color2gray, image",
                             repeat = 5,
                             number = 5)

    times_numba = timeit.repeat(stmt='numba_color2gray(image)',
                                setup="from __main__ import numba_color2gray, image",
                                repeat = 5,
                                number = 5)

    times_cython = timeit.repeat(stmt='cython_color2gray(image)',
                                 setup='from __main__ import cython_color2gray, image',
                                 repeat = 5,
                                 number = 5)

    print("Writing report")

    # Write to file
    with open("cython_report_color2gray.txt", "w") as f:
        f.write(
            f"""
Timing: cython_color2gray
Average runtime running cython_color2gray after 5 runs: {sum(times_cython)/len(times_cython):.4f} s
Average runtime running of cython_color2gray is {(sum(times)/len(times))/(sum(times_cython)/len(times_cython)):.2f} times faster 
            than python_color2gray
Average runtime running of cython_color2gray is {(sum(times_np)/len(times_np))/(sum(times_cython)/len(times_cython)):.2f} times faster 
            than numpy_color2gray
Average runtime running of cython_color2gray is {(sum(times_numba)/len(times_numba))/(sum(times_cython)/len(times_cython)):.2f} times faster 
            than numpy_color2gray
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of grayscale image: {grayscale_image_cython.shape}
            """)
        
