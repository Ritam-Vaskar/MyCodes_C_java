#include <stdio.h>
#include <stdlib.h>


void addPoly(int *poly1, int *poly2, int *result, int n) {
    for (int i = 0; i < n; i++) {
        result[i] = poly1[i] + poly2[i];
    }
}



void displayPoly(int *poly, int n) {
    for (int i = 0; i < n; i++) {
        if (poly[i] != 0) {
            printf("%d", poly[i]);
            if (i > 0) {
                printf("x^%d", i);
            }
            if (i < n - 1 && poly[i + 1] != 0) {
                printf(" + ");
            }
        }
    }
    printf("\n");
}



int main() {
    int deg;
    printf("Enter the deg of the polynomials: ");
    scanf("%d", &deg);

    int *poly1 = (int *)malloc((deg + 1) * sizeof(int));
    int *poly2 = (int *)malloc((deg + 1) * sizeof(int));
    int *result = (int *)malloc((deg + 1) * sizeof(int));


    printf("Enter the coefficients of the first polynomial:\n");
    for (int i = 0; i <= deg; i++) {
        printf("Coefficient of x^%d: ", i);
        scanf("%d", &poly1[i]);
    }


    printf("Enter the coefficients of the second polynomial:\n");
    for (int i = 0; i <= deg; i++) {
        printf("Coefficient of x^%d: ", i);
        scanf("%d", &poly2[i]);
    }


    addPoly(poly1, poly2, result, deg + 1);


    printf("Result:\n");
    displayPoly(result, deg + 1);


    free(poly1);
    free(poly2);
    free(result);

    return 0;
}

