#include <stdio.h>
#include <stdlib.h>

struct stack {
    int size;
    int top;
    int* arr;
};

int isEmpty(struct stack* ptr) {
    return (ptr->top == -1);
}

int isFull(struct stack* ptr) {
    return (ptr->top == ptr->size - 1);
}

void push(struct stack* ptr, int val) {
    if (isFull(ptr)) {
        printf("Stack Overflow!\n");
    } else {
        ptr->top++;
        ptr->arr[ptr->top] = val;
    }
}

int pop(struct stack* ptr) {
    if (isEmpty(ptr)) {
        printf("Stack Underflow!\n");
        return -1;
    } else {
        int val = ptr->arr[ptr->top];
        ptr->top--;
        return val;
    }
}

int peek(struct stack* s, int i) {
    int ind = s->top - i + 1;
    if (ind < 0) {
        printf("Not a valid position for the stack\n");
        return -1;
    } else {
        return s->arr[ind];
    }
}

int main() {
    struct stack s;
    s.size = 50;
    s.top = -1;
    s.arr = (int*)malloc(s.size * sizeof(int));

    printf("Before pushing, full: %d\n", isFull(&s));
    printf("Before pushing, empty: %d\n", isEmpty(&s));

    push(&s, 1);
    push(&s, 23);
    push(&s, 99);
    push(&s, 75);
    push(&s, 3);
    push(&s, 64);
    push(&s, 57);
    push(&s, 46);
    push(&s, 89);
    push(&s, 6);

    printf("After pushing, Full: %d\n", isFull(&s));
    printf("After pushing, Empty: %d\n", isEmpty(&s));

    printf("Popped %d from the stack\n", pop(&s));
    printf("Popped %d from the stack\n", pop(&s));
    printf("Popped %d from the stack\n", pop(&s));

    for (int j = 1; j <= s.top + 1; j++) {
        printf("The value at position %d is %d\n", j, peek(&s, j));
    }

    free(s.arr);
    return 0;
}