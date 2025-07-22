//number of duplicates in an array and most repeated element and how many times it is repeated
#include <stdio.h>
int main() {
    int n;
    printf("Enter the size of the array: ");
    scanf("%d", &n);

    int arr[n];
    printf("Enter the elements of the array:\n");
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    int count = 0;
    int maxCount = 0;
    int maxElement = arr[0];

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (arr[i] == arr[j]) {
                count++;
                if (count > maxCount) {
                    maxCount = count;
                    maxElement = arr[i];
                }
            }
        }
        count = 0;
    }

    printf("Number of duplicates: %d\n", maxCount);
    printf("Most repeated element: %d\n", maxElement);
    printf("Number of times repeated: %d\n", maxCount);

    return 0;
}
