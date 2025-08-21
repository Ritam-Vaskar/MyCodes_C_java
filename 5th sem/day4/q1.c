//max and min in array using recursion
#include <stdio.h>
#include <limits.h>
int findMax(int arr[], int n) {
    if (n == 1)
        return arr[0];
    return (arr[n - 1] > findMax(arr, n - 1)) ? arr[n - 1] : findMax(arr, n - 1);
}

int findMin(int arr[], int n) {
    if (n == 1)
        return arr[0];
    return (arr[n - 1] < findMin(arr, n - 1)) ? arr[n - 1] : findMin(arr, n - 1);
}

int main(){
    int n;
    printf("Enter the size of the array: ");
    scanf("%d", &n);

    int arr[n];
    printf("Enter the elements of the array:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int maxElement = findMax(arr, n);
    int minElement = findMin(arr, n);
    printf("Minimum element in the array: %d\n", minElement);
    printf("Maximum element in the array: %d\n", maxElement);

    return 0;
}