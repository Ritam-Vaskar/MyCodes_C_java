#include <stdio.h>

int main() {
    int rows = 4; // Number of rows in the triangle

    for (int i = 1; i <= rows; i++) {
        // Print spaces to align numbers to the right
        for (int j = 0; j < rows - i; j++) {
            printf(" ");
        }

        // Print numbers
        for (int k = 1; k <= i; k++) {
            printf("%d", k);
        }

        printf("\n");
    }

    return 0;
}
