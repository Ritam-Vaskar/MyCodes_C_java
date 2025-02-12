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

int main() {
    int rows, cols;


    printf("Enter the number of rows: ");
    scanf("%d", &rows);
    printf("Enter the number of columns: ");
    scanf("%d", &cols);


    int **matrix = (int **)malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int *)malloc(cols * sizeof(int));
    }


    printf("Enter the elements of the sparse matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("Element at (%d, %d): ", i, j);
            scanf("%d", &matrix[i][j]);
        }
    }


    int nonZeroCount = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (matrix[i][j] != 0) {
                nonZeroCount++;
            }
        }
    }


    int **triplet = (int **)malloc(nonZeroCount * sizeof(int *));
    for (int i = 0; i < nonZeroCount; i++) {
        triplet[i] = (int *)malloc(3 * sizeof(int));
    }


    sparseToTriplet(matrix, rows, cols, triplet, &nonZeroCount);


    printf("Triplet form of the sparse matrix:\n");
    displayTriplet(triplet, nonZeroCount);



    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);

    for (int i = 0; i < nonZeroCount; i++) {
        free(triplet[i]);
    }
    free(triplet);

    return 0;
}