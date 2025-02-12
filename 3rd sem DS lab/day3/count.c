#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* createNode(int data) {
    struct Node* new = (struct Node*)malloc(sizeof(struct Node));
    new->data = data;
    new->next = NULL;
    return new;
}

void insert(struct Node** head, int data, int position) {
    struct Node* new = createNode(data);

    if (position == 1) {
        new->next = *head;
        *head = new;
        return;
    }

    struct Node* temp = *head;

    for (int i = 1; i < position - 1 && temp != NULL; i++) {
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Position out of bounds.\n");
        free(new);
    } else {
        new->next = temp->next;
        temp->next = new;
    }
}

int count(struct Node* head) {
    int count = 0;
    struct Node* current = head;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}

int main() {
    struct Node* head = NULL;
    insert(&head, 1, 1);
    insert(&head, 2, 2);
    insert(&head, 3, 3);
    insert(&head, 4, 4);

    printf("Number of nodes: %d\n", count(head));

    while (head != NULL) {
        struct Node* temp = head;
        head = head->next;
        free(temp);
    }

    return 0;
}

#include <stdio.h>
#include <stdlib.h>

// Define the structure for a node in the doubly linked list
struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
};

// Function to insert a new node at any given position in the doubly linked list
void insertAtPosition(struct Node** head, int data, int position) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    newNode->prev = NULL;

    // If inserting at the head (position 1)
    if (position == 1) {
        newNode->next = *head;
        if (*head != NULL) {
            (*head)->prev = newNode;
        }
        *head = newNode;
        return;
    }

    struct Node* temp = *head;
    int currentPos = 1;

    // Traverse to the position where the new node will be inserted
    while (temp != NULL && currentPos < position - 1) {
        temp = temp->next;
        currentPos++;
    }

    // If temp is NULL, the position is out of bounds
    if (temp == NULL) {
        printf("Position out of bounds.\n");
        free(newNode);
        return;
    }

    // Insert the new node
    newNode->next = temp->next;
    if (temp->next != NULL) {
        temp->next->prev = newNode;
    }
    temp->next = newNode;
    newNode->prev = temp;
}

// Function to display the doubly linked list
void displayList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

// Main function to test the insertAtPosition function
int main() {
    struct Node* head = NULL;

    // Inserting nodes at different positions
    insertAtPosition(&head, 10, 1);  // List: 10
    insertAtPosition(&head, 20, 2);  // List: 10 20
    insertAtPosition(&head, 30, 3);  // List: 10 20 30
    insertAtPosition(&head, 15, 2);  // List: 10 15 20 30
    insertAtPosition(&head, 25, 4);  // List: 10 15 20 25

