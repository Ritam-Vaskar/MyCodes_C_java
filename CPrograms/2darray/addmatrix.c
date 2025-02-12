#include<stdio.h>
int main(){
    
    int arr[2][2];
    
    for(int i=0;i<2;i++){
        for(int j=0 ; j<2 ; j++){
            scanf("%d " , &arr[i] [j]);
        }
        
    }

    int brr[2][2];

    for(int i=0;i<2;i++){
        for(int j=0 ; j<2 ; j++){
            scanf("%d " , &brr[i] [j]);
        }
        
    }

    int res[2][2];
    
    for(int i=0;i<2;i++){
        for(int j=0 ; j<2 ; j++){
           res[i][j] = arr[i][j]+brr[i][j];
        }
        printf("\n");
        
    }

    for(int i=0;i<2;i++){
        for(int j=0 ; j<2 ; j++){
           printf("%d ", res[i][j]); 
        }
        printf("\n");
        
    }
}