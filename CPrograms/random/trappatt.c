#include<stdio.h>
int main(){

int count = 2;
for(int i = 1; i <= 3; i++) {
    for(int j = 1; j <= count; j++) {
        printf(" ");
    }
    for(int j = 1; j <= i * 2 + 1; j++) {
        printf("*");
    }
    for(int j = 1; j <= count * 2 + 1; j++) {
        printf(" ");
    }
    for(int j = 1; j <= i * 2 + 1; j++) {
        printf("*");
    }
    printf("\n");
    count--;
}
}