from tkinter import *
from tkinter import ttk
import random
import numpy as np
import time
import math



####   algorithms
def merge_sort(numbers, left, right):
    if (left < right):
        middle = (left + right) // 2

        merge_sort(numbers, left, middle)
        merge_sort(numbers, middle + 1, right)
        merge(numbers, left, middle, right)

def merge(numbers, left, middle, right):
    # define index iterators: 
    # left arr: [i,...,middle], right arr: [j,...,right]
    # working arr: [0,...,k,...,N-1]
    i = left
    j = middle + 1
    k = left

    # copy of the working array
    temp = numbers.copy()
    
    # iterate until one of the sides runs out of items
    while (i <= middle and j <= right):
        

        if (temp[i] <= temp[j]):
            numbers[k] = temp[i]
            
            i += 1
        else:
            numbers[k] = temp[j]
            
            j += 1

        k += 1
    
    #append remaining from left side
    while (i <= middle):

        numbers[k] = temp[i]
        
        k += 1
        i += 1

    #append remaining from right side
    while (j <= right):

        numbers[k] = temp[j]
        
        
        k += 1
        j += 1

#### Execution after this point

# Put in your own array
array = [5,4,3,2,1]




print(array)
merge_sort(array, 0, len(array)-1)
print(array)




