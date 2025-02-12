#include <stdio.h>

void copy(char *a, char *b) {
    while (*a != '\0') {
        *b = *a;
        a++;
        b++;
    }
    *b = '\0';
}

int main() {
    char a[200];
    printf("Enter sentence: ");
    scanf("%[^\n]s",a);
    char b[200]; 
    
    copy(a, b);
    
    printf("Real string: %s\n", a);
    printf("Copied string: %s\n", b);
    
    return 0;
}