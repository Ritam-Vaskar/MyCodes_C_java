#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* last = NULL;

void insertAtEnd(int value) {
    struct Node* temp = (struct Node*)malloc(sizeof(struct Node));
    temp->data = value;

    if (last == NULL) {
        last = temp;
        last->next = last;
    } else {
        temp->next = last->next;
        last->next = temp;
        last = temp;
    }
}

void deleteNode(int key) {
    if (last == NULL) {
        printf("List is empty.\n");
        return;
    }

    struct Node *temp = last->next, *prev = last;
    if (temp->data == key) {
        if (temp == last) {
            last = NULL;
            free(temp);
            return;
        }
        last->next = temp->next;
        free(temp);
        return;
    }

    while (temp != last && temp->data != key) {
        prev = temp;
        temp = temp->next;
    }

    if (temp->data == key) {
        prev->next = temp->next;
        if (temp == last) last = prev;
        free(temp);
    } else {
        printf("Node not found.\n");
    }
}

void traverse() {
    if (last == NULL) {
        printf("List is empty.\n");
        return;
    }

    struct Node* temp = last->next;
    do {
        printf("%d -> ", temp->data);
        temp = temp->next;
    } while (temp != last->next);
    printf("\n");
}

int count() {
    if (last == NULL) return 0;

    int count = 0;
    struct Node* temp = last->next;
    do {
        count++;
        temp = temp->next;
    } while (temp != last->next);
    return count;
}

void reverse() {
    if (last == NULL) return;

    struct Node *prev = NULL, *current = last->next, *next;
    struct Node* head = last->next;
    do {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    } while (current != head);

    head->next = prev;
    last->next = prev;
    last = head;
}

void sort() {
    if (last == NULL) return;

    struct Node* current = last->next;
    struct Node* index = NULL;
    int temp;

    do {
        index = current->next;
        while (index != last->next) {
            if (current->data > index->data) {
                temp = current->data;
                current->data = index->data;
                index->data = temp;
            }
            index = index->next;
        }
        current = current->next;
    } while (current != last->next);
}

int main() {
    int choice, value;

    while (1) {
        printf("\nCircular Linked List Operations:\n");
        printf("1. Insert at End\n");
        printf("2. Delete Node\n");
        printf("3. Traverse List\n");
        printf("4. Count Nodes\n");
        printf("5. Reverse List\n");
        printf("6. Sort List\n");
        printf("7. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter value to insert: ");
                scanf("%d", &value);
                insertAtEnd(value);
                break;
            case 2:
                printf("Enter value to delete: ");
                scanf("%d", &value);
                deleteNode(value);
                break;
            case 3:
                traverse();
                break;
            case 4:
                printf("Number of nodes: %d\n", count());
                break;
            case 5:
                reverse();
                printf("List reversed.\n");
                break;
            case 6:
                sort();
                printf("List sorted.\n");
                break;
            case 7:
                exit(0);
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
