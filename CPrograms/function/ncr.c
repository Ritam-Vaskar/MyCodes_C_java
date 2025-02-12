#include<stdio.h>

int fact(int x){
    int f=1;
    for(int i=2 ; i<=x ; i++){
      f=f*i;  
    }
    return f;
}
int main (){
    int n;
    printf("Enter n :- ");
    scanf("%d" , &n);

    int r;
    printf("Enter r :- ");
    scanf("%d" , &r);
    int nCr=fact(n)/(fact(r)*fact(n-r));
    printf("The nCr result is %d" , nCr);
    return 0;
}