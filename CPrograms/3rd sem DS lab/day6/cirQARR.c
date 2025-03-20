#include <stdio.h>
#include <stdbool.h>

struct Queue {
    int data[5];
    int front;
    int rear;
    int size;
};

void isEmpty(struct Queue* q) {
    if(q->size == 0) {
        printf("Queue is empty\n");
    }
    return;
}

bool isFull(struct Queue* q) {
    return q->size == 5;
}

void enqueue(struct Queue* q, int data) {
    if (isFull(q)) {
        printf("Queue is full\n");
        return;
    }
    if (q->rear == -1) { 
        q->front = q->rear = 0;
    } else {
        q->rear = (q->rear + 1) % 5;
    }
    q->data[q->rear] = data;
    q->size++;
}

int dequeue(struct Queue* q) {
    if(q->front == -1 && q->rear == -1) {
        printf("Queue is empty\n");
        return -1;
    }
    int removedData = q->data[q->front];
    if (q->front == q->rear) { 
        q->front = q->rear = -1;
    } else {
        q->front = (q->front + 1) % 5;
    }
    q->size--;
    return removedData;
}

int frontElement(struct Queue* q) {
    if (q->front == -1) {
        printf("Queue is empty\n");
        return -1;
    }
    return q->data[q->front];
}

void printQueue(struct Queue* q) {
    if (q->front == -1) {
        printf("Queue is empty\n");
        return;
    }
    int i = q->front;
    for (int j = 0; j < q->size; j++) {
        printf("%d ", q->data[i]);
        i = (i + 1) % 5;
    }
    printf("\n");
}

void checkFull(struct Queue* q) {
    if (q->size == 5) {
        printf("Queue is full\n");
    } else {
        printf("Queue is not full\n");
    }
}

void displayMenu() {
    printf("Queue Operations Menu\n");
    printf("1. Check if queue is empty\n");
    printf("2. Enqueue\n");
    printf("3. Dequeue\n");
    printf("4. Get front element\n");
    printf("5. Print queue\n");
    printf("6. Check if queue is full\n");
    printf("7. Exit\n");
    printf("Enter your choice: ");
}

int main() {
    struct Queue* q;
    q->front = -1; 
    q->rear = -1;
    q->size = 0;

    int choice;
    int data;

    while (1) {
        displayMenu();
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                isEmpty(&q);
                break;
            case 2:
                printf("Enter element to enqueue: ");
                scanf("%d", &data);
                enqueue(&q, data);
                break;
            case 3:
                printf("Dequeued element is: %d\n", dequeue(&q));
                break;
            case 4:
                printf("Front element is: %d\n", frontElement(&q));
                break;
            case 5:
                printQueue(&q);
                break;
            case 6:
                checkFull(&q);
                break;
            case 7:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}