#include <stdio.h>
int main() {
    int n = 1;
    float sum = 0.0;
    int m;
    scanf("%d" , &m);
    while (n <= m) { 
        if (n % 2 == 1) {
            sum +=(float) (n) / (float) ((n + 1));
        } else {
            sum -= (float) (n)/ (float) ((n + 1));
        }
        n++;
    }

    printf("Sum of the series is: %.2f\n", sum);

    return 0;
}
