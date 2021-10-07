# -*- coding: utf-8 -*-
import numpy as np
import cv2
import timeit
from python_color2sepia import python_color2sepia

def numpy_color2sepia(image):
    """Function to turn an image from rgb color to sepia. 
        This implementation uses numpy for speed.
    
    Args:
        image (:obj:`numpy.array` of :obj:`int`): The image can have any 
             width and height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`numpy.array` of :obj:`int`
             A new image with dimentsions (W, H, 3). 
    """
    # Sepia matrix
    s = np.array([[ 0.393 , 0.769 , 0.189],
                  [ 0.349 , 0.686 , 0.168],
                  [ 0.272 , 0.534 , 0.131]])
    
    # Grab the largest sum of the rows in s. This sum is larger than 1 and will result
    # in pixels with larger value than 255. Using this value we can safely scale the
    # transformed image back to max value of 255 while keeping pixel ratios. 
    normalizer = np.sum(s[0])

    # To multiply matrix s with the color vector of each pixel we do an einsteinsum
    # leaving the free indices ijl to be the first two indices of the image
    # and the final to be the first index of the matrix. This means we sum
    # the rows of the matrix with the RGB components of the pixels in the image.
    im = np.einsum('ijk,lk', image.astype("int"), s)

    return (im / normalizer).astype("uint8")    

# Run this section if the program is run as main
if __name__ == "__main__":
    # Default filename, use rain.jpg for testing
    filename = "rain.jpg"
    # Write to this file for testing
    to_filename = "rain_sepia.jpeg"
    # ready the image in a numpy array and change from BGR to RGB
    image = cv2.imread(filename)
    print(f"Turning the file {filename} (dimenions: (H, W, C) = {image.shape}) to sepia")

    # Call the function numpy_color2sepia to create the sepia image
    sepia_image_np = cv2.cvtColor(numpy_color2sepia(image), cv2.COLOR_BGR2RGB)
    print(f"Image {to_filename} (dimensions: (H, W, C) = {sepia_image_np.shape}).")

    # write the image
    cv2.imwrite(to_filename, sepia_image_np)

    # Perform benchmarking

    times = timeit.repeat(stmt='python_color2sepia(image)',
                          setup="from __main__ import python_color2sepia, image",
                          repeat = 5,
                          number = 5)

    times_np = timeit.repeat(stmt='numpy_color2sepia(image)',
                             setup="from __main__ import numpy_color2sepia, image",
                             repeat = 5,
                             number = 5)


    print("Writing report")

    # Write to file
    with open("numpy_report_color2sepia.txt", "w") as f:
        f.write(
            f"""
Timing: numpy_color2sepia
Average runtime running numpy_color2sepia after 3 runs: {sum(times_np)/len(times_np):.4f} s
Average runtime running of numpy_color2sepia is {(sum(times)/len(times))/(sum(times_np)/len(times_np)):.2f} times faster 
            than python_color2sepia
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of sepia image: {sepia_image_np.shape}
            """)
