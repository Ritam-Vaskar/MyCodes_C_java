#include <stdio.h>
#include <stdlib.h>

// Define a Node structure for the polynomial
struct Node {
    int coeff;
    int exp;
    struct Node* next;
};

int main() {
    struct Node *poly1 = NULL, *poly2 = NULL, *result = NULL;

    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 3;
    newNode->exp = 3;
    newNode->next = poly1;
    poly1 = newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 2;
    newNode->exp = 2;
    newNode->next = poly1;
    poly1 = newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 1;
    newNode->exp = 0;
    newNode->next = poly1;
    poly1 = newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 4;
    newNode->exp = 3;
    newNode->next = poly2;
    poly2 = newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 3;
    newNode->exp = 1;
    newNode->next = poly2;
    poly2 = newNode;

    newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->coeff = 2;
    newNode->exp = 0;
    newNode->next = poly2;
    poly2 = newNode;

    struct Node *p1 = poly1, *p2 = poly2;
    while (p1 != NULL && p2 != NULL) {
        if (p1->exp > p2->exp) {
            newNode = (struct Node*)malloc(sizeof(struct Node));
            newNode->coeff = p1->coeff;
            newNode->exp = p1->exp;
            newNode->next = result;
            result = newNode;
            p1 = p1->next;
        } else if (p1->exp < p2->exp) {
            newNode = (struct Node*)malloc(sizeof(struct Node));
            newNode->coeff = p2->coeff;
            newNode->exp = p2->exp;
            newNode->next = result;
            result = newNode;
            p2 = p2->next;
        } else {
            int sumCoeff = p1->coeff + p2->coeff;
            if (sumCoeff != 0) {
                newNode = (struct Node*)malloc(sizeof(struct Node));
                newNode->coeff = sumCoeff;
                newNode->exp = p1->exp;
                newNode->next = result;
                result = newNode;
            }
            p1 = p1->next;
            p2 = p2->next;
        }
    }

    while (p1 != NULL) {
        newNode = (struct Node*)malloc(sizeof(struct Node));
        newNode->coeff = p1->coeff;
        newNode->exp = p1->exp;
        newNode->next = result;
        result = newNode;
        p1 = p1->next;
    }

    while (p2 != NULL) {
        newNode = (struct Node*)malloc(sizeof(struct Node));
        newNode->coeff = p2->coeff;
        newNode->exp = p2->exp;
        newNode->next = result;
        result = newNode;
        p2 = p2->next;
    }

    struct Node *current = result;
    while (current != NULL) {
        if (current->coeff > 0 && current != result) {
            printf(" + ");
        }
        printf("%dx^%d", current->coeff, current->exp);
        current = current->next;
    }
    printf("\n");

    return 0;
}
