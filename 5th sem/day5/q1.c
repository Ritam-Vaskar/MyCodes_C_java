#include <stdio.h>

void merge(int arr[], int temp[], int l, int m, int r, int *c) {
    int i = l, j = m + 1, k = l;

    while (i <= m && j <= r) {
        (*c)++;
        if (arr[i] <= arr[j])
            temp[k++] = arr[i++];
        else
            temp[k++] = arr[j++];
    }
    while (i <= m)
        temp[k++] = arr[i++];
    while (j <= r)
        temp[k++] = arr[j++];

    for (i = l; i <= r; i++)
        arr[i] = temp[i];
}

void mergeSort(int arr[], int temp[], int l, int r, int *c) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, temp, l, m, c);
        mergeSort(arr, temp, m + 1, r, c);
        merge(arr, temp, l, m, r, c);
    }
}

int main() {
    int n;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    int arr[n];
    int temp[n];

    printf("Enter the elements: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int comparisionCount = 0;
    mergeSort(arr, temp, 0, n - 1, &comparisionCount);

    printf("Number of comparisons: %d\n", comparisionCount);

    return 0;
}