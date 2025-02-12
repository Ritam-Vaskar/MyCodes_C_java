#include <stdio.h>

int find(int arr[], int size, int target, int *index_found) {
  
  *index_found = -1;

  
  for (int i = 0; i < size; i++) {
    if (arr[i] == target) {
      
      *index_found = i;
      return 1; 
    }
  }

  
  return 0;
}

int main() {
    int n;
    printf("Enter the size of array: ");
    scanf("%d",&n);
    int arr[n];
    printf("Enter the Elements: ");
  for (int i = 0; i < n; i++)
    {  
        scanf("%d", &arr[i]);  
    }
  
  int target, index;

  printf("Enter the number to search: ");
  scanf("%d", &target);

  if (find(arr, n, target, &index)) {
    printf("Number %d found at index %d\n", target, index);
  } else {
    printf("Number %d not found in the array\n", target);
  }

  return 0;
}
