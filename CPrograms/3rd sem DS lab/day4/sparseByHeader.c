#include <stdio.h>
#include <stdlib.h>

struct Node {
    int row;
    int col;
    int value;
    struct Node* next;
};

struct Node* create(int row, int col, int value) {
    struct Node* new = (struct Node*)malloc(sizeof(struct Node));
    new->row = row;
    new->col = col;
    new->value = value;
    new->next = NULL;
    return new;
}

void insert(struct Node** head, int row, int col, int value) {
    struct Node* new = create(row, col, value);

    if (*head == NULL) {
        *head = new;
    } else {
        struct Node* temp = *head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = new;
    }
}

void convert(int matrix[100][100], int rows, int cols, struct Node** head) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (matrix[i][j] != 0) {
                insert(head, i, j, matrix[i][j]);
            }
        }
    }
}


void display(struct Node* head, int rows, int cols) {
    struct Node* temp = head;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (temp != NULL && temp->row == i && temp->col == j) {
                printf("%d ", temp->value);
                temp = temp->next;
            } else {
                printf("0 ");
            }
        }
        printf("\n");
    }
}


void print(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("Row: %d, Column: %d, Value: %d\n", temp->row, temp->col, temp->value);
        temp = temp->next;
    }
}


void tuple(struct Node* head) {
    printf("\n3-Tuple Representation:\n");
    printf("Row  Column  Value\n");
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d     %d      %d\n", temp->row, temp->col, temp->value);
        temp = temp->next;
    }
}


int main() {
    int matrix[100][100];
    int rows, cols;
    struct Node* head = NULL;

    
    printf("Enter the number of rows in the matrix: ");
    scanf("%d", &rows);
    printf("Enter the number of columns in the matrix: ");
    scanf("%d", &cols);

    
    printf("Enter the elements of the matrix:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            scanf("%d", &matrix[i][j]);
        }
    }

    convert(matrix, rows, cols, &head);

 
    printf("\nSparse Matrix Representation:\n");
    display(head, rows, cols);

 
    printf("\nLinked List Representation:\n");
    print(head);

    
    tuple(head);

    return 0;
}
