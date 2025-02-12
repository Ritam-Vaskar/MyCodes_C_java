#include<stdio.h>
#include<math.h>
int main(){

//no. of digit

int n;
int i=0;
scanf("%d", &n);


while(n!=0){
	int a=n%10;
	i++;
	n=n/10;
	}
	if (i%2==0){
        int num1= n/pow(10,n);
    }

}