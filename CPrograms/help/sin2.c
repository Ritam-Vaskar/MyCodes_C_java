#include <stdio.h>

float power(float base, int exponent) {
    float result = 1.0;
    int i;

    for (i = 0; i < exponent; i++) {
        result *= base;
    }

    return result;
}


int factorial(int n) {
    int fact = 1;
    for (int i = 1; i <= n; ++i) {
        fact *= i;
    }
    return fact;
}


float Sin(float x, int n) {
    float sine = 0.0;
    int sign = 1;

    for (int i = 0; i < n; i++) {
        sine += sign * power(x, 2 * i + 1) / factorial(2 * i + 1);
        sign *= -1; 
    }

    return sine;
}

int main() {
    float angle;
    int terms;

    printf("Enter angle in radians: ");
    scanf("%f", &angle);

    printf("Enter number of terms: ");
    scanf("%d", &terms);

    float res = Sin(angle, terms);

    printf("Sin(%f) = %.6f\n", angle, res);

    return 0;
}
