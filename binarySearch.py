# Algorithm: Iterative Binary Search
# Overall Time Complexity: O(log n).
# Space Complexity: O(1).
# Author: https://www.linkedin.com/in/kilar.

def binarySearch(arr, key):
    r, l = len(arr) - 1, 0
    m = (1 + r) // 2

    if r == 0:
        return False
    
    while(l <= r and arr[m] != key):
        if key < arr[m]:
            r = m - 1
            
        else:
            l = m + 1
        m = (l + r) // 2
        
    if(l <= r):
        return True
    else:
        return False