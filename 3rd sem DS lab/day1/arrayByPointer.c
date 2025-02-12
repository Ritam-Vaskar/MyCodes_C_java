#include<stdio.h>
int main(){
    int arr[5];
    int *ptr;
    ptr= &arr[0];
    for(int i=0 ; i<5 ; i++){
        scanf("%d" , (ptr+i));
    }
    ptr= &arr[0];
    for(int i=0 ; i<5 ; i++){
        printf("%d " , *(ptr+i));
    }

}