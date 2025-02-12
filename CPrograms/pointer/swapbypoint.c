#include<stdio.h>

void swap(int* x , int* y){
    int temp = *x;
    *x=*y;
    *y=temp;
    return ;
}

int main (){
    int n;
    printf("Enter n :- ");
    scanf("%d" , &n);

    int r;
    printf("Enter r :- ");
    scanf("%d" , &r); 

    swap(&n,&r);
    
    printf("New n is %d , " , n );
    printf("New r is %d" , r );
    return 0;
}