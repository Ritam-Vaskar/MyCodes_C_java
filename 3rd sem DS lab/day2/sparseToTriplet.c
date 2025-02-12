#include <stdio.h>

void sparseToTriplet(int matrix[100][100], int rows, int cols, int triplet[100][3], int *nonZeroCount) {
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

void displayTriplet(int triplet[100][3], int nonZeroCount) {
    printf("Row\tColumn\tValue\n");
    for (int i = 0; i < nonZeroCount; i++) {
        printf("%d\t%d\t%d\n", triplet[i][0], triplet[i][1], triplet[i][2]);
    }
}

int main() {
    int rows, cols;
    int matrix[100][100];
    int triplet[100][3];
    int nonZeroCount = 0;

    printf("Enter the number of rows: ");
    scanf("%d", &rows);
    printf("Enter the number of columns: ");
    scanf("%d", &cols);

    printf("Enter the elements of the sparse matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("Element at (%d, %d): ", i, j);
            scanf("%d", &matrix[i][j]);
        }
    }

    sparseToTriplet(matrix, rows, cols, triplet, &nonZeroCount);

    printf("Triplet form of the sparse matrix:\n");
    displayTriplet(triplet, nonZeroCount);

    return 0;
}