# Algorithm: Count inversions in an array.
# Overall Time Complexity: O(n log n).
# Space Complexity: O(n).
# Author: https://www.linkedin.com/in/kilar.

def invCount(arr, inv = 0):
    if len(arr) > 1:
 
        mid = len(arr) // 2
 
        L = arr[:mid]
        R = arr[mid:]
 
        inv += mergeSort(L)
        inv += mergeSort(R)
 
        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
                inv += mid - i
            k += 1
 
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
        
    return inv