# cython: language_level=2
import numpy as np
cimport numpy as np
cimport cython
import ctypes

DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

def cython_color2gray(np.ndarray[DTYPE_t, ndim=3] img):
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
    
    if img.shape[2] != 3:
            raise ValueError("You need to provide a color image.")
    assert img.dtype == DTYPE
    
    cdef Py_ssize_t i = 0
    cdef Py_ssize_t j = 0
    cdef unsigned int w = img.shape[0]
    cdef unsigned int h = img.shape[1]
    cdef double result = 0
    cdef np.ndarray[DTYPE_t, ndim=2] final_img = np.empty([w,h], dtype=DTYPE)
    
    for i in range(w):
        for j in range(h):
            result = img[i, j, 0]*0.21 + img[i, j, 1]*0.72 + img[i, j, 2]*0.07
            final_img[i, j] = <DTYPE_t>result 
    
    return final_img
