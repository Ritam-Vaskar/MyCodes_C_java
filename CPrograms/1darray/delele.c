#include <stdio.h>

int main() {
    int arr[100], n, i, element, count = 0;

    printf("Enter the size of the array: ");
    scanf("%d", &n);

    printf("Enter the elements of the array:\n");
    for (i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    printf("Enter the element to be deleted: ");
    scanf("%d", &element);

    
    for (i = 0; i < n - count;) {
        if (arr[i] == element) {
            
            for (int j = i; j < n - 1; j++) {
                arr[j] = arr[j + 1];
            }
            count++; 
        } else {
            i++; 
        }
    }

    n -= count; 

    printf("The array after deletion:\n");
    for (i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}
