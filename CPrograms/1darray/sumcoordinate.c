#include<stdio.h>
int main(){
    int n , m;
    printf("enter no. of elements:- ");
    scanf("%d" , &n);
   
    int arr[n];
    printf("Enter %d elements\n", n);
    
    for(int i=0;i<n;i++){
        
            scanf("%d" , &arr[i]);
        
        }

    int sum=0;
    for(int i=n-1;i>=0;i--){
            sum+=arr[i];
            printf("%d " , sum);

        
    }

}