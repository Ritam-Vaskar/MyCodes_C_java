//1.4 Aim of the program: Write a function to ROTATE_RIGHT (p1, p2) right an array for first p2elements by 1 position using EXCHANGE (p, q) function that swaps/exchanges the numbersp& q. Parameter p1 be the starting address of the array and p2 be the number of elements toberotated. Input: Enter an array A of size N (9): 11 22 33 44 55 66 77 88 99 Call the function ROTATE_RIGHT (A, 5) Output: Before ROTATE: 11 22 33 44 55 66 77 88 99 After ROTATE: 55 11  22 33 44 66 77 88 99

#include <stdio.h>

void rotate_right(int arr[], int n, int k) {
    int temp;
    for (int i = 0; i < k; i++) {
        temp = arr[n - 1];
        for (int j = n - 1; j > 0; j--) {
            arr[j] = arr[j - 1];
        }
        arr[0] = temp;
    }
}

int main() {
    int arr[9];
    printf("Enter an array A of size N (9): ");
    for (int i = 0; i < 9; i++) {
        scanf("%d", &arr[i]);
    }
    int n = 9;
    int k = 5;
    printf("Before ROTATE: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    rotate_right(arr, n, k);
    printf("After ROTATE: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    return 0;
}