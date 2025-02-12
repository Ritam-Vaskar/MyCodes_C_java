#include<stdio.h>
int prime(int num){
    if(num<=1){
        return 0;
    }
    for(int i=2;i*i<=num;i++){
        if(num%i==0){
            return 0;
        }
    }
}
int main(){
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);
    if(prime(num)){
        printf("The number is Prime");
    }
    else printf("the number is not a prime number");
    return 0;
}