# README.md Assignment3

## Task 3

### Prerequisites

To run the tests properly, use pytest. from `/array_pkg/` run `pip install .` to install. Then it should be possible to run py.test from `/array_pkg/` directory. The Array package relies on the listed requirements in requirements.txt found in array_pkg directory.

### Functionality

The Array class contained in `/array_pkg/Array/array.py` file functions similar to the numpy array in some respects. You can add, subtract, multiply and compare with other Arrays and numbers. You can print any array of any dimension. The underlying datastructure is the list native to python and tuple containing the dimension information. The list is contigous and not nested, a choice made for performance reasons (in theory, it's not performance tested against nested lists. It should be easily ported to C style contigous arrays). 

### Missing Functionality

None that I know of.

### Usage

Make the package globally accessible by running `pip install .` from `/array_pkg/` directory.
To import in a python project import using
`from Array.array import Array`
You are now ready to use the Array class.
To create a new array:
`A = Array((2,2), 1, 2, 3, 4)`
To add two arrays:
`array1 + array2`
This works for subtraction, multiplication and `==` operator as well.
You can call an element from the array with indices. For example:
```
from Array.array import Array
A = Array((2,), 1 2)
A[0] # returns 1
A[1] # returns 2

B = Array((2,2), 1, 2, 3, 4)
print(B[0])
# > [1, 2]

C = Array((2,2,2), *range(1, 9))
print(C[0])
# > [[1, 2], [3, 4]]
```

You can access an element using both indices in tuples an access one sub array at a time
```
from Array.array import Array
C = Array((2,2,2), *range(1,9))
C[0,0,0] # returns 1
C[0,0,1] # returns 2

C[0][0][0] # returns 1
C[0][0][1] # returns 2
```


To perform unittests run py.test from `array_pkg`.
