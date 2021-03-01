import math

# Algorithm: Merge k sorted arrays of n numbers.
# Overall Time Complexity: O(nk * log k).
# Space Complexity: O(1).
# Author: https://www.linkedin.com/in/kilar.

class HeapNode:

    def __init__(self, value, listIndex, valueIndex):
        self.value = value
        self.listIndex = listIndex
        self.valueIndex = valueIndex


def buildMinHeap(A, heapSize):
    for i in range(len(A)):
        nodeObj = HeapNode(A[i][0], i, 0)
        A[i][0] = nodeObj

    for i in range((heapSize - 1) // 2, -1, -1):
        minHeapify(A, i, heapSize)


def minHeapify(A, i, heapSize):
    l = 2 * i + 1
    r = 2 * i + 2

    if l <= heapSize and A[l][0].value < A[i][0].value:
        smallest = l
    else:
        smallest = i
    if r <= heapSize and A[r][0].value < A[smallest][0].value:
        smallest = r 
    if smallest != i:
        swap(A, i, smallest)
        minHeapify(A, smallest, heapSize)


def swap(A, n, m):
    A[m][0].listIndex, A[n][0].listIndex = A[n][0].listIndex, A[m][0].listIndex 
    A[m], A[n] = A[n], A[m]


def extractMin(A, heapSize):
    minNode = A[0][0]
    min = minNode.value

    if minNode.valueIndex < len(A[minNode.listIndex]) - 1:
        minNode.valueIndex += 1
        minNode.value = A[minNode.listIndex][minNode.valueIndex]
        minHeapify(A, 0, heapSize)
    else:
        minNode.value = math.inf
        swap(A, 0, heapSize)
        minHeapify(A, 0, heapSize)
        heapSize -= 1

    return min, heapSize


def main(A, res = []):
    heapSize = len(A) - 1
    buildMinHeap(A, heapSize)

    while (heapSize >= 0):
        min, heapSize = extractMin(A, heapSize)
        res.append(min)

    return res

# Demonstration of I/O
A = [[2, 4, 7, 9, 14],
    [16, 34, 67, 70],
    [700, 800, 850, 2322],
    [100, 123, 234, 678], 
    [124, 432, 765, 7544, 34345],
    [1, 2, 3, 222, 223, 543],
    [0.5, 1, 2.5, 11, 22, 44, 87, 111, 849, 1111]]

print(main(A))
