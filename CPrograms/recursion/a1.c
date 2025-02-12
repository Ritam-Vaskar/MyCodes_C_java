#include<stdio.h>
int a(int m,int n){
 int i;
 for(i=m;i<=n;i++){
     if(i!=0){
         printf("%d ",i);
     }
 }
}
int main(){
    int m=0 ,n=10;
    a(m,n);
}