#!/usr/bin/env pythin

import numpy as np
from numba import jit
import cv2

def python_color2gray(image):
    """Function to turn an image from rgb color to grayscale. It also times
        the time.
    
    Args:
        image (:obj:`list` of :obj:`int`): The image can have any width and 
             height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`list` of :obj:`int`
             A new image with dimentsions (W, H). The channel dimension has 
             been merged into a single grayscale channel. 
             
    """
    image = [[int(px[0]*0.21 +
                  px[1]*0.72 +
                  px[2]*0.07) for px in col] for col in image]
    
    return np.array(image, dtype="uint8")


def numpy_color2gray(image):
    """Function to turn an image from rgb color to grayscale. It also times
        the time. This implementation uses numpy for speed.
    
    Args:
        image (:obj:`numpy.array` of :obj:`int`): The image can have any 
             width and height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`numpy.array` of :obj:`int`
             A new image with dimentsions (W, H). The channel dimension has 
             been merged into a single grayscale channel. 
             
    """
    image = image[:,:,0]*0.21 + image[:,:,1]*0.72 + image[:,:,2]*0.07
    return image.astype("uint8")

@jit
def numba_color2gray(image):
    """Function to turn an image from rgb color to grayscale. It also times
        the time. This version uses numba for speed.
    
    Args:
        image (:obj:`list` of :obj:`int`): The image can have any width and 
             height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`list` of :obj:`int`
             A new image with dimentsions (W, H). The channel dimension has 
             been merged into a single grayscale channel. 
             
    """
    image = [[int(px[0]*0.21 +
                  px[1]*0.72 +
                  px[2]*0.07) for px in col] for col in image]
    
    return np.array(image, dtype="uint8")

def grayscale_image(input_filename, output_filename=None,
                    implementation="numpy", scale = 1, sepia_effect = 1):
    """Converts given image to grayscale, writes it to disk and returns it.
    Args:
        input_filename (string): Searches for the image. The image can
             have any width and height, but needs to be RGB.
        output_filename (string): Writes the image to this location. If
             None appends _gray to inputfilename at same location.
        implementation ({python, numpy, numba}):
             Provide argument for which implementation to use when 
             applying the filter.
        sepia_effect (int): Redundant variable used for sepia images.

    Returns:
        :obj:`numpy.array of :obj:`uint8`
             A new image with the height and width dimension of the 
             original given image.
    """
    # Fetch the correct function to use
    function = implementation + "_color2gray"
    method = globals()[function]
    
    # Reads in the image and converts from BGR to RGB.
    image = cv2.cvtColor(cv2.imread(input_filename), cv2.COLOR_BGR2RGB)

    # Resize the image if requested.
    if scale != 1:
        image = cv2.resize(image, (0,0), fx=scale, fy=scale)
    
    # Converts the image.
    converted_image = method(image)
    if output_filename == None:
        # Returns the image, format is RGB.
        output_filename = "_gray.".join([string for string in input_filename.rsplit(".", 1)])
        print(f"Writing file {output_filename} to disk") 
        cv2.imwrite(output_filename, cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR))
        print(f"Done") 
        return converted_image
    else:
        # Writes the image using cv2. Must therefore convert to BGR.
        print(f"Writing file {output_filename} to disk") 
        cv2.imwrite(output_filename, cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR))
        print(f"Done") 
        return converted_image
