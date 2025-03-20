#include <stdio.h>

int stack[100];
int top = -1; 


void push(int value) {
    if (top >= 100 - 1) {
        printf("Stack Overflow\n");
    } else {
        top++;
        stack[top] = value;
        printf("%d pushed to stack\n", value);
    }
}


int pop() {
    if (top == -1) {
        printf("Stack Underflow\n");
        return -1; 
    } else {
        int value = stack[top];
        top--;
        printf("%d popped from stack\n", value);
        return value;
    }
}


int peek() {
    if (top == -1) {
        printf("Stack is empty\n");
        return -1;
    } else {
        return stack[top];
    }
}


int isEmpty() {
    return top == -1;
}


int main() {
    push(10);
    push(20);
    push(30);

    printf("Top element is %d\n", peek());

    pop();
    pop();

    if (isEmpty()) {
        printf("Stack is empty\n");
    } else {
        printf("Stack is not empty\n");
    }

    return 0;
}
