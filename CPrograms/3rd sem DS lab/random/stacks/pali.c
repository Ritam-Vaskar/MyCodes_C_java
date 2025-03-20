#include <stdio.h>
#include <string.h>

int main() {
    char str[100];
    char stack[100];
    int top = -1;

   
    printf("Enter a string: ");
    scanf("%s", str);

    int length = strlen(str);

    
    for (int i = 0; i < length; i++) {
        stack[++top] = str[i];
    }

   
    for (int i = 0; i < length; i++) {
        if (str[i] != stack[top--]) {
            printf("The string is not a palindrome.\n");
            return 0;
        }
    }

    printf("The string is a palindrome.\n");
    return 0;
}
