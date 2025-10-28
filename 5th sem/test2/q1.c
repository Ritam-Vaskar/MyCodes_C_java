#include <stdio.h>
#include <stdlib.h>

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}


int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] >= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

int quickSelect(int arr[], int low, int high, int k) {
    if (low == high) {
        return arr[low];
    }
    
    int pivotIndex = partition(arr, low, high);
    
    if (pivotIndex == k - 1) {
        return arr[pivotIndex];
    }
    else if (pivotIndex > k - 1) {
        return quickSelect(arr, low, pivotIndex - 1, k);
    }
    else {
        return quickSelect(arr, pivotIndex + 1, high, k);
    }
}

int findKthLargest(int arr[], int n, int k) {
    if (k < 1 || k > n) {
        printf("Invalid k value. k should be between 1 and %d\n", n);
        return -1;
    }
    
    return quickSelect(arr, 0, n - 1, k);
}

int main() {
    int n, k;
    
    printf("Enter the size of array: ");
    scanf("%d", &n);
    
    int arr[n];
    printf("Enter %d elements: ", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    
    printf("Enter k (to find kth largest element): ");
    scanf("%d", &k);
    
    int result = findKthLargest(arr, n, k);
    
    if (result != -1) {
        printf("The %d%s largest element is: %d\n", k, 
               (k == 1) ? "st" : (k == 2) ? "nd" : (k == 3) ? "rd" : "th", result);
    }
    
    printf("\nArray after partitioning: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    
    return 0;
}