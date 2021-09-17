class Array:

    def __init__(self, shape, *values):
        """
        
        Initialize an array of 1-dimensionality. Elements can only be of type:
        - int
        - float
        - bool
        
        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.

        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """
        
        # Check that the shape is valid
        if not isinstance(shape, tuple):
            raise ValueError("The shape needs to ba a tuple")
        
        # Check if the values are of valid type
        for val in values:
            if not isinstance(val, (int, float, bool)):
                raise ValueError("This array only accepts int, float or bool datatypes")
        
        # Check that the number of arguments provided matches the shape
        totalLength = 1
        for arg in shape:
            totalLength *= arg
        if not totalLength == len(values):
            raise ValueError("The shape does not match the number of arguments")
        
        # Optional: If not all values are of same type, all are converted to floats.
        self._num_dims = len(shape)
        self._shape = shape
        self._datatype = type(values[0])
        for val in values:
            if self._datatype != val.__class__:
                self._arr = [float(e) for e in values]
                self._datatype = type(self._arr[0])
            else:
                self._arr = [e for e in values]

    
    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            str: A string representation of the array.

        """
        def iterate_over_i(dims, arr):
            arr_str = "["
            if len(dims) > 1:
                for i in range(dims[0]-1):
                    arr_str += iterate_over_i(dims[1:], Array(dims[1:], *(arr[i]._arr))) + ", "
                arr_str += iterate_over_i(dims[1:], Array(dims[1:], *(arr[i+1]._arr)))
            else:
                for i in range(dims[0]-1):
                    arr_str += str(arr[i]) + ", "
                arr_str += str(arr[i+1])
            return arr_str + "]"

        return iterate_over_i(self._shape, self)
    
        
    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        
        # check that the method supports the given arguments (check for data type and shape of array) 

        if not isinstance(other, (self.__class__, int, float)):
            return NotImplemented
        
        if isinstance(other, (int, float)):
            return Array(self._shape, *[a + other for a in self._arr])
            
        if self._datatype == bool:
            return NotImplemented

        if self._shape != other._shape:
            return NotImplemented
        
        return Array(self._shape, *[a + b for a, b in zip(self._arr, other._arr)])
        
        
        

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)
        

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if not isinstance(other, (self.__class__, int, float)):
            return NotImplemented
        
        if isinstance(other, (int, float)):
            return Array(self._shape, *[a - other for a in self._arr])
            
        if self._datatype == bool:
            return NotImplemented

        if self._shape != other._shape:
            return NotImplemented
        
        return Array(self._shape, *[a - b for a, b in zip(self._arr, other._arr)])
    
    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        # For subtraction we need to factor out the negative to make it
        # equivalent to __sub__ method
        return self.__sub__(other) * -1

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if not isinstance(other, (self.__class__, int, float)):
            return NotImplemented
        
        if isinstance(other, (int, float)):
            return Array(self._shape, *[a * other for a in self._arr])
            
        if self._datatype == bool:
            return NotImplemented

        if self._shape != other._shape:
            return NotImplemented
        
        return Array(self._shape, *[a * b for a, b in zip(self._arr, other._arr)])
    
    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        # Hint: this solution/logic applies for all r-methods
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if not isinstance(other, self.__class__):
            return False
        if self._shape == other._shape:
            return True
        return False

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        
        if not isinstance(other, self.__class__) and isinstance(other, (int, float, bool)):
            return Array(self._shape, *[a == other for a in self._arr])
        if isinstance(other, self.__class__):
            if self._shape != other._shape:
                raise ValueError("Shape does not match")
            return Array(self._shape, *[a == b for a, b in zip(self._arr, other._arr)])
        return TypeError
        

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """
        if self._datatype != bool:
            return float(min(self._arr))
        raise ValueError("There is no minimum element for a boolean array")

    def __getitem__(self, *indices):
        """Returns the value in the index place.

        Returns:
            float: The value of the element in the index place
         
        Raises:
            IndexOutOfBoundsError: if the index is out of bounds.
        """
        
        # Special case for single input index
        if isinstance(*indices, int):
            i = indices[0]
            if i > self._shape[0]:
                raise IndexError("Index out of range")
            if len(self._shape) == 1:
                return float(self._arr[i])
            else:
                top_dim = self._shape[0]
                rest_dim = self._shape[1:]
                dim_jump = 1
                for arg in rest_dim:
                    dim_jump *= arg

                start_i = dim_jump * i
                end_i = start_i + dim_jump
                return Array(rest_dim, *self._arr[start_i : end_i])
        

        # Otherwise
        indices = indices[0]
        if len(self._shape) != len(indices):
            raise IndexError("Shape does not match")
        for shape_ind, access_ind in zip(self._shape, indices):
            if shape_ind <= access_ind:
                raise IndexError("Index out of bounds")

        # for 2d: assume 3x4: fetch 2,3: 2*3 + 3
        # for n, m: fetch element a, b: n*a + b
        # Implement for contigous list:
        """ [[0, 1, 2],
             [3, 4, 5]]
              ->
            [0, 1, 2, 3, 4, 5]
        """
        i = 0
        # Strategy: First index shows number of traverses across all other indexes
        # next index shows total traverses in similar manner. Relies on contigous lists
        for dim in range(1, len(self._shape)):
            cumdims = 1
            for lowdims in self._shape[dim:]:
                cumdims *= lowdims
            i += indices[dim-1]*cumdims
        i += indices[-1]
            
        return float(self._arr[i])
