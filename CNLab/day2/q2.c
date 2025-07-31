// Write a C program to extract each byte from a
// given number and store them in separate character
// variables and print the content of those variables.

#include <stdio.h>

int main() {
    int num = 12345678;
    char byte1 = (num >> 24) & 0xFF;
    char byte2 = (num >> 16) & 0xFF;
    char byte3 = (num >> 8) & 0xFF;
    char byte4 = num & 0xFF;

    printf("Byte 1: %d\n", byte1);
    printf("Byte 2: %d\n", byte2);
    printf("Byte 3: %d\n", byte3);
    printf("Byte 4: %d\n", byte4);

    return 0;
}