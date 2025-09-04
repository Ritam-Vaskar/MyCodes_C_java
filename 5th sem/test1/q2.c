//find the kth largest element in an array using quick sort algorithm
#include <stdio.h>
#include <stdlib.h>

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return i + 1;
}

int kthLargest(int arr[], int low, int high, int k) {
    if (k > 0 && k <= high - low + 1) {
        int index = partition(arr, low, high);
        if (index - low == k - 1)
            return arr[index];
        if (index - low > k - 1)
            return kthLargest(arr, low, index - 1, k);
        return kthLargest(arr, index + 1, high, k - index + low - 1);
    }
    return -1;  
}

int main() {
    int n, k;
    printf("Enter the number of elements: ");
    scanf("%d", &n);
    int arr[n];
    printf("Enter the elements: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    printf("Enter the value of k: ");
    scanf("%d", &k);
    int result = kthLargest(arr, 0, n - 1, n+1 -k);
    if (result != -1)
        printf("The %dth largest element is %d\n", k, result);
    else
        printf("Invalid input\n");
    return 0;
}