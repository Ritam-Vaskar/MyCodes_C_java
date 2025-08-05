#include <stdio.h>

void insertionSort(int arr[], int n) {
    int i, j, key;
    int steps = 0;
    int comparisons = 0;

    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;

        while (j >= 0 && arr[j] > key) {
            comparisons++; 
            arr[j + 1] = arr[j];
            j--;
            steps++;
        }

        comparisons++; 
        arr[j + 1] = key;
        steps++;
    }

    printf("Sorted array: ");
    for (i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    printf("Number of steps: %d\n", steps);
    printf("Number of comparisons: %d\n", comparisons);
}

int main() {
    FILE *fp;
    int arr[100]; 
    int n = 0;

    fp = fopen("random.txt", "r");
    if (fp == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    while (fscanf(fp, "%d", &arr[n]) == 1) {
        n++;
    }

    fclose(fp);

    insertionSort(arr, n);

    return 0;
}