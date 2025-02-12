#include <stdio.h>

int main() {

    int count = 2;
    for(int i = 1; i <= 3; i++) {
        for(int j = 1; j <= count; j++) {
            printf("  ");
        }
        for(int j = 1; j <= i * 2 + 1; j++) {
            printf("* ");
        }
        for(int j = 1; j <= count * 2 + 1; j++) {
            printf("  ");
        }
        for(int j = 1; j <= i * 2 + 1; j++) {
            printf("* ");
        }
        printf("\n");
        count--;
    }   

    
    for (int a = 8; a >= 1; a--) {
        
        for (int b = 1; b <= 8 - a; b++) {
            printf("  ");
        }

        
        for (int k = 1; k <= 2 * a - 1; k++) {
            printf("* ");
        }

        printf("\n");
    }

    return 0;
}
