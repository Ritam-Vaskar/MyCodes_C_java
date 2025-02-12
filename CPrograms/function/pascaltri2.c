#include<stdio.h>

int fact(int x){
    int f=1;
    for(int i=2 ; i<=x ; i++){
      f=f*i;  
    }
    return f;
}

int comb(int a , int b){
    int aCb= fact(a)/(fact(b)*fact(a-b));
    return aCb;
}
int main (){
    int n;
    printf("Enter n :- ");
    scanf("%d" , &n);

    for(int i=0 ; i<=n ; i++){
        for(int k=n ; k>=i ; k-- ){
            printf(" ");
        }

        for(int j=0 ; j<=i ; j++){
            int iCj= comb(i,j);
            printf("%d " , iCj );
        }
            
        printf("\n");
    }
    
    return 0;
}