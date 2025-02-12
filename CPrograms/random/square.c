#include <stdio.h>

int main() {
    int rows = 4; // Number of rows in the square
    int count = 1; // Initial value for the square

    // Printing the square pattern
    for (int i = 0; i < rows; i++) {
        if (i % 2 == 0) {
            // Even row: increasing order
            for (int j = 0; j < rows; j++) {
                printf("%d\t", count);
                count++;
            }
        } else {
            // Odd row: decreasing order
            int temp = count + rows - 1;
            for (int j = 0; j < rows; j++) {
                printf("%d\t", temp);
                temp--;
            }
            count += rows;
        }
        printf("\n");
    }

    return 0;
}
