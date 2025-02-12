#include <stdio.h>

int main() {
    int a, b, c;

    
    printf("Enter three numbers: ");

    scanf("%d %d %d", &a, &b, &c);

    
    int d= (((a >= b && a <= c) || (a >= c && a <= b)) ? a : (((b >= a && b <= c) || (b >= c && b <= a)) ? b : c));

        printf("Second highest number: %d\n", d);

   
}
