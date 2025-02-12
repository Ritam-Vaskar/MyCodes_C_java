#include <stdio.h>

void swap(char str[]) {
  int len = 0;
  while (str[len] != '\0') {
    len++;
  }

  for (int i = 0; i < len - 1; i++) {
    
    char temp = str[i];
    str[i] = str[i + 1];
    str[i + 1] = temp;
  }
}

int main() {
  char str[100];

  printf("Enter a string: ");
  fgets(str, 100, stdin);

  swap(str);

  printf("String after swapping: %s\n", str);

  return 0;
}
