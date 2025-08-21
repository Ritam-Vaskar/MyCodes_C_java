#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_SIZE 1000

typedef struct {
    int steps;
    int comparisons;
    double time_taken;
} SortMetrics;

SortMetrics insertionSort(int arr[], int n) {
    int i, j, key;
    int steps = 0;
    int comparisons = 0;
    clock_t start, end;

    start = clock();

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

    end = clock();

    SortMetrics metrics;
    metrics.steps = steps;
    metrics.comparisons = comparisons;
    metrics.time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    return metrics;
}

int readFile(const char* filename, int arr[]) {
    FILE *fp = fopen(filename, "r");
    int n = 0;

    if (fp == NULL) {
        printf("Error opening file %s\n", filename);
        return -1;
    }

    while (fscanf(fp, "%d", &arr[n]) == 1 && n < MAX_SIZE) {
        n++;
    }

    fclose(fp);
    return n;
}

int main() {
    const char* files[] = {"random.txt", "random2.txt", "random3.txt"};
    int numFiles = 3;
    int arr[MAX_SIZE];
    SortMetrics total = {0, 0, 0};

    for (int i = 0; i < numFiles; i++) {
        int n = readFile(files[i], arr);
        if (n == -1) continue;

        printf("\nSorting %s (%d elements):\n", files[i], n);

        SortMetrics metrics = insertionSort(arr, n);

        printf("Steps: %d\n", metrics.steps);
        printf("Comparisons: %d\n", metrics.comparisons);
        printf("Time Taken: %.6f seconds\n", metrics.time_taken);

        total.steps += metrics.steps;
        total.comparisons += metrics.comparisons;
        total.time_taken += metrics.time_taken;

        // Write sorted output (optional)
        char outputFile[50];
        sprintf(outputFile, "sorted_%s", files[i]);
        FILE *out = fopen(outputFile, "w");
        for (int j = 0; j < n; j++) {
            fprintf(out, "%d\n", arr[j]);
        }
        fclose(out);
    }

    printf("\n--- Averages ---\n");
    printf("Average Steps: %d\n", total.steps / numFiles);
    printf("Average Comparisons: %d\n", total.comparisons / numFiles);
    printf("Average Time Taken: %.6f seconds\n", total.time_taken / numFiles);

    return 0;
}
