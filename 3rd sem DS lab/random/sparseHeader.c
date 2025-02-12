#include <stdio.h>
#include <stdlib.h>

struct Node {
    int row;
    int col;
    int value;
    struct Node* next;
};

struct Node* createNode(int row, int col, int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->row = row;
    newNode->col = col;
    newNode->value = value;
    newNode->next = NULL;
    return newNode;
}

void insertNode(struct Node** head, int row, int col, int value) {
    struct Node* newNode = createNode(row, col, value);

    if (*head == NULL) {
        *head = newNode;
    } else {
        struct Node* temp = *head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = newNode;
    }
}

void convertToSparseMatrix(int matrix[100][100], int totalRows, int totalCols, struct Node** head) {
    for (int i = 0; i < totalRows; i++) {
        for (int j = 0; j < totalCols; j++) {
            if (matrix[i][j] != 0) {
                insertNode(head, i, j, matrix[i][j]);
            }
        }
    }
}


void displaySparseMatrix(struct Node* head, int totalRows, int totalCols) {
    struct Node* temp = head;
    for (int i = 0; i < totalRows; i++) {
        for (int j = 0; j < totalCols; j++) {
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


void displayLinkedList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("Row: %d, Column: %d, Value: %d\n", temp->row, temp->col, temp->value);
        temp = temp->next;
    }
}

// Function to display the 3-tuple representation
void displayThreeTuple(struct Node* head) {
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
    int totalRows, totalCols;
    struct Node* head = NULL;

    
    printf("Enter the number of rows in the matrix: ");
    scanf("%d", &totalRows);
    printf("Enter the number of columns in the matrix: ");
    scanf("%d", &totalCols);

    
    printf("Enter the elements of the matrix:\n");
    for (int i = 0; i < totalRows; i++) {
        for (int j = 0; j < totalCols; j++) {
            scanf("%d", &matrix[i][j]);
        }
    }

    convertToSparseMatrix(matrix, totalRows, totalCols, &head);

 
    printf("\nSparse Matrix Representation:\n");
    displaySparseMatrix(head, totalRows, totalCols);

 
    printf("\nLinked List Representation:\n");
    displayLinkedList(head);

    //3-tuple 
    displayThreeTuple(head);

    return 0;
}
