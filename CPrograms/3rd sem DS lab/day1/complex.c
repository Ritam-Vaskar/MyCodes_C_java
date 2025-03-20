#include <stdio.h>

struct complex {
    int real;
    int imaginary;
};


void addComplex(struct complex *c1, struct complex *c2, struct complex *result) {
    result->real = c1->real + c2->real;
    result->imaginary = c1->imaginary + c2->imaginary;
}

int main() {
    struct complex c1, c2, result;

    printf("Enter real and imaginary parts of the first complex number: ");
    scanf("%d %d", &c1.real, &c1.imaginary);

    printf("Enter real and imaginary parts of the second complex number: ");
    scanf("%d %d", &c2.real, &c2.imaginary);

    addComplex(&c1, &c2, &result);

    printf("Sum of the complex numbers: %d + %di\n", result.real, result.imaginary);

    return 0;
}
