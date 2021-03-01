#include <stddef.h>

// Algorithm: Iterative Binary Search
// Overall Time Complexity: O(log n).
// Space Complexity: O(1).
// Author: https://www.linkedin.com/in/kilar.

int *binary_search(int value, const int *arr, size_t length) {
    int l = 0, r = length, m = (l + r) / 2;

    if(r == 0){
        return NULL;
    }

    while(l <= r && arr[m] != value) {
        if(value < arr[m]) {
            r = m - 1;
        } else {
            l = m + 1;
        }
        m = (l + r) / 2;
    }
    if(l <= r) {
        return (int *) &arr[m];
    } else {
        return NULL;
    }
}