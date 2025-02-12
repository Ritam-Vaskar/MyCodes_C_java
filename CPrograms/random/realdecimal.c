#include<stdio.h>
int main (){
    float n;
    printf("Enter a Number:- ");
    scanf("%f", &n);
    int a=n;
    float b = n-a;
    printf("Before Decimal: ");
    printf("%d", a);
    printf("\nAfter Decimal:- ");
    printf("%f", b);
}