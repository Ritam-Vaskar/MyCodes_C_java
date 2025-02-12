#include<stdio.h>
int main(){
    int n;
    printf("Enter The Number: ");
    scanf("%d",&n);
    // for(int i=1;i<=n;i++){
    //     for(int j=1; j<=n ; j++){
    //         printf("* ");
    //     }
    //     printf("\n");
        
    // }

    // for(int i=1;i<=n;i++){
    //     for(int j=1; j<=n ; j++){
    //         printf("%d ", j);
    //     }
    //     printf("\n");
        
    // }



    for(int i=1;i<=n;i++){
        for(int j=1; j<=n ; j=j+2){
            printf("%d ", j);
        }
        printf("\n");
        
    }

}