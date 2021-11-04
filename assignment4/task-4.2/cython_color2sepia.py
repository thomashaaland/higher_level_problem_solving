# -*- coding: utf-8 -*-
import numpy as np
from numba import jit
import cython
import ctypes
import cv2
import timeit
from python_color2sepia import python_color2sepia
from numpy_color2sepia import numpy_color2sepia
from numba_color2sepia import numba_color2sepia
from cython_color2sepia import cython_color2sepia

# Run this section if the program is run as main
if __name__ == "__main__":
    # Default filename, use rain.jpg for testing
    filename = "rain.jpg"
    # Write to this file for testing
    to_filename = "rain_sepia.jpeg"
    # ready the image in a numpy array and change from BGR to RGB
    image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
    print(f"Turning the file {filename} (dimenions: (H, W, C) = {image.shape}) to sepia")

    # Call the function rgb_to_sepia to create the sepia image
    sepia_image_cython = np.array(cython_color2sepia(image), dtype="uint8")
    print(f"Image {to_filename} (dimensions: (H, W, C) = {sepia_image_cython.shape}).")

    # write the image
    cv2.imwrite(to_filename, cv2.cvtColor(sepia_image_cython, cv2.COLOR_RGB2BGR))

    # Perform benchmarking

    times = timeit.repeat(stmt='python_color2sepia(image)',
                          setup="from __main__ import python_color2sepia, image",
                          repeat = 5,
                          number = 5)

    times_np = timeit.repeat(stmt='numpy_color2sepia(image)',
                             setup="from __main__ import numpy_color2sepia, image",
                             repeat = 5,
                             number = 5)

    times_numba = timeit.repeat(stmt='numba_color2sepia(image)',
                                setup="from __main__ import numba_color2sepia, image",
                                repeat = 5,
                                number = 5)

    times_cython = timeit.repeat(stmt='cython_color2sepia(image)',
                                 setup="from __main__ import cython_color2sepia, image",
                                 repeat = 5,
                                 number = 5)

    print("Writing report")

            # Write to file                                                                    
    with open("cython_report_color2sepia.txt", "w") as f:                               
        f.write(                                                                       
            f"""
Timing: cython_color2sepia
Average runtime running cython_color2sepia after 5 runs: {sum(times_cython)/len(times_cython):.4f} s
Average runtime running of cython_color2sepia is {(sum(times)/len(times))/(sum(times_cython)/len(times_cython)):.2f} times faster
            than python_color2sepia
Average runtime running of cython_color2sepia is {(sum(times_np)/len(times_np))/(sum(times_cython)/len(times_cython)):.2f} times faster
            than numpy_color2sepia
Average runtime running of cython_color2sepia is {(sum(times_numba)/len(times_numba))/(sum(times_cython)/len(times_cython)):.2f} times faster
            than numba_color2sepia
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of sepia image: {sepia_image_cython.shape}
            """)

        
