#include <stdio.h>
#include <string.h>

struct Book {
    char title[100];
    char author[100];
    char publication[100];
    float price;
};

void displayBooksByAuthor(struct Book books[], int n, char *author) {
    printf("Books by %s:\n", author);
    for (int i = 0; i < n; i++) {
        if (strcmp(books[i].author, author) == 0) {
            printf("Title: %s\n", books[i].title);
            printf("Author: %s\n", books[i].author);
            printf("Publication: %s\n", books[i].publication);
            printf("Price: %.2f\n", books[i].price);
            printf("\n");
        }
    }
}

int main() {
    int n;
    printf("Enter the number of books: ");
    scanf("%d", &n);
    
    if (n > 100) {
        printf("Maximum number of books exceeded.\n");
        return 1;
    }
    
    struct Book books[100];
    
    for (int i = 0; i < n; ++i) {
        printf("Enter details for book %d:\n", i + 1);
        printf("Title: ");
        scanf("%s", books[i].title);
        printf("Author: ");
        scanf("%s", books[i].author);
        printf("Publication: ");
        scanf("%s", books[i].publication);
        printf("Price: ");
        scanf("%f", &books[i].price);
    }
    
    char author[100];
    printf("Enter author's name to display their books: ");
    scanf("%s", author);
    
    displayBooksByAuthor(books, n, author);
    
    return 0;
}