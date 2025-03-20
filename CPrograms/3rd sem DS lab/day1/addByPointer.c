// #include<stdio.h>
// int add(int *a , int *b , int *c){
//     *c = *b + *a;
// }
// int main(){
//     int a,b,res;
//     int *p1 , *p2 , *p3;
//     p1=&a;
//     p2=&b;
//     p3=&res;
//     scanf("%d" , &*p1);
//     scanf("%d" , &*p2);
//     add(&a , &b , &c);
//     printf("%d", );

// }

#include <stdio.h>
int sum(int *a, int *b, int *c)
{
    *c = *a + *b;
}
int main()
{
    printf("enter the 1st number:");
    int a;
    scanf("%d", &a);
    printf("enter the 2nd number:");
    int b;
    scanf("%d", &b);
    int c;
    // int c = a + b;
    // int *ptr1;
    // int *ptr2;
    // int *ptr3;
    // ptr1 = &a;
    // ptr2 = &b;
    // ptr3 = &c;
    sum(&a, &b, &c);
    printf("the sum of two numbers is %d :", c);
}