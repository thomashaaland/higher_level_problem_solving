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


def test_grayfilter2():
    # Test to check that the gray filter works

    fakeimage = np.random.randint(0, 256, size=(400, 600, 3))
    output =  np.array(gray.numba_color2gray(fakeimage))
    output2 = np.array(gray.numpy_color2gray(fakeimage))
    output3 = np.array(gray.numpy_color2gray(fakeimage))

    i = np.random.randint(0, 400)
    j = np.random.randint(0, 600)
    expected = 0

    w = [0.21, 0.72, 0.07]

    for c in range(3):
        expected += fakeimage[i, j, c]*w[c]

    expected = np.array(expected).astype("uint8")
    output = np.array(output).astype("uint8")
    output2 = np.array(output2).astype("uint8")
    output3 = output3.astype("uint8")

    numba = expected == output[i][j]
    python = expected == output2[i][j]
    numpy = expected == output3[i][j]
    str = '\n'
    str += f'expected {expected}\n'
    str += f'numba    {output[i][j]}\n'
    str += f'numpy    {output2[i][j]}\n'
    str += f'numpa    {output3[i][j]}\n'
    assert all([numba, python, numpy]), str


def test_sepiafilter2():
    # Test to check that the sepia filter works with sepia_effect

    fakeimage = np.random.randint(0, 256, size=(400, 600, 3))

    output = np.array(sepia.numba_color2sepia(fakeimage, sepia_effect=0.5))
    output2 = np.array(sepia.numpy_color2sepia(fakeimage, sepia_effect=0.5))
    output3 = np.array(sepia.numpy_color2sepia(fakeimage, sepia_effect=0.5))

    i = np.random.randint(0, 400)
    j = np.random.randint(0, 600)
    expected = [0]*3

    s = np.array([[0.393, 0.769, 0.189],
                  [0.349, 0.686, 0.168],
                  [0.272, 0.534, 0.131]])
    sepia_effect = 0.5
    I = np.identity(3)

    s = (1 - sepia_effect) * np.eye(3, 3) + (sepia_effect) * s

    expected = ((s @ fakeimage[i, j]) / np.sum(s[0])).astype("uint8")
    output = np.array(output).astype("uint8")
    output2 = np.array(output2).astype("uint8")
    output3 = output3.astype("uint8")

    numba = expected == output[i][j]
    python = expected == output2[i][j]
    numpy = expected == output3[i][j]

    str = '\n'
    str += f'expected {expected}\n'
    str += f'numba    {output[i][j]}\n'
    str += f'numpy    {output2[i][j]}\n'
    str += f'numpa    {output3[i][j]}\n'
    assert all(numba), str
    assert all(python), str
    assert all(numpy), str


test_grayfilter2()
test_sepiafilter2()
