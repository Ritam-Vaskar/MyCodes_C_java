#include <stdio.h>

int main() {
    int decimal, remainder, stack[32], top = -1;

    
    printf("Enter a decimal number: ");
    scanf("%d", &decimal);


    if (decimal == 0) {
        printf("Binary: 0\n");
        return 0;
    }

    
    while (decimal > 0) {
        remainder = decimal % 2;
        stack[++top] = remainder;  
        decimal = decimal / 2;
    }

  
    printf("Binary: ");
    while (top >= 0) {
        printf("%d", stack[top--]);
    }
    printf("\n");

    return 0;
}
