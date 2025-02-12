#include<stdio.h>
int main(){
    int n;
    printf("Enter The Number: ");
    scanf("%d",&n);
    for(int i=1;i<=n;i++){
        for(int j=1; j<=i ; j++){
            if((i+j)%2==0)
            printf("1 ");
            else printf("0 ");
        }
        printf("\n");
        
    }

    

    // for(int i=1;i<=n;i++){
    //     for(int j=1; j<=i ; j++){
    //         printf("%d ",j);
            
    //     }
    //     printf("\n");
        
    // }
    



    // for(int i=1;i<=n;i++){
    //     for(int j=1; j<=n+1-i ; j++){
    //         printf("%d ",j);
            
    //     }
    //     printf("\n");
        
    // }


    // int a=n;
    // for(int i=1;i<=n;i++){
    //     for(int j=1; j<=2*a-1 ; j=j+2){
    //         printf("%d ",j);
            
    //     }
    //     a--;
    //     printf("\n");
        
    // }

}