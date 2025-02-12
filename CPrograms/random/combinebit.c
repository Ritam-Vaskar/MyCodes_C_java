#include <stdio.h>

int main() {
   unsigned short a = 0x3A;
   unsigned short b = 0x24;

   
   unsigned short c = (a << 8) | b;

   
   unsigned short d = ((c & 0xFF00) >> 8) | ((c & 0x00FF) << 8);

   printf("Combined value: 0x%X\n", c);
   printf("Swapped value: 0x%X\n", d);

   return 0;
}
