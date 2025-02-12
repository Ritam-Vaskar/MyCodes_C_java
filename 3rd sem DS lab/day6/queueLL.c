#include <stdio.h>
#include <stdlib.h>

struct Node{
    int data;
    struct Node* next;
};

struct Queue{
    struct Node* front;
    struct Node* rear;
};
void enqueue(struct Queue* queue, int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;

    if (queue->rear == NULL) {
        queue->front = queue->rear = newNode;
        return;
    }

    queue->rear->next = newNode;
    queue->rear = newNode;
}

int frontElement(struct Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue is empty\n");
        return -1;
    }
    return queue->front->data;
}

int dequeue(struct Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue is empty\n");
        return -1;
    }

    struct Node* temp = queue->front;
    int removedData = temp->data;
    queue->front = queue->front->next;

    if (queue->front == NULL) {
        queue->rear = NULL;
    }

    free(temp);
    return removedData;
}
void isEmpty(struct Queue *queue){
    if(queue->front==NULL){
        printf("Queue is Empty");
    }
    else{
        printf("Queue is Not Empty");
    }
}
void traverse(struct Queue *queue){
    struct Node *ptr;
    ptr= queue->front;
    while(ptr!=NULL){
        printf("%d ",ptr->data);
        ptr=ptr->next;
    }
}


void displayMenu() {
    printf("\nMenu:\n");
    printf("1. Enqueue\n");
    printf("2. Dequeue\n");
    printf("3. isEmpty\n");
    printf("4. Traverse\n");
}

int main() {
    struct Queue queue;
    queue.front=NULL;
    queue.rear=NULL;
    int choice, data;
    int count=0;
    while (1) {
        displayMenu();
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                enqueue(&queue, data);
                count++;
                break;
            case 2:
                dequeue(&queue);
                count--;
                break;
            case 3:
                isEmpty(&queue);
                break;
            case 4:
                traverse(&queue);
                printf("\nnumber of element is: %d", count);
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}