
// Q.1: WAP to create a 1-D array of n elements and perform the following menu-based operations using functions.

// insert a given element at a specific position.
// delete an element from a specific position of the array.
// linear search to search an element
// traversal of the array

#include <stdio.h>
#include <stdlib.h>


//function for insert

void insertElement(int arr[], int *n, int element, int position) {
    if (position < 0 || position > *n) {
        printf("Invalid position!\n");
        return;
    }
    for (int i = *n; i > position; i--) {
        arr[i] = arr[i - 1];
    }
    arr[position] = element;
    (*n)++;
}



//for deletion
void deleteElement(int arr[], int *n, int position) {
    if (position < 0 || position >= *n) {
        printf("Invalid position!\n");
        return;
    }
    for (int i = position; i < *n - 1; i++) {
        arr[i] = arr[i + 1];
    }
    (*n)--;
}


//for searching
int linearSearch(int arr[], int n, int element) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == element) {
            return i;
        }
    }
    return -1;
}



//for traverse
void traverseArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}




int main() {
    int n, choice, element, position;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    int *arr = (int *)malloc(n * sizeof(int));

    printf("Enter the elements of the array:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    while (1) {
        printf("\nMenu:\n");
        printf("1. Insert an element\n");
        printf("2. Delete an element\n");
        printf("3. Search for an element\n");
        printf("4. Traverse the array\n");
        printf("5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the element to insert: ");
                scanf("%d", &element);
                printf("Enter the position to insert the element: ");
                scanf("%d", &position);
                insertElement(arr, &n, element, position);
                break;
            case 2:
                printf("Enter the position to delete the element: ");
                scanf("%d", &position);
                deleteElement(arr, &n, position);
                break;
            case 3:
                printf("Enter the element to search for: ");
                scanf("%d", &element);
                position = linearSearch(arr, n, element);
                if (position != -1) {
                    printf("Element found at position %d\n", position);
                } else {
                    printf("Element not found\n");
                }
                break;
            case 4:
                printf("Array elements: ");
                traverseArray(arr, n);
                break;
            case 5:
                free(arr);
                return 0;
            default:
                printf("Invalid choice! Please try again.\n");
        }
    }
}
