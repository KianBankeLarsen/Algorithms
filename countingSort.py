# Algorithm: Counting Sort
# Overall Time Complexity: O(n + k).
# Space Complexity: O(n + k).
# Author: https://www.linkedin.com/in/kilar.

def counting_sort(int A, int k):
    C = [0]*(k + 1)
    B = [0]*len(A)

    for j in A:
        C[j] += 1
    
    cdef int cum_sum = 0
    for i in range(0, k + 1):
        C[i] += cum_sum
        cum_sum = C[i]

    for j in range(len(A) -1, -1, -1):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] = C[A[j]] - 1

    return B
