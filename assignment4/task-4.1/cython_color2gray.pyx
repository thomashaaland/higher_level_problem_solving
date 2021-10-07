# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np
import cython
import ctypes

cpdef cython_color2gray(np.ndarray[np.uint8_t, ndim=3, cast = True] image):
    """Function to turn an image from rgb color to grayscale. It also times
        the time. This version is to be compiled with cython for speed.
    
    Args:
        image (:obj:`list` of :obj:`int`): The image can have any width and 
             height dimension, but it needs to be RGB for the 
             conversion to work properly. Dimension ((W, H, C) = (x, y, 3))

    Returns:
        :obj:`list` of :obj:`int`
             A new image with dimentsions (W, H). The channel dimension has 
             been merged into a single grayscale channel. 
             
    """
    cdef int i, j
    cdef int w, h
    w = image.shape[0]
    h = image.shape[1]
    cdef np.ndarray[np.uint8_t, ndim=2] final_image = np.empty((w,h), dtype='uint8')

    for i in range(w):
        for j in range(h):
            final_image[i][j] = ( (float)(image[i][j][0])*0.21 + (float)(image[i][j][1])*0.72 + (float)(image[i][j][2])*0.07 ) 

    
    return final_image
