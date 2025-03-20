#include <stdio.h>
#include <stdlib.h>


struct Node {
    int data;
    struct Node* next;
};

struct Node* last = NULL;

void insertEnd(int value) {

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


int main() {
    int value;
    insertEnd(10);
    insertEnd(20);
    insertEnd(30);
    insertEnd(40);
    printf("Circular Singly Linked List: ");

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

    return 0;
}
