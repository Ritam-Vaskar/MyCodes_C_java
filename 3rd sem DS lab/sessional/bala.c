#include <stdio.h>
#include <stdlib.h>

#define MAX 100

int main() {
    char expr[MAX];
    char stack[MAX];
    int top = -1;
    
    printf("Enter the expression: ");
    scanf("%s", expr);
    
    for(int i = 0; expr[i] != '\0'; i++) {
        char current = expr[i];
        
        if(current == '(' || current == '{' || current == '[') {
            stack[++top] = current;
        } else if(current == ')' || current == '}' || current == ']') {
            if(top == -1) {
                printf("The parentheses are not balanced.\n");
                return 0;
            }
            char popped = stack[top--];
            if((current == ')' && popped != '(') || 
               (current == '}' && popped != '{') || 
               (current == ']' && popped != '[')) {
                printf("The parentheses are not balanced.\n");
                return 0;
            }
        }
    }
    
    if(top == -1) {
        printf("The parentheses are balanced.\n");
    } else {
        printf("The parentheses are not balanced.\n");
    }

    return 0;
}
