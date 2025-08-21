#include <stdio.h>

void quickSort(int arr[], int l, int r, int *c) {
    if (l < r) {
        int pivot = arr[r];
        int i = l - 1;

        for (int j = l; j < r; j++) {
            (*c)++;
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[r];
        arr[r] = temp;

        quickSort(arr, l, i, c);
        quickSort(arr, i + 2, r, c);
    }
}

int main() {
    int n;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    int arr[n];

    printf("Enter the elements: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int comparisionCount = 0;
    quickSort(arr, 0, n - 1, &comparisionCount);

    printf("Number of comparisons: %d\n", comparisionCount);

    return 0;
}