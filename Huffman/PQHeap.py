"""
File from previous part of project reused.
"""

# module exports are given below

class PQHeap:
    """
    Priority queue implemented with min-heap.
    Takes integer keys, and implements the following:
     - insert(key) in lg(n) time
     - extractMin() in lg(n) time
    
    Authors:
     - Kian Banke Larsen (kilar20)
     - Silas Pockendahl (silch20)
    """

    @staticmethod
    def createEmptyPQ():
        return PQHeap()

    def __init__(self):
        self._heap = []

    def insert(self, key):
        """
        Inserts key into priority queue

        Worst case time complexity: log(n)
        """
        self._heap.append(key)
        i = len(self._heap) - 1
        parent = ( i - 1 ) // 2

        # While min-heap property not satisfied ...
        while parent >= 0 and self._heap[parent] > self._heap[i]:
            self._swap(i, parent)
            i = parent
            parent = ( i - 1 ) // 2

    def extractMin(self):
        """
        Removes and returns minimum key
        Precondition: heap is non-empty

        Worst case time complexity: log(n)
        """
        key = self._heap[0]
        self._heap[0] = self._heap[-1]
        self._heap.pop()

        if len(self._heap):

            # sift head down, until min-heap property is restored
            i = 0 # current index
            while 1:

                minI, minKey = i, self._heap[i]

                # child indices
                left = i * 2 + 1
                right = left + 1

                if left < len(self._heap) and self._heap[left] < minKey:
                    minI, minKey = left, self._heap[left]

                if right < len(self._heap) and self._heap[right] < minKey:
                    minI, minKey = right, self._heap[right]

                if minI == i:
                    # heap property restored
                    break

                self._swap(i, minI)
                i = minI
        
        return key
    
    def _swap(self, i, j):
        """
        Swaps keys at ```i``` and ```j``` in _heap
        """
        self._heap[i], self._heap[j] = \
            self._heap[j], self._heap[i]

# required exports:

createEmptyPQ = PQHeap.createEmptyPQ
insert = PQHeap.insert
extractMin = PQHeap.extractMin