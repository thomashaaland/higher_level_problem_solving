# -*- coding: utf-8 -*-
import numpy as np
import cv2
import timeit
from python_color2gray import python_color2gray

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
    grayscale_image_np = numpy_color2gray(image)
    print(f"Image {to_filename} (dimensions: (H, W, C) = {grayscale_image_np.shape}).")

    # write the image
    cv2.imwrite(to_filename, grayscale_image_np)

    # Perform benchmarking

    times = timeit.repeat(stmt='python_color2gray(image)',
                          setup="from __main__ import python_color2gray, image",
                          repeat = 5,
                          number = 5)

    times_np = timeit.repeat('numpy_color2gray(image)',
                             setup="from __main__ import numpy_color2gray, image",
                             repeat = 5,
                             number = 5)


    print("Writing report")

    # Write to file
    with open("numpy_report_color2gray.txt", "w") as f:
        f.write(
            f"""
Timing: numpy_color2gray
Average runtime running numpy_color2gray after 3 runs: {sum(times_np)/len(times_np):.4f} s
Average runtime running of numpy_color2gray is {(sum(times)/len(times))/(sum(times_np)/len(times_np)):.2f} times faster 
            than python_color2gray
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of grayscale image: {grayscale_image_np.shape}


            """)
