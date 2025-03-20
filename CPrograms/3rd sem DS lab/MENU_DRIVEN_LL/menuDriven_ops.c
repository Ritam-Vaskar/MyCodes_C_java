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

//insert at any pos
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

// delete a node at position
void delete(struct Node** head, int position) {
    if (*head == NULL) {
        printf("List is empty.\n");
        return;
    }

    struct Node* temp = *head;

    if (position == 1) {
        *head = temp->next;
        free(temp);
        return;
    }

    struct Node* prev = NULL;
    for (int i = 1; i < position && temp != NULL; i++) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Position out of bounds.\n");
    } else {
        prev->next = temp->next;
        free(temp);
    }
}

//count nodes
int count(struct Node* head) {
    int count = 0;
    while (head != NULL) {
        count++;
        head = head->next;
    }
    return count;
}

//traverse
void traverse(struct Node* head) {
    if (head == NULL) {
        printf("List is empty.\n");
        return;
    }

    while (head != NULL) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}

// search
void search(struct Node* head, int key) {
    int position = 1;
    while (head != NULL) {
        if (head->data == key) {
            printf("Element %d found at position %d\n", key, position);
            return;
        }
        head = head->next;
        position++;
    }
    printf("Element %d not found in the list.\n", key);
}

// sort
void sort(struct Node** head) {
    struct Node* current = *head;
    struct Node* index = NULL;
    int temp;

    if (*head == NULL) {
        return;
    }

    while (current != NULL) {
        index = current->next;

        while (index != NULL) {
            if (current->data > index->data) {
                temp = current->data;
                current->data = index->data;
                index->data = temp;
            }
            index = index->next;
        }
        current = current->next;
    }
}

//reverse
void reverse(struct Node** head) {
    struct Node* prev = NULL;
    struct Node* current = *head;
    struct Node* next = NULL;

    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    *head = prev;
}

//menu
void displayMenu() {
    printf("\nMenu:\n");
    printf("1. Insert a node at specific position\n");
    printf("2. Deletion of an element from specific position\n");
    printf("3. Count nodes\n");
    printf("4. Traverse the linked list\n");
    printf("5. Search an element in the list\n");
    printf("6. Sort the list in ascending order\n");
    printf("7. Reverse the list\n");
    printf("8. Exit\n");
}

int main() {
    struct Node* head = NULL;
    int choice, data, position;

    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                printf("Enter position to insert: ");
                scanf("%d", &position);
                insert(&head, data, position);
                break;
            case 2:
                printf("Enter position to delete: ");
                scanf("%d", &position);
                delete(&head, position);
                break;
            case 3:
                printf("Number of nodes: %d\n", count(head));
                break;
            case 4:
                traverse(head);
                break;
            case 5:
                printf("Enter element to search: ");
                scanf("%d", &data);
                search(head, data);
                break;
            case 6:
                sort(&head);
                printf("List sorted.\n");
                break;
            case 7:
                reverse(&head);
                printf("List reversed.\n");
                break;
            case 8:
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
