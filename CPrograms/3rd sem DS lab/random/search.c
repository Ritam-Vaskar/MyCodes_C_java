// #include<stdio.h>

// int search (int arr , int size , int key){
//     for(int i=0 ; i<=key ;i++){
//         printf("%d" , i);
//     }
// }
// int main(){
//     int arr[10];
//     int size;
//     scanf("%d", size);
//     for(int i=0 ; i<=size ; i++){
//         scanf("%d" , &arr[i]);
//     }
//     int key;
//     scanf("%d" , key);
//     search(arr , size ,key );
// }

#include <stdio.h>
void search(int a[], int n, int key)
{
    int f = 0;
    for (int i = 0; i < n; i++) if (a[i] == key) f = 1;
    if (f == 1)  printf("found");
    else  printf("not found");

}
int main()
{
    int arr[10];
    int key;
    printf("enter the elements of the array : ");
    for (int i = 0; i < 10; i++) scanf("%d", &arr[i]);
    printf("enter the key element : ");
    scanf("%d", &key);
    search(arr, 10, key);
    return 0;
}