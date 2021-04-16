# Algorithm: Longest monotonic subsequence
# Overall Time Complexity: O(n^2).
# Space Complexity: O(n).
# Author: https://www.linkedin.com/in/kilar.

def monotonic_subsequence(arr):
    Dict = {}
    maximum = 0

    for i in range(len(arr)):

        Dict[i] = [arr[i]]

        for j in range(i + 1, len(arr)):
            if arr[j] >= Dict[i][-1]:
                Dict[i].append(arr[j])

        for m in Dict:
            temp = maximum
            maximum = max(maximum, len(Dict[m]))

            if temp < maximum:
                key = m

    return Dict[key]
