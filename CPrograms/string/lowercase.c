#include <stdio.h>



int main() {
    char s[100];
    int i = 0;

    printf("Enter a Sentence in uppercase: ");
    scanf("%[^\n]", s); 
    

    while (s[i] != '\0') {
        if (s[i] >= 'A' && s[i] <= 'Z') {
            s[i] += 32;
        }
        i++;
    }

    printf("Sentence in lowercase: %s\n", s);

    return 0;
}
