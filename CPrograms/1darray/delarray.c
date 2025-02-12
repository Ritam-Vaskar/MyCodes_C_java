#include <stdio.h>

void del(int arr[], int *size, int element) {
    int i, j, found = 0;
    
    
    for(i = 0; i < *size; i++) {
        if(arr[i] == element) {
            found = 1;
            
            
            for(j = i; j < *size - 1; j++) {
                arr[j] = arr[j + 1];
            }
            (*size)--;
            break;
        }
    }
    
    if(found) {
        printf("Element %d deleted successfully.\n", element);
    } else {
        printf("Element %d not found in the array.\n", element);
    }
}

int main() {
    int arr[100], size, i, element;

    printf("Enter the size of the array: ");
    scanf("%d", &size);

    printf("Enter the elements of the array:\n");
    for (i = 0; i < size; i++) {
        scanf("%d", &arr[i]);
    }

    printf("Enter the element to delete: ");
    scanf("%d", &element);

    del(arr, &size, element);

    printf("Array after deletion:\n");
    for (i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0;
}