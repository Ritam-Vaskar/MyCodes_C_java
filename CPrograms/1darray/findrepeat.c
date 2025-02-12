#include<stdio.h>
void rep(int arr[], int size) {
    
    for (int i = 0; i < size - 1; ++i) {
        for (int j = i + 1; j < size; ++j) {
            if (arr[i] > arr[j]) {
                
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }

    for (int i = 0; i < size - 1; i++) {
        if (arr[i] == arr[i + 1]) {
            printf("Repeated element: %d\n", arr[i]);
            return;
        }
    }
}

int main(){
    
    int arr[4]={1,2,3,3};
    rep(arr,4);

}