import numpy as np
import cv2
from numba import jit

def python_color2sepia(image, sepia_effect = 1):
    """Function to turn an image from rgb color to sepia. 
    
    Args:
        image (:obj:`list` of :obj:`int`): The image can have any width and 
             height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`list` of :obj:`int`
             A new image with dimentsions (W, H, C) = (x, y, 3). 
    """
    # Sepia matrix
    s = np.array([[ 0.393 , 0.769 , 0.189],
                  [ 0.349 , 0.686 , 0.168],
                  [ 0.272 , 0.534 , 0.131]])

    
    s = (1 - sepia_effect) * np.eye(3,3) + (sepia_effect) * s
    # Matrix multiplication between Sepia matrix and pixel components of image
    # The transformation is done on RGB components of each pixel in image.
    im = [[[sum([s[j][i]*H[i] for i in range(3)]) for j in range(3)]
           for H in W] for W in image]

    # Grab the largest sum of the rows in s. This sum is larger than 1 and
    # will result in pixels with larger value than 255. Using this value we
    # can safely scale the transformed image back to max value of 255 while
    # keeping pixel ratios. 
    normalizer = (sum(s[0]))
    im = [[[int(C/normalizer) for C in H] for H in W] for W in im]
    return np.array(im, dtype="uint8")

def numpy_color2sepia(image, sepia_effect = 1):
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

    s = (1 - sepia_effect) * np.eye(3,3) + (sepia_effect) * s

    
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

@jit(nopython=True)
def numba_color2sepia(image, sepia_effect = 1):
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
    s = np.array([[ 0.393 , 0.769 , 0.189],
                  [ 0.349 , 0.686 , 0.168],
                  [ 0.272 , 0.534 , 0.131]])

    s = (1 - sepia_effect) * np.eye(3,3) + (sepia_effect) * s
    
    
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
    return np.array(im, dtype="uint8")

def sepia_image(input_filename, output_filename=None,
                implementation="numpy", scale = 1, sepia_effect = 1):
    """Converts given image to sepia, writes the image to disk and returns it.
    Args:
        input_filename (string): Searches for the image. The image can
             have any width and height, but needs to be RGB.
        output_filename (string): Writes the image to this location. If
             None appends _sepia to inputfilename at same location.
        implementation ({python, numpy, numba}): Provide argument for which
             implementation to use when applying the filter.
        sepia_effect (int): Must be between 0 and 1. How much sepia effect is
             to be applied

    Returns:
        :obj:`numpy.array of :obj:`uint8`
             A new image with the height and width dimension of the 
             original given image.
    """

    # Fetch- the correct function to use.
    function = implementation + "_color2sepia"
    method = globals()[function]
    
    # Reads the image and converts to RGB.
    image = cv2.cvtColor(cv2.imread(input_filename), cv2.COLOR_BGR2RGB)

    # Resize the image if requested
    if scale != 1:
        image = cv2.resize(image, (0,0), fx=scale, fy=scale)
    
    # Converts the image.
    converted_image = method(image, sepia_effect)

    # Be sure to name the effect correctly
    if sepia_effect == 0:
        named_effect = "_resized."
    else:
        named_effect = "_sepia." 


    if output_filename == None:
        # Returns the image in RGB.
        output_filename = named_effect.join([string for string in input_filename.rsplit(".", 1)])
        converted_image_BGR = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
        print(f"Writing file {output_filename} to disk") 
        cv2.imwrite(output_filename, converted_image_BGR)
        print("Done")
        return converted_image
    else:
        # Writes the image, since we are using cv2 we need to write in BGR
        print(f"Writing file {output_filename} to disk") 
        cv2.imwrite(output_filename, cv2.cvtColor(converted_image, cv2.COLOR_BGR2RGB))
        print("Done")
