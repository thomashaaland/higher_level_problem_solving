# README.md Assignment4

## Task 4

### Prerequisites

The instapy package requires numpy, numba, matplotlib, opencv and python 3.9.7. For a comprehensive list of requirements consult the `requirements.txt` file in the `./instapy/` directory.

### Functionality

The instapy package is located in the `/instapy/` directory. In the `task-x` directories are preliminary tasks solved. These are python scripts and generate the `*_report.txt` files. The instapy package is located in the `instapy` directory from root. This package can apply a stepless sepia filter, a grayscale filter and supports resize. You can always resize and you can turn on either or both filters. So, if you only apply scaling you get a rescaled image. If you switch on either sepia or grayscale you get a sepia or grayscale image and if you switch on both you get both. If you apply scaling and filters you only get a scaled and filtered image, not just a scaled image. The sepia filter is stepless so you can control how much sepia you want to add. You can also select the implementation which is pure python, numpy or numba. Finally, you can write to a custom filename and location or the program will write a file with the process appended (ie. "{filename}_sepia.jpg" if sepia filter has been applied).

### Missing Functionality

I have not implemented cython everywhere.

### Usage

Make the package globally accessible by running `pip install .` from `/instapy/` directory.
You are now ready to use the instapy package.

You can now use the instapy command directly from the terminal. To get started type instapy in the terminal.
```bash
$ instapy
usage: instapy [-h] -f FILE [-se] [-st STEPLESS_SEPIA] [-g] [-sc SCALE] [-i {python,numpy,numba}] [-o OUT]
instapy: error: the following arguments are required: -f/--file
```

To get a short description of how instapy works you can get help with the `--help` flag, or `-h` for short. 

```bash
$ instapy -h

usage: instapy [-h] -f FILE [-se] [-st STEPLESS_SEPIA] [-g] [-sc SCALE] [-i {python,numpy,numba}] [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The filename of the file to apply the filter to.
  -se, --sepia          Select the sepia filter
  -st STEPLESS_SEPIA, --stepless_sepia STEPLESS_SEPIA
                        Include this to choose amount of sepia applied. Between 0 and 1.
  -g, --gray            Select the gray filter
  -sc SCALE, --scale SCALE
                        Scale factor to resize the image
  -i {python,numpy,numba}, --implement {python,numpy,numba}
                        Choose the implementation.
  -o OUT, --out OUT     The output filename. If this is not specified a new file is saved at the same location as {filename}_filter.jpg
```

The quickest way to get started is to provide a file to apply a filter and the filter.

```bash
$ instapy -f testImage.jpg -se
Writing file testImage_sepia.jpg to disk
Done
```

### Options:
* -h, --help
Using this flag gives a short description of the available flags and how to use them.
* -f, FILE --file FILE
After this flag include the path and name of the file you want to apply a filter to.
* -se, --sepia
This is a switch which lets you turn on the sepia filter. Including this flag writes a new image with the sepia filter applied.
* -st STEPLESS_SEPIA, --stepless_sepia STEPLESS_SEPIA
Including this flag and a value between 0 and 1 applies the sepia filter partly. A value of 0 applies no sepia filter, while a value of 1 applies it completely.
* -g, --gray
This switch turns grayscale filter on.
* -sc SCALE, --scale SCALE
Using this rescales the image.
* At least one of the flags sepia, grayscale or scale is required. 
* -i IMPLEMENT, --implement IMPLEMENT
Let's the user choose which implementation to use. It is possible to choose between python, numpy and numba implementations.
* -o OUT, --out OUT
If you choose to include custom names you must include as many names as there are output files. If you only apply scaling you need one name. If you apply either sepia or grayscale filter you need one name. If you apply both sepia and grayscale you need two names. You need at most two names.

To import the module in a python project you can do so with
`import instapy.grayscale_image as c2g` for grayscale functionality and
`import instapy.sepia_image as c2s` for sepia functionality.

Now you can call specific functions such as
```python
import instapy.sepia_image as c2s
im2sepia = c2s.python_color2sepia

with open("filename") as f:
     sepia_image = im2sepia(f)
```

The functions `sepia_image` and `grayscale_image` is used to collect most functionality. These functions resizes the image, applies relevant filter and writes the image to disk.

The required arguments are
* `input_filename`
The filename to apply the filter to goes here.
* `output_filename`
If no argument is provided the program uses the input filename and appends a description. For instance "rain.jpg" becomes "rain_sepia.jpg".
* `implementation`
Choose which implementation you want to try. Numpy is default.
* `scale`
Provide a scale factor if you want to scale the image.
* `sepia_effect`
When applying a sepia filter you can choose to apply the filter partly.

```python
sepia_image(input_filename, output_filename=None,
            implementation="numpy", scale = 1, sepia_effect = 1)
```

```python
grayscale_image(input_filename, output_filename=None,
            implementation="numpy", scale = 1, sepia_effect = 1)
```

The implementations are identical, but sepia_effect is redundant in grayscale and does nothing there.

To perform unittests run py.test from `instapy` root.
