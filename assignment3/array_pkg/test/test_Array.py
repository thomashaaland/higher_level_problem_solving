from Array.array import Array

def test_make_array():
    #Test to check if Array can make arrays.
    shape = (4,)
    Array(shape, 1, 2, 3, 4)
    Array(shape, 1., 2., 3., 4.)
    Array(shape, True, False, True, False)
    Array(shape, 1, 2, 3., False)

    # Check to see if the Array throws an exception if called wrong
    try:
        Array(1, 2, 3, 4)
    except ValueError:
        print("Approved")
    else:
        raise AssertionError("Non-tuple accepted as a tuple")

    try:
        Array(shape, 1, 2, "car", [])
    except ValueError:
        print("Approved")
    else:
        raise AssertionError("String accecpted as argument in Array")
    
    try:
        Array(shape, 1, 2)
    except ValueError:
        print("Approved")
    else:
        raise AssertionError("Shape and number of arguments do not match!")
    
def test_str():
    # Test to see if the output is good for a 1d array
    arr1 = Array((4,), 1, 2, 3, 4)
    assert arr1.__str__() == "[1, 2, 3, 4]"
    
def test_getitem_1d():
    # Test to see if we can get an item from a 1d array
    shape = (4,)
    arr = Array(shape, 1, 2, 3, 4)
    assert arr[0] == 1
    assert arr[1] == 2
    assert arr[2] == 3
    assert arr[3] == 4

def test_getitem_2d():
    # test to see if we can get an item from a 2d array
    shape = (3,2)
    arr = Array(shape, 1, 2, 3, 4, 5, 6)
    assert arr[0,0] == 1
    assert arr[0,1] == 2
    assert arr[1,0] == 3
    assert arr[1,1] == 4
    assert arr[2,0] == 5
    assert arr[2,1] == 6

    shape = (2,3)
    arr = Array(shape, 1, 2, 3, 4, 5, 6)
    assert arr[0,0] == 1
    assert arr[0,1] == 2
    assert arr[0,2] == 3
    assert arr[1,0] == 4
    assert arr[1,1] == 5
    assert arr[1,2] == 6

def test_getitem_3d():
    # test to see if we can get items from an 3d array
    shape = (2,2,2)
    arr = Array(shape, 1, 2, 3, 4, 5, 6, 7, 8)
    val = 1
    for i in [0,1]:
        for j in [0,1]:
            for k in [0,1]:
                assert arr[i,j,k] == val
                val += 1

def test_getitem_nd():
    # test to see if we can get items from an nd array
    shape = (5,6,9,12)
    arr = Array(shape, *[i for i in range(1, (5*6*9*12)+1)])
    val = 1
    for i in range(shape[0]):
        for j in range(shape[1]):
            for k in range(shape[2]):
                for l in range(shape[3]):
                    assert arr[i,j,k,l] == val
                    val += 1
                
def test_add_arrays():
    # test to see if we can add properly with arrays or numbers
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 + arr2)._arr == [5, 5, 5, 5]
    assert (arr2 + arr1)._arr == [5, 5, 5, 5]
    assert (arr1 + 1)._arr == [2, 3, 4, 5]
    assert (arr1 + 0.5)._arr == [1.5, 2.5, 3.5, 4.5]
    assert (arr1 + (-1))._arr == [0, 1, 2, 3]
    try:
        arr1 + "teddybear"
        arr1 + arr3
        arr1 + arr4
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

def test_add_2d_arrays():
    # test to see if we can add properly with arrays or numbers
    shape = (2,2)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 + arr2)._arr == [5, 5, 5, 5]
    assert (arr2 + arr1)._arr == [5, 5, 5, 5]
    assert (arr1 + 1)._arr == [2, 3, 4, 5]
    assert (arr1 + 0.5)._arr == [1.5, 2.5, 3.5, 4.5]
    assert (arr1 + (-1))._arr == [0, 1, 2, 3]
    try:
        arr1 + "teddybear"
        arr1 + arr3
        arr1 + arr4
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

    
def test_radd_arrays():
    # test to see if we can add if the Array comes from the right
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 + arr2)._arr == [5, 5, 5, 5]
    assert (arr2 + arr1)._arr == [5, 5, 5, 5]
    assert (1 + arr1)._arr == [2, 3, 4, 5]
    assert (0.5 + arr1)._arr == [1.5, 2.5, 3.5, 4.5]
    assert (-1 + arr1)._arr == [0, 1, 2, 3]
    try:
        "teddybear" + arr1
        arr3 + arr1
        arr4 + arr1
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

def test_sub_arrays():
    # test to see if we can subtract
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 - arr2)._arr == [-3, -1, 1, 3]
    assert (arr2 - arr1)._arr == [3, 1, -1, -3]
    assert (arr1 - 1)._arr == [0, 1, 2, 3]
    assert (arr1 - 0.5)._arr == [0.5, 1.5, 2.5, 3.5]
    assert (arr1 - (-1))._arr == [2, 3, 4, 5]
    try:
        arr1 - "teddybear"
        arr1 - arr3
        arr1 - arr4
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

def test_rsub_arrays():
    # test to see if we can subtract when array comes from the left
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 - arr2)._arr == [-3, -1, 1, 3]
    assert (arr2 - arr1)._arr == [3, 1, -1, -3]
    assert (1 - arr1)._arr == [0, -1, -2, -3]
    assert (0.5 - arr1)._arr == [-0.5, -1.5, -2.5, -3.5]
    assert (-1 - arr1)._arr == [-2, -3, -4, -5]
    try:
        "teddybear" - arr1
        arr3 - arr1
        arr4 - arr1
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

def test_mul_arrays():
    # test to see if we can multiply
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 * arr2)._arr == [4, 6, 6, 4]
    assert (arr2 * arr1)._arr == [4, 6, 6, 4]
    assert (arr1 * 1)._arr == [1, 2, 3, 4]
    assert (arr1 * 0.5)._arr == [0.5, 1., 1.5, 2.]
    assert (arr1 * (-1))._arr == [-1, -2, -3, -4]
    try:
        arr1 * "teddybear"
        arr1 * arr3
        arr1 * arr4
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")

def test_rmul_arrays():
    # test to see if we can multiply when the array comes from the right
    shape = (4,)
    arr1 = Array(shape, 1, 2, 3, 4)
    arr2 = Array(shape, 4, 3, 2, 1)
    arr3 = Array(shape, True, True, False, False)
    arr4 = Array((2,), 1, 2)
    assert (arr1 * arr2)._arr == [4, 6, 6, 4]
    assert (arr2 * arr1)._arr == [4, 6, 6, 4]
    assert (1 * arr1)._arr == [1, 2, 3, 4]
    assert (0.5 * arr1)._arr == [0.5, 1., 1.5, 2.]
    assert (-1 * arr1)._arr == [-1, -2, -3, -4]
    try:
        "teddybear" * arr1
        arr3 * arr1
        arr4 * arr1
    except TypeError:
        print("NotImplemented test passed")
    else:
        raise AssertionError("Functionality not implemented")


def test_equality():
    # test to see if the == operator works properly
    arr1 = Array((4,), 1, 2, 3, 4)
    arr2 = Array((4,), 1, 2, 3, 4)
    arr3 = Array((2,2), 1, 2, 3, 4)
    arr4 = Array((4,), 4, 3, 2, 1)
    assert (arr1 == arr2) == True
    assert (arr1 == arr3) == False
    assert (arr1 == arr4) == True
    assert (arr1 == 4) == False
    assert (arr1 == "teddybear") == False

def test_equal():
    # test to see if the is_equal method works properly
    arr1 = Array((4,), 1, 2, 3, 4)
    arr2 = Array((4,), 0, 2, 4, 4)
    arr3 = Array((2,), 0, 2)
    assert arr1.is_equal(arr2)._arr == [False, True, False, True]
    assert arr1.is_equal(1)._arr == [True, False, False, False]
    assert arr1.is_equal("Hamster") == TypeError
    
    try:
        arr1.is_equal(arr3)
    except ValueError:
        print("Passed equality test")
    else:
        raise AssertionError("Equality performed when shape does not match")
    
def test_min_element():
    # test to see if we can find the smallest element properly
    arr1 = Array((4,), 1, 2, 3, 4)
    arr2 = Array((4,), 4, 1, 2, 3)
    arr3 = Array((4,), 3, 4, 1, 2)
    arr4 = Array((4,), 2, 3, 4, 1)
    assert arr1.min_element() == 1
    assert arr2.min_element() == 1
    assert arr3.min_element() == 1
    assert arr4.min_element() == 1
    try:
        Array((1,), True).min_element()
    except ValueError:
        print("Passed boolean minimum test")
    else:
        raise AssertionError("The test for minimum boolean arrays failed.")
