#include <stdio.h>
#include <stdlib.h>

#define MAX 5


int stack[MAX];
int top = -1;


void push();
void pop();
void peek();
void display();
void reverse();

// Push operation
void push() {
    int val;
    if (top == MAX - 1) {
        printf("Stack Overflow!\n");
    } else {
        printf("Enter value to push: ");
        scanf("%d", &val);
        top++;
        stack[top] = val;
        printf("%d pushed onto the stack.\n", val);
    }
}

// Pop operation
void pop() {
    if (top == -1) {
        printf("Stack Underflow!\n");
    } else {
        printf("Popped element: %d\n", stack[top]);
        top--;
    }
}

// Peek operation (Top Element)
void peek() {
    if (top == -1) {
        printf("Stack is empty.\n");
    } else {
        printf("Top element: %d\n", stack[top]);
    }
}

// Display stack elements
void display() {
    if (top == -1) {
        printf("Stack is empty.\n");
    } else {
        printf("Stack elements:\n");
        for (int i = top; i >= 0; i--) {
            printf("%d\n", stack[i]);
        }
    }
}

// Reverse stack
void reverse() {
    if (top == -1) {
        printf("Stack is empty. Cannot reverse.\n");
    } else {
        printf("Reversing the stack...\n");
        for (int i = 0; i < top / 2; i++) {
            int temp = stack[i];
            stack[i] = stack[top - i];
            stack[top - i] = temp;
        }
        printf("Stack reversed.\n");
    }
}

int main() {
    int choice;
    
    while (1) {
        printf("\nStack Operations Menu:\n");
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Peek (Top Element)\n");
        printf("4. Display Stack\n");
        printf("5. Reverse Stack\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1: push(); break;
            case 2: pop(); break;
            case 3: peek(); break;
            case 4: display(); break;
            case 5: reverse(); break;
            case 6: exit(0); break;
            default: printf("Invalid choice! Please try again.\n");
        }
    }
    return 0;
}
