#include<stdio.h>
#include<stdlib.h>

struct Queue {
    int data[5];
    int front;
    int rear;
    int size;
};

void insert(struct Queue* q, int data) {
    if (q->size == 5) {
        printf("Queue is full\n");
    } else {
        if (q->front == -1) {
            q->front = q->rear = 0;
        } else {
            q->rear = (q->rear + 1) % 5;
        }
        q->data[q->rear] = data;
        q->size++;
    }
}

void delete(struct Queue* q) {
    if (q->size == 0) {
        printf("Queue is empty\n");
    } else {
        if (q->front == q->rear) {
            q->front = q->rear = -1;
        } else {
            q->front = (q->front + 1) % 5;
        }
        q->size--;
    }
}

int main() {
    struct Queue q;
    q.front = q.rear = -1;
    q.size = 0;

    insert(&q, 10);
    insert(&q, 20);
    insert(&q, 30);
    insert(&q, 40);
    insert(&q, 50);
    insert(&q, 60);

    delete(&q);
    delete(&q);

    if (q.size == 0) {
        printf("Queue is empty\n");
    } else {
        int i = q.front;
        while (i != q.rear) {
            printf("%d ", q.data[i]);
            i = (i + 1) % 5;
        }
        printf("%d\n", q.data[q.rear]);
    }

    return 0;
}
