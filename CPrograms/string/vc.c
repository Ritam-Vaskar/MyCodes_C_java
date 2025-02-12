#include <stdio.h>

int main() {
    char str[100];
    int vowels = 0, consonants = 0;
    
    printf("Enter a string: ");
    scanf("%[^\n]c" , str);
    

    for (int i = 0; str[i] != '\0'; i++) {
        
        if (str[i] >= 'A' && str[i] <= 'Z')
            str[i] += 32;

        
            if (str[i] == 'a' || str[i] == 'e' || str[i] == 'i' || str[i] == 'o' || str[i] == 'u') {
                vowels++;
                
            } else {
                consonants++;
            }
        
    }

    printf("Number of vowels: %d\n", vowels);
    printf("Number of consonants: %d\n", consonants);

    return 0;
}
