// #include<stdio.h>

// void count(int arr[],int n);

// void count(int arr[],int n){

//     int c=0;
//     for(int i=0;i<n;i++){
//         if(arr[i]%2!=0){
//             c++;
//         }
//     }
//     printf("the total number of odd numbers are %d \n",c);
// }

// int main(){
//     printf("enter the size of array \n");
//     int n;
//     scanf("%d",&n);

    
//     int arr[n];
//     for(int i=0;i<n;i++){
//         printf("%d index : ",i);
//         scanf("%d",&arr[i]);
//     }
//     int sum=0;
//     for(int i=0;i<n;i++){   
//         sum=sum+arr[i];  
//     }
//      printf("%d",sum);
    
//     return 0;
// }

#include <stdio.h>

int main() {
    int arr[] = {2, 5, 6, 7, 9, 10};
    int n = 6; // Size of the array
    
    // Initialize max to the first element of the array
    int max = arr[0];
    
    // Iterate through the array to find the maximum value
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    
    printf("Largest number in the array: %d\n", max);
    
    return 0;
}









// #include<stdio.h>

// int main()

// {
//     int temp=0;

//     printf("enter the size of array: ");
//     int n;
//     scanf("%d",&n);

//     printf("enter the elements of array:  \n");

//     int a[n];
    
//     for(int i=0;i<n;i++)
//     {
//         scanf("%d",&a[i]);
//     }

//     printf("the array is:  \n");
//     {
//         for(int i=0;i<n;i++)
//         {
//             printf("%d ",a[i]);
//         }
//         printf("\n");
//     }

//     for(int i=0;i<n;i++)
//     {
//         if(i==0)
//         {
//             temp=a[n-1];
//             a[n-1]=a[i];
//             a[i]=temp;
//         }

//         else if(i==2)
//         {
//             temp=a[n-2];
//             a[n-2]=a[i];
//             a[i]=temp;
//         }
//     }

//     for(int i=0;i<n;i++)
//         {
//             printf("%d ",a[i]);
//         }
//     return 0;
// }