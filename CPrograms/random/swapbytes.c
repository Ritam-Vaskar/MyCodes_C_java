#include <stdio.h>

int main() {
    unsigned int a = 0xA345986B;

    // Interchange the bytes using bitwise operations
    unsigned int b = 
        ((a & 0x000000FF) << 24) |  
        ((a & 0x0000FF00) << 8) |   
        ((a & 0x00FF0000) >> 8) |   
        ((a & 0xFF000000) >> 24);   

    printf("Original value: 0x%X\n", a);
    printf("Swapped value: 0x%X\n", b);

    return 0;
}
