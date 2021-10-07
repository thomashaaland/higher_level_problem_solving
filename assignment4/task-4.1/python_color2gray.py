# -*- coding: utf-8 -*-
import numpy as np
import cv2
import timeit

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
    
    return image

    
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
    grayscale_image = np.array(python_color2gray(image), dtype = "uint8")
    print(f"Image {to_filename} (dimensions: (H, W, C) = {grayscale_image.shape}).")

    # write the image
    cv2.imwrite(to_filename, grayscale_image)

    # Perform benchmarking

    times = timeit.repeat(stmt='python_color2gray(image)',
                          setup="from __main__ import python_color2gray, image",
                          repeat = 5,
                          number = 5)

    print("Writing report")

    # Write to file
    with open("python_report_color2gray.txt", "w") as f:
        f.write(
            f"""
Timing: python_color2gray
Average runtime running python_color2gray after 5 runs: {sum(times)/len(times):.2f} s
Timing performed using: timeit module
Dimensions of original image: {image.shape}
Dimensions of grayscale image: {grayscale_image.shape}
            """)
