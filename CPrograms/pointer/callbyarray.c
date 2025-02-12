#include <stdio.h>

void max(int arr[], int size, int *maxele) {

  *maxele = arr[0];

 
  printf("Array elements: ");
  for (int i = 0; i < size; i++) {
    printf("%d ", arr[i]);

 
    if (arr[i] > *maxele) {
      *maxele = arr[i];
    }
  }
  printf("\n");
}

int main() {
  int arr[100]; 
  int size, maxval;

  printf("Enter the size of the array (less than 100): ");
  scanf("%d", &size);

  printf("Enter the array elements: ");
  for (int i = 0; i < size; i++) {
    scanf("%d", &arr[i]);
  }

  max(arr, size, &maxval);

  printf("Maximum element: %d\n", maxval);

  return 0;
}
