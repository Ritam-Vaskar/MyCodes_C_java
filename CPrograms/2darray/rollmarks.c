#include<stdio.h>
int main(){
    int n;
    printf("Enter The No. of Student :- ");
    scanf("%d" , &n);
    int arr[3][n];
    for(int i=0;i<n;i++){
        for(int j=0 ; j<3 ; j++){
            printf("Number of %d Subject of %d student ", j+1 , i+1);
            scanf("%d" , &arr[i] [j]);
        }
        
    }
    
    for(int i=0;i<n;i++){
        printf ("Marks of %d student in PCM is ", i+1);
        for(int j=0 ; j<3 ; j++){
            printf("%d " , arr[i] [j]);
        }

        printf("\n");
        
    }
}