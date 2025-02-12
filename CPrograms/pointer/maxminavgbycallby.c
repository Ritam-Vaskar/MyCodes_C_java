#include <stdio.h>

void find(int num1, int num2, float *avg, int *max, int *min) {
  
  *avg = (float) (num1 + num2) / 2.0;

 
  *max = num1;
  *min = num1;

  
  if (num2 > *max) {
    *max = num2;
  }
  if (num2 < *min) {
    *min = num2;
  }
}

int main() {
  int num1, num2;
  float avg;
  int max, min;

  printf("Enter two integers: ");
  scanf("%d %d", &num1, &num2);

  find(num1, num2, &avg, &max, &min);

  printf("Average: %.2f\n", avg);
  printf("Maximum: %d\n", max);
  printf("Minimum: %d\n", min);

  return 0;
}