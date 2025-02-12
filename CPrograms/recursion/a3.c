#include<stdio.h>
void dis(int a){
        if(a<0)
        return;
       printf("%d ",a);
       dis(a-2);
     }
int main(){
    int n;
    printf("Enter initial term: ");
    scanf("%d",&n);
    printf("The series is: ");
    dis(n);
    return 0;
}