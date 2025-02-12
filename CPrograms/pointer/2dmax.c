#include <stdio.h>
#include <limits.h> 

void find_stats_and_display(int arr[][100], int rows, int cols, int *max, int *min, int *secmin) {
  
  *max = INT_MIN;
  *min = INT_MAX;
  *secmin = INT_MAX;

  
  printf("Array elements:\n");
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      printf("%d ", arr[i][j]);

     
      if (arr[i][j] > *max) {
        *max = arr[i][j];
      }
      if (arr[i][j] < *min) {
        *min = arr[i][j];
      } else if (arr[i][j] < *secmin && arr[i][j] > *min) {
        *secmin = arr[i][j];
      }
    }
    printf("\n");
  }
}

int main() {
  int arr[100][100]; 
  int rows, cols, maxval, minval, secminval;

  printf("Enter the number of rows: ");
  scanf("%d", &rows);
  printf("Enter the number of columns: ");
  scanf("%d", &cols);

  printf("Enter the array elements:\n");
  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      scanf("%d", &arr[i][j]);
    }
  }

  find_stats_and_display(arr, rows, cols, &maxval, &minval, &secminval);

  printf("Maximum element: %d\n", maxval);
  printf("Minimum element: %d\n", minval);
  printf("Second minimum element: %d\n", secminval);

  return 0;
}
