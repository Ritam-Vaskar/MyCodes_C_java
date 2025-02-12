#include<stdio.h>
int adddigit(int a){
    int sum=0 , b;
    while (a>0)
    {
        b=a%10;
        sum=sum+b;
        a=a/10;
    }
    printf(" sum is %d", sum);
    
}
int main(){
    int n;
    printf("enter a number: ");
    scanf("%d",&n);
    adddigit(n);
    
}