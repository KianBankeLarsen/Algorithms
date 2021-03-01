# Algorithm: Check if a pair in a given sorted array, evaluates to a certain sum when added.
# Overall Time Complexity: O(n).
# Space Complexity: O(n).
# Author: https://www.linkedin.com/in/kilar.

def sumInList(arr, key, k = 0):
    arrLength = len(arr)

    for i in range(arrLength):
        if arr[k] + arr[i] == key:
            return True, "{} + {} = key".format(arr[k], arr[i])

        elif i < arrLength - 1:
            if arr[k + 1] + arr[i + 1] > key:
                continue
            else: 
                k += 1

    return False, "No pair sums to key"