//you are given an array A[1...n] of n numbers which is bitonic (first increasing then decreasing).sort the array in ascending order in O(n) time
#include <stdio.h>
int findPeak(int A[], int n) {
    int low = 0, high = n - 1;
    while (low < high) {
        int mid = (low + high) / 2;
        if (A[mid] < A[mid + 1])
            low = mid + 1;
        else
            high = mid;
    }
    return low;
}


void reverse(int A[], int low, int high) {
    while (low < high) {
        int temp = A[low];
        A[low] = A[high];
        A[high] = temp;
        low++;
        high--;
    }
}


void merge(int A[], int low, int mid, int high) {
    int n1 = mid - low + 1;
    int n2 = high - mid;
    int L[n1], R[n2];
    for (int i = 0; i < n1; i++)
        L[i] = A[low + i];
    for (int j = 0; j < n2; j++)
        R[j] = A[mid + 1 + j];
    int i = 0, j = 0, k = low;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            A[k] = L[i];
            i++;
        } else {
            A[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        A[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        A[k] = R[j];
        j++;
        k++;
    }
}


void sortBitonicArray(int A[], int n) {
    int peak = findPeak(A, n);
    reverse(A, peak + 1, n - 1);
    merge(A, 0, peak, n - 1);
}


int main() {
    int A[] = {1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1};
    int n = sizeof(A) / sizeof(A[0]);
    printf("Original array: ");
    for(int i=0;i<n;i++){
        printf("%d ",A[i]);
    }
    sortBitonicArray(A, n);
    printf("\nSorted array: ");
    for (int i = 0; i < n; i++)
        printf("%d ", A[i]);
    
    return 0;
}