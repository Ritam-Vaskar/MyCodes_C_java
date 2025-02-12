#include <stdio.h>
int main(){

int n;
printf("Enter even size: ");
scanf("%d",&n);
printf("Enter %d elements ",n);

int arr[n];


int *b=&arr;

for(int x=0;x<n;x++){
	scanf("%d",&arr[x]);
}
for(int x=0;x<n;x++){
	printf("%d",*(b+x));
}
for(int i=0,j=n-1;i<n/2;i++,j--){
	int temp=*(b+i);
	*(b+i)=*(b+j);
	*(b+j)=temp;
}
printf("\n");
for(int x=0;x<n;x++){
	printf("%d",*(b+x));
}
	return 0;

}
