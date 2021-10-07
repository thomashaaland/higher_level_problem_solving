import numpy as np
import timeit

def random_array(size, dim=3):
    """
    Generate a random array of size size and dimension dim
    """
    return np.random.rand(int(size), dim)


def loop(array):
    """
    Takes a numpy array and isolates all points that are within [0.52,0.6]
    for the first column and between [0.88,0.96] for the second column by
    looping through every point.
    """
    filtered_list = []
    for i in range(len(array)):
        # Check if the point is within the rectangle
        if ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.88)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.96)):
            filtered_list.append(array[i])
    return np.array(filtered_list)

def snake_loop(array):
    """
    Takes a numpy array and isolates all points in a given 
    range via array indexing by
    looping through every point.
    """
    filtered_list = []
    for i in range(len(array)):
        # Check if the point is within the rectangle
        if (((array[i][0] >= 0.16)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.24)
            and (array[i][1] <= 0.24))
            #2nd square
            or 
            ((array[i][0] >= 0.28)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.36)
            and (array[i][1] <= 0.24))
            #3nd square
            or ((array[i][0] >= 0.4)
            and (array[i][1] >= 0.16)
            and (array[i][0] <= 0.48)
            and (array[i][1] <= 0.24))
            #4th square
            or ((array[i][0] >= 0.4)
            and (array[i][1] >= 0.28)
            and (array[i][0] <= 0.48)
            and (array[i][1] <= 0.36))
            #5th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.28)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.36))
            #5th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.4)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.48))
            #6th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.52)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.6))
            
            #6th square
            or ((array[i][0] >= 0.52)
            and (array[i][1] >= 0.64)
            and (array[i][0] <= 0.6)
            and (array[i][1] <= 0.72))):
            filtered_list.append(array[i])
    return np.array(filtered_list)
# Generate a random array of size 1e5
array = random_array(1e5)
filtered_array = snake_loop(array)
filtered_array_snack = loop(array)

# Run timeit on the three functions we want to investigate
# The number of runs is 10
snake_loop = timeit.timeit('snake_loop(array)', number = 10,
                           globals = globals())
make_array = timeit.timeit('random_array(1e5)', number = 10,
                           globals = globals())
loop = timeit.timeit('loop(array)', number = 10,
                     globals = globals())

# Select the slowest part of the program
if make_array > max(snake_loop, loop):
    slowest = "make_array"
    slowest_time = make_array
else:
    if snake_loop > loop:
        slowest = "snake_loop"
        slowest_time = snake_loop
    else:
        slowest = "loop"
        slowest_time = loop


# Write to file
with open("timeit_report.txt", "w") as pf:
    pf.write(f"Timeit module\n")
    pf.write(f"Slowest times:\n")
    pf.write(f"Making array:  {make_array:.4f}s\n")
    pf.write(f"Snake loop:    {snake_loop:.4f}s\n")
    pf.write(f"Loop:          {loop:.4f}s\n")
    pf.write(f"\n{slowest} is slowest with time:  {slowest_time:.4f}s")


# Plot the results
import matplotlib.pyplot as plt

#if running in a jupyter notebook you might this inline
#matplotlib inline

plt.figure(figsize=(10, 10))
plt.title('Plot of Your Filters')
plt.plot(array[:, 0], array[:, 1], 'k.')
plt.plot(filtered_array[:, 0], filtered_array[:, 1], 'g.')
plt.plot(filtered_array_snack[:, 0], filtered_array_snack[:, 1], 'r.')
plt.show()
