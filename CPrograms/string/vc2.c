#include <stdio.h>

int main() {
    char str[100];
    int vowels[5] = {0}; 
    int consonants[26] = {0}; 

    printf("Enter a string: ");
    scanf("%s", str);

    
    for (int i = 0; str[i] != '\0'; i++) {
        
        char ch = str[i];
        if (ch >= 'A' && ch <= 'Z')
            ch += 32;

      
        if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {
            
            switch(ch) {
                case 'a':
                    vowels[0]++;
                    break;
                case 'e':
                    vowels[1]++;
                    break;
                case 'i':
                    vowels[2]++;
                    break;
                case 'o':
                    vowels[3]++;
                    break;
                case 'u':
                    vowels[4]++;
                    break;
            }
        }
        
        else if (ch >= 'a' && ch <= 'z') {
            
            consonants[ch - 'a']++;
        }
    }

    
    printf("Vowels: \n");
    if (vowels[0] > 0) printf("a: %d\n", vowels[0]);
    if (vowels[1] > 0) printf("e: %d\n", vowels[1]);
    if (vowels[2] > 0) printf("i: %d\n", vowels[2]);
    if (vowels[3] > 0) printf("o: %d\n", vowels[3]);
    if (vowels[4] > 0) printf("u: %d\n", vowels[4]);

    
    printf("Consonants: \n");
    for (int i = 0; i < 26; i++) {
        if (consonants[i] > 0) {
            printf("%c: %d\n", 'a' + i, consonants[i]);
        }
    }

    return 0;
}
