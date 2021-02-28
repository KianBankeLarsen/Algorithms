import math

# Algorithm: Merge k sorted arrays of n digits.
# Overall Time Complexity: O(n * k * log k)
# Space Complexity: if output is not stored O(k), else O(k * n)
# Author: https://www.linkedin.com/in/kilar

class HeapNode:

    def __init__(self, value, listIndex, valueIndex):
        self.value = value
        self.listIndex = listIndex
        self.valueIndex = valueIndex


def initMinHeap(A, heapSize, l = []):
    for i in range(len(A)):
        l.append(HeapNode(A[i][0], i, 0))

    buildMinHeap(l, heapSize)

    return l


def buildMinHeap(A, heapSize):
    for i in range((heapSize - 1) // 2, -1, -1):
        minHeapify(A, i, heapSize)


def minHeapify(A, i, heapSize):
    l = 2 * i + 1
    r = 2 * i + 2

    if l <= heapSize and A[l].value < A[i].value:
        smallest = l
    else:
        smallest = i
    if r <= heapSize and A[r].value < A[smallest].value:
        smallest = r 
    if smallest != i:
        swap(A, i, smallest)
        minHeapify(A, smallest, heapSize)


def swap(A, n, m):
    A[m], A[n] = A[n], A[m]


def extractMin(A, orgA, heapSize):
    minNode = A[0]
    min = minNode.value

    if minNode.valueIndex < len(orgA[minNode.listIndex]) - 1:
        minNode.valueIndex += 1
        minNode.value = orgA[minNode.listIndex][minNode.valueIndex]
        minHeapify(A, 0, heapSize)
    else:
        A[0].value = math.inf
        swap(A, 0, heapSize)
        minHeapify(A, 0, heapSize)
        heapSize -= 1

    return min, heapSize


def main(A, res = []):
    heapSize = len(A) - 1
    l = initMinHeap(A, heapSize)

    while (heapSize >= 0):
        min, heapSize = extractMin(l, A, heapSize)
        res.append(min)

    return res


A = [[2, 4, 7, 9, 14],
    [16, 34, 67, 70],
    [700, 800, 850, 2322],
    [100, 123, 234, 678], 
    [124, 432, 765, 7544, 34345],
    [1, 2, 3, 222, 223, 543],
    [1, 11, 22, 44, 87, 111, 1111]]

print(main(A))