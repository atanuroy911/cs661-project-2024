# write a code to sum all the numbers in an array and return that value as output.
import math
def add(arr):
    sum = 0
    for i in arr:
        sum += i
    return sum
print("Sum is",add([1,2,3]))