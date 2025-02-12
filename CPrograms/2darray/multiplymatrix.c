#include<stdio.h>
int main(){
    int n , m;
    printf("enter no. of rows of 1st:- ");
    scanf("%d" , &m);
    printf("enter no. of col. of 1st:- ");
    scanf("%d" , &n);

    int p , q;
    printf("enter no. of rows of 2nd:- ");
    scanf("%d" , &p);
    printf("enter no. of col. of 2nd:- ");
    scanf("%d" , &q);

    int a[m][n];
    //input 1st
    printf("Enter the %d elements of 1st matrix: ", m*n);
    for(int i=0;i<m;i++){
        for(int j=0 ; j<n ; j++){
            scanf("%d" , &a[i] [j]);
        }
        
    }

    int b[p][q];
    //input 1st
    printf("Enter the %d elements of 2nd matrix: ", p*q);
    for(int i=0;i<p;i++){
        for(int j=0 ; j<q ; j++){
            scanf("%d" , &b[i] [j]);
        }
        
    }

    //check

    if (n!=p)
    {
        printf("Can't Multiply");
    }

    else{
        //multiply
        int res[m][q];
        for(int i=0;i<m;i++){
        for(int j=0 ; j<q ; j++){
            res[i][j]=0;
            for (int k = 0; k < n; k++)
            {
                res [i][j]+= a[i][k] * b[k][j];
            }
            
        }
        
    }

    //print

    for(int i=0;i<m;i++){
        for(int j=0 ; j<q ; j++){
            printf("%d " , res[i][j]);
        }
        printf("\n");
        
    }
    }
    return 0;

}
    