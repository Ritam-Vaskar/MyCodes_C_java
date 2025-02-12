#include<stdio.h>

int main()

{
    printf("enter the last term: ");
    int n;
    scanf("%d",&n);

    float sum=0.0;
    for(int i=1;i<=n;i++)
    {
        sum=sum+(1.0/i);
    }

    printf("the sum is %f \n",sum);
    return 0;
}