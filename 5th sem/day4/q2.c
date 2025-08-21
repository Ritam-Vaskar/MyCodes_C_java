// find a^n
#include<stdio.h>
int power(int a, int n) {
    if (n == 0)
        return 1;
    return a * power(a, n - 1);
}
int main() {
    int a, n;
    printf("Enter the base (a): ");
    scanf("%d", &a);
    printf("Enter the exponent (n): ");
    scanf("%d", &n);

    int result = power(a, n);
    printf("%d raised to the power of %d is: %d\n", a, n, result);

    return 0;
}