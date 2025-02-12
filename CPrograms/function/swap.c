#include<stdio.h>

void swap(int x , int y){
    int temp = x;
    x=y;
    y=temp;
    return ;
}

int main (){
    int n;
    printf("Enter n :- ");
    scanf("%d" , &n);

    int r;
    printf("Enter r :- ");
    scanf("%d" , &r); 

    swap(n,r);
    
    printf("%d , " , n );
    printf("%d" , r );
    return 0;
}