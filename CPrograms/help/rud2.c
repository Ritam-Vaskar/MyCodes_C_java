#include <stdio.h>

void reverse_string(char *str) {
    if (*str == '\0') {
        return;
    }
    reverse_string(str + 1);
    printf("%c", *str);
}

int main() {
    char str[] = "hello\0";
    reverse_string(str);
    return 0;
}