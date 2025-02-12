#include<stdio.h>
int main(){

int i=1,n;
scanf("%d", &n);
while(i>0){

	if(n%i==0){
	
	printf("%d " , i);
	}
	i++;
}
}