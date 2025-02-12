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

        if(i%2==0){
            for(int j=0 ; j<m ; j++){
                printf("%d " , arr[i] [j]);
            }
        
        }
        else{
            for(int j=n-1 ; j>=0 ; j--){
                printf("%d " , arr[i] [j]);
            }
        

        
        
    }
    printf("\n");


}
}