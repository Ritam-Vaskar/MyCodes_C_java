#include <stdio.h>

struct Data {
    int num1;
    float num2;
    char ch;
};

int main() {
    struct Data data; 

    
    int *ptrnum1 = &data.num1;
    float *ptrnum2 = &data.num2;
    char *ptrch = &data.ch;

    
    printf("Enter an integer: ");
    scanf("%d", ptrnum1);

    printf("Enter a floating-point number: ");
    scanf("%f", ptrnum2);

    printf("Enter a character: ");
    scanf(" %c", ptrch);

    
    printf("\nData entered:\n");
    printf("Integer: %d\n", *ptrnum1);
    printf("Floating-point number: %.2f\n", *ptrnum2);
    printf("Character: %c\n", *ptrch);

    return 0;
}
