# -*- coding: utf-8 -*-
import numpy as np
from numba import jit
import cv2
import timeit
from python_color2sepia import python_color2sepia
from numpy_color2sepia import numpy_color2sepia

@jit(nopython=True)
def numba_color2sepia(image):
    """Function to turn an image from rgb color to sepia. It also times
        the time. This version uses numba for speed.
    
    Args:
        image (:obj:`list` of :obj:`int`): The image can have any width and 
             height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`list` of :obj:`int`
             A new image with dimentsions (W, H). The channel dimension has 
             been merged into a single sepia channel. 
             
    """
    # Sepia matrix
    s = [[ 0.393 , 0.769 , 0.189],
         [ 0.349 , 0.686 , 0.168],
         [ 0.272 , 0.534 , 0.131]]
    
    # Matrix multiplication between Sepia matrix and pixel components of image
    # The transformation is done on RGB components of each pixel in image.
    im = [[[sum([s[j][i]*H[i] for i in range(3)]) for j in range(3)]
           for H in W] for W in image]
    
    # Grab the largest sum of the rows in s. This sum is larger than 1 and will result
    # in pixels with larger value than 255. Using this value we can safely scale the
    # transformed image back to max value of 255 while keeping pixel ratios. 
    normalizer = 1 / (sum(s[0]))
        
    # 255 = maximum_value * scale -> scale = 255 / maximum_value
    im = [[[int(C*normalizer) for C in H] for H in W] for W in im]
    return im



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
    sepia_image_numba = np.array(numba_color2sepia(image), dtype="uint8")
    print(f"Image {to_filename} (dimensions: (H, W, C) = {sepia_image_numba.shape}).")

    # write the image
    cv2.imwrite(to_filename, cv2.cvtColor(sepia_image_numba, cv2.COLOR_RGB2BGR))

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

    print("Writing report")

    # Write to file
    with open("numba_report_color2sepia.txt", "w") as f:
        f.write(
            f"""
Timing: numba_color2sepia
Average runtime running numba_color2sepia after 3 runs: {sum(times_numba)/len(times_numba):.4f} s
Average runtime running of numba_color2sepia is {(sum(times)/len(times))/(sum(times_np)/len(times_np)):.2f} times faster 
            than python_color2sepia
Average runtime running of numba_color2sepia is {(sum(times_np)/len(times_np))/(sum(times_numba)/len(times_numba)):.2f} times faster 
            than numpy_color2sepia
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of sepia image: {sepia_image_numba.shape}
            """)
