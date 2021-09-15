# README.md Assignment3

## Task 3

### Prerequisites

To run the tests properly, use pytest. from `/array_pkg/` run `pip install .` to install. Then it should be possible to run py.test from `/array_pkg/` directory.

### Functionality

The Array class contained in `/array_pkg/Array/array.py` file functions similar to the numpy array in some respects. You can add, subtract, multiply and compare with other Arrays and numbers. You can print a 1d array, but other functions support an arbitrary number of dimensions.

### Missing Functionality

As of right now you cannot print higher dimensional arrays and the function to call elements are done with a syntax like `array[1,34]` as opposed to `array[1][34]`. This is because my implementation relies on contigous arrays and index arithmetics.

### Usage

To create a new array:
`Array((2,2), 1, 2, 3, 4)`
To add two arrays:
`array1 + array2`
This works for subtraction, multiplication and `==` operator as well.

To perform unittests run py.test from `array_pkg`.
