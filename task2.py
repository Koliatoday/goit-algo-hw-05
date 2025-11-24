""" Binary search algorithm implementation. """

import random


def binary_search(arr, x):
    """
    Performs binary search to find the target value x in the sorted list arr.
    Args:
        arr (list): A sorted list to search.
        x (any): The target value to find.
    Returns:
        tuple: number of iterations performed, next element in arr after
               found element if found, otherwise -1
    """
    low = 0
    mid = 0
    n_iter = 0
    high = len(arr) - 1

    while low <= high:
        n_iter += 1
        mid = (high + low) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return n_iter, arr[mid+1] if mid < len(arr) - 1 else arr[mid]

    return n_iter, -1


data = sorted([random.uniform(0, 10) for _ in range(10)])
print(f"Random float data array: {data}")
print(f"Look for {data[0]}, get: {binary_search(data, data[0])}")
print(f"Look for {data[4]}, get: {binary_search(data, data[4])}")
print(f"Look for {data[9]}, get: {binary_search(data, data[9])}")
print(f"Look for {data[0]+1.23}, get: {binary_search(data, data[0]+1.23)}")
