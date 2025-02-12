#include <stdio.h>

struct com {
    int im;
    int re;
} input1,input2;

int main(){
    printf("Enter first complex no.: ");
    scanf("%d+%di", &input1.re , &input1.im);
    printf("Enter second complex no.: ");
    scanf("%d+%di", &input2.re , &input2.im);
    printf("addition is %d+%di",input1.re+input2.re,input1.im+input2.im);

}

