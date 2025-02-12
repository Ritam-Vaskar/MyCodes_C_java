#include<stdio.h>
void dis(int r){
int rem=0;
        if(r==0)
        return ;
       rem=r%10;
       dis(r/10);
        printf("%d",rem);
       return ;
     }
int main(){
    int n;
    printf("Enter The Number: ");
    scanf("%d",&n);
    printf("Digits in The Number are: \n");
    dis(n);
    return 0;
}