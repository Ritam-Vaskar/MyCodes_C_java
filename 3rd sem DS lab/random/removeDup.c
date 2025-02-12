#include<stdio.h>
void removeDup(int *arr , int *n){
    if (*n==0) return;
    int idx=0;
    for (int i = 0; i < *n; i++) {
        if (arr[i]!=arr[idx])
        {
            idx++;
            arr[idx]=arr[i];
        }
        
    }

    *n=idx+1;
}
int main(){
    int arr[] = {1, 2, 3, 4, 4 ,4 , 5, 5, 6};
    int n = sizeof(arr) / sizeof(arr[0]);

    removeDup(arr, &n);

    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}