#include <stdio.h>
#include <stdlib.h>

void sparseToTriplet(int **matrix, int rows, int cols, int *triplet[], int *nonZeroCount) {
    int count = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (matrix[i][j] != 0) {
                triplet[count][0] = i;
                triplet[count][1] = j;
                triplet[count][2] = matrix[i][j];
                count++;
            }
        }
    }
    *nonZeroCount = count;
}


void displayTriplet(int *triplet[], int nonZeroCount) {
    printf("Row\tColumn\tValue\n");
    for (int i = 0; i < nonZeroCount; i++) {
        printf("%d\t%d\t%d\n", triplet[i][0], triplet[i][1], triplet[i][2]);
    }
}


void addSparseMatrices(int *triplet1[], int nonZeroCount1, int *triplet2[], int nonZeroCount2, int *res[], int *resultNonZeroCount) {
    int i = 0, j = 0, k = 0;
    while (i < nonZeroCount1 && j < nonZeroCount2) {
        if (triplet1[i][0] < triplet2[j][0] || (triplet1[i][0] == triplet2[j][0] && triplet1[i][1] < triplet2[j][1])) {
            res[k][0] = triplet1[i][0];
            res[k][1] = triplet1[i][1];
            res[k][2] = triplet1[i][2];
            i++;
        } else if (triplet1[i][0] > triplet2[j][0] || (triplet1[i][0] == triplet2[j][0] && triplet1[i][1] > triplet2[j][1])) {
            res[k][0] = triplet2[j][0];
            res[k][1] = triplet2[j][1];
            res[k][2] = triplet2[j][2];
            j++;
        } else {
            res[k][0] = triplet1[i][0];
            res[k][1] = triplet1[i][1];
            res[k][2] = triplet1[i][2] + triplet2[j][2];
            i++;
            j++;
        }
        k++;
    }

    while (i < nonZeroCount1) {
        res[k][0] = triplet1[i][0];
        res[k][1] = triplet1[i][1];
        res[k][2] = triplet1[i][2];
        i++;
        k++;
    }

    while (j < nonZeroCount2) {
        res[k][0] = triplet2[j][0];
        res[k][1] = triplet2[j][1];
        res[k][2] = triplet2[j][2];
        j++;
        k++;
    }

    *resultNonZeroCount = k;
}

int main() {
    int rows, cols;

    // Enter the dimensions of the sparse matrices
    printf("Enter the number of rows: ");
    scanf("%d", &rows);
    printf("Enter the number of columns: ");
    scanf("%d", &cols);

    // Allocate memory for the sparse matrices
    int **matrix1 = (int **)malloc(rows * sizeof(int *));
    int **matrix2 = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        matrix1[i] = (int *)malloc(cols * sizeof(int));
        matrix2[i] = (int *)malloc(cols * sizeof(int));
    }


    printf("Enter the elements of the first sparse matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("Element at (%d, %d): ", i, j);
            scanf("%d", &matrix1[i][j]);
        }
    }


    printf("Enter the elements of the second sparse matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("Element at (%d, %d): ", i, j);
            scanf("%d", &matrix2[i][j]);
        }
    }


    int nonZeroCount1 = 0, nonZeroCount2 = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (matrix1[i][j] != 0) {
                nonZeroCount1++;
            }
            if (matrix2[i][j] != 0) {
                nonZeroCount2++;
            }
        }
    }


    int **triplet1 = (int **)malloc(nonZeroCount1 * sizeof(int *));
    int **triplet2 = (int **)malloc(nonZeroCount2 * sizeof(int *));
    for (int i = 0; i < nonZeroCount1; i++) {
        triplet1[i] = (int *)malloc(3 * sizeof(int));
    }
    for (int i = 0; i < nonZeroCount2; i++) {
        triplet2[i] = (int *)malloc(3 * sizeof(int));
    }


    sparseToTriplet(matrix1, rows, cols, triplet1, &nonZeroCount1);
    sparseToTriplet(matrix2, rows, cols, triplet2, &nonZeroCount2);

    int maxNonZeroCount = nonZeroCount1 + nonZeroCount2;
    int **res = (int **)malloc(maxNonZeroCount * sizeof(int *));
    for (int i = 0; i < maxNonZeroCount; i++) {
        res[i] = (int *)malloc(3 * sizeof(int));
    }


    int resultNonZeroCount;
    addSparseMatrices(triplet1, nonZeroCount1, triplet2, nonZeroCount2, res, &resultNonZeroCount);


    printf("Resultant triplet form after addition:\n");
    displayTriplet(res, resultNonZeroCount);


    for (int i = 0; i < rows; i++) {
        free(matrix1[i]);
        free(matrix2[i]);
    }
    free(matrix1);
    free(matrix2);

    for (int i = 0; i < nonZeroCount1; i++) {
        free(triplet1[i]);
    }
    free(triplet1);

    for (int i = 0; i < nonZeroCount2; i++) {
        free(triplet2[i]);
    }
    free(triplet2);

    for (int i = 0; i < maxNonZeroCount; i++) {
        free(res[i]);
    }
    free(res);

    return 0;
}
