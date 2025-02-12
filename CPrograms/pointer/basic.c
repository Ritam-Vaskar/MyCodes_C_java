#include<stdio.h>
int main(){
    int a=10;
    int* ptr =&a;
    printf("%p",&a);
    printf("\n%d",ptr);
}