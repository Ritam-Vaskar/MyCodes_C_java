#include<stdio.h>
#include<stdlib.h>

int prime(int n) {
    if (n <= 1) return 0; 

    int i = 2;
    int flag = 1;

    while (i <= n / 2) { 
        if (n % i == 0) {
            flag = 0; 
            break;
        }
        i++;
    }

    return flag;
}

int main() {
    int *ptr;
    ptr = (int *) malloc(5 * sizeof(int));
    

    for (int i = 0; i < 5; i++) {
        printf("Enter %d element: ", i + 1);
        scanf("%d", ptr + i);
    }

    printf("The elements are: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", *(ptr + i));
    }
    printf("\n");

    int sum = 0;
    for (int i = 0; i < 5; i++) {
        if (prime(*(ptr + i))) {
            sum += *(ptr + i);
        }
    }

    printf("Sum of prime numbers in the array: %d\n", sum);

    free(ptr);
    return 0;
}
