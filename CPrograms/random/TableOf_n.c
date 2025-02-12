#include<stdio.h>
int main(){

    int n;
    printf("Rquired Table: ");
    scanf("%d", &n);
    for(int i=n; i<=(10*n); i=i+n){
        printf("%d ", i);
    }

    return 0;

}