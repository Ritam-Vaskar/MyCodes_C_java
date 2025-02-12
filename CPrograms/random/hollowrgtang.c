#include <stdio.h>

int main() {
    int rows = 5; // Number of rows in the pattern

    for (int i = 0; i < rows; i++) {
        // Print stars
        printf("*");

        // Print spaces
        for (int j = 0; j < i; j++) {
            printf("\t");
        }

        // Print stars again
        printf("*");

        // Print additional spaces to align the next stars
        for (int k = 0; k < (rows - i - 1) * 4; k++) {
            printf("\t");
        }

        // Print stars
        printf("*");

        printf("\n");
    }

    return 0;
}
