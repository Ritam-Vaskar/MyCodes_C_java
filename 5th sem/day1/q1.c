// //2nd largest & 2nd smallest element in an array of size n
// #include <stdio.h>
// #include <limits.h>

// int main() {
//     int n;
//     printf("Enter the size of the array: ");
//     scanf("%d", &n);

//     int arr[n];
//     printf("Enter the elements of the array:\n");
//     for (int i = 0; i < n; i++) {
//         scanf("%d", &arr[i]);
//     }

//     int largest = INT_MIN;
//     int sl = INT_MIN;
//     int smallest = INT_MAX;
//     int ss = INT_MAX;

//     for (int i = 0; i < n; i++) {
//         if (arr[i] > largest) {
//             sl = largest;
//             largest = arr[i];
//         } else if (arr[i] > sl) {
//             sl = arr[i];
//         }

//         if (arr[i] < smallest) {
//             ss = smallest;
//             smallest = arr[i];
//         } else if (arr[i] < ss) {
//             ss = arr[i];
//         }
//     }

//     printf("Second largest element: %d\n", sl);
//     printf("Second smallest element: %d\n", ss);

//     return 0;
// }

#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
int main() {
    FILE *file = fopen("q1.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    //read the size of the array
    int n;
    fscanf(file, "%d", &n);

    //allocate memory for the array using malloc
    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed.\n");
        fclose(file);
        return 1;
    }

    for (int i = 0; i < 5; i++) {
        fscanf(file, "%d", &arr[i]);
    }

    int largest = INT_MIN;
    int sl = INT_MIN;
    int smallest = INT_MAX;
    int ss = INT_MAX;

    for (int i = 0; i < 5; i++) {
        if (arr[i] > largest) {
            sl = largest;
            largest = arr[i];
        } else if (arr[i] > sl) {
            sl = arr[i];
        }

        if (arr[i] < smallest) {
            ss = smallest;
            smallest = arr[i];
        } else if (arr[i] < ss) {
            ss = arr[i];
        }
    }

    printf("Second largest element: %d\n", sl);
    printf("Second smallest element: %d\n", ss);
}