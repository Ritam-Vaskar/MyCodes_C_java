#include<stdio.h>
int main(){
    int n , m;
    printf("enter no. of rows:- ");
    scanf("%d" , &n);
    printf("enter no. of col.:- ");
    scanf("%d" , &m);

    int arr[n][m];
    printf("Enter %d elements\n", n*m);
    
    for(int i=0;i<n;i++){
        for(int j=0 ; j<m ; j++){
            scanf("%d" , &arr[i] [j]);
        }
        
    }

    for(int i=0;i<n;i++){
        for(int j=0 ; j<m ; j++){
            printf("%d " , arr[i] [j]);
        }

        printf("\n");
        
    }

    int sum=0;
    for(int i=0 ; i<n ; i++){
        for(int j=0 ; j<m ; j++){
            sum+=arr[i][j];
        }
    }
    printf("the sum is %d" , sum);
}