#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* mergeAndSort(struct Node* head1, struct Node* head2) {
    struct Node* merged = NULL;
    struct Node* tempMerged = NULL;

    while (head1 != NULL && head2 != NULL) {
        struct Node* newNode = NULL;
        
        if (head1->data < head2->data) {
            newNode = head1;
            head1 = head1->next;
        } else {
            newNode = head2;
            head2 = head2->next;
        }

        if (merged == NULL) {
            merged = newNode;
            tempMerged = merged;
        } else {
            tempMerged->next = newNode;
            tempMerged = tempMerged->next;
        }
    }

    if (head1 != NULL) {
        tempMerged->next = head1;
    } else if (head2 != NULL) {
        tempMerged->next = head2;
    }

    return merged;
}

int main() {
    struct Node *head1 = NULL, *head2 = NULL, *temp1, *temp2, *merged;
    int n1, n2, data, i;

    printf("Enter the number of nodes in the first linked list: ");
    scanf("%d", &n1);
    printf("Enter the elements of the first linked list in sorted order: ");
    for (i = 0; i < n1; i++) {
        struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
        scanf("%d", &data);
        newNode->data = data;
        newNode->next = NULL;

        if (head1 == NULL) {
            head1 = newNode;
        } else {
            temp1 = head1;
            while (temp1->next != NULL)
                temp1 = temp1->next;
            temp1->next = newNode;
        }
    }

    printf("Enter the number of nodes in the second linked list: ");
    scanf("%d", &n2);
    printf("Enter the elements of the second linked list in sorted order: ");
    for (i = 0; i < n2; i++) {
        struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
        scanf("%d", &data);
        newNode->data = data;
        newNode->next = NULL;

        if (head2 == NULL) {
            head2 = newNode;
        } else {
            temp2 = head2;
            while (temp2->next != NULL)
                temp2 = temp2->next;
            temp2->next = newNode;
        }
    }

    merged = mergeAndSort(head1, head2);

    printf("Merged and sorted linked list: ");
    temp1 = merged;
    while (temp1 != NULL) {
        printf("%d -> ", temp1->data);
        temp1 = temp1->next;
    }
    printf("NULL\n");

    return 0;
}
