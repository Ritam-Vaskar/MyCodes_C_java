#include <stdio.h>

int main() {
    int rows = 5; 
    int count = 1; 

    for (int i = 0; i < rows; i++) {
        if (i % 2 == 0) {
            
            for (int j = 0; j < rows - i; j++) {
                printf("%d ", count);
                count++;
            }
        } else {
            
            int a = count + rows - 1 - i;
            for (int j = 0; j < rows - i; j++) {
                printf("%d ", a);
                a--;
            }
            count += rows - i;
        }
        printf("\n");
    }

    return 0;
}
