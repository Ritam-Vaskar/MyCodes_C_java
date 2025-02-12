#include<stdio.h>

int main()

{
    int temp=0;

    printf("enter the size of array: ");
    int n;
    scanf("%d",&n);

    printf("enter the elements of array:  \n");

    int a[n];
    
    for(int i=0;i<n;i++)
    {
        scanf("%d",&a[i]);
    }

    printf("the array is:  \n");
    {
        for(int i=0;i<n;i++)
        {
            printf("%d ",a[i]);
        }
        printf("\n");
    }

    for(int i=0;i<n/2;i++)
    {
        temp=a[i+(n/2)];
        a[i+(n/2)]=a[i];
        a[i]=temp;
    }

    for(int i=0;i<n;i++)
        {
            printf("%d ",a[i]);
        }
    return 0;
}