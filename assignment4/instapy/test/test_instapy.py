import numpy as np
import matplotlib.pyplot as plt
import instapy.grayscale_image as gray
import instapy.sepia_image as sepia

def test_gray_filter():
    # Test to check that the gray filter works
   shape = (600, 400, 3)
   random_array = (np.random.rand(*shape)*255).astype("uint8")
   test_pixel = int(random_array[0,0] @ np.array([0.21, 0.72, 0.07]))
   python_gray = np.array(gray.python_color2gray(random_array))
   numpy_gray = np.array(gray.numpy_color2gray(random_array))
   numba_gray = np.array(gray.numba_color2gray(random_array))

   assert test_pixel == python_gray[0,0]
   assert test_pixel == numpy_gray[0,0]
   assert test_pixel == numba_gray[0,0]   
   

def test_sepia_filter():
    # Test to check that the sepia filter works
   shape = (600, 400, 3)
   random_array = (np.random.rand(*shape)*255).astype("uint8")
   s = np.array([[ 0.393, 0.769, 0.189],
                 [ 0.349, 0.686, 0.168],
                 [ 0.272, 0.534, 0.131]])
   
   test_pixel = ((s @ random_array[0,0]) / np.sum(s[0])).astype("uint8")
   python_sepia = np.array(sepia.python_color2sepia(random_array))
   numpy_sepia = np.array(sepia.numpy_color2sepia(random_array))
   numba_sepia = np.array(sepia.numba_color2sepia(random_array))

   assert all(test_pixel == python_sepia[0,0])
   assert all(test_pixel == numpy_sepia[0,0])
   assert all(test_pixel == numba_sepia[0,0])   
