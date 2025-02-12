#include <stdio.h>
#include <string.h>

struct Person {
    char name[50];
    float height;
};


void swap(struct Person *a, struct Person *b) {
    struct Person temp = *a;
    *a = *b;
    *b = temp;
}


void sort(struct Person arr[], int n) {
    int i, j;
    for (i = 0; i < n-1; i++) {
        for (j = 0; j < n-i-1; j++) {
            if (arr[j].height < arr[j+1].height) {
                swap(&arr[j], &arr[j+1]);
            }
        }
    }
}

int main() {
    int n, i;
    
    printf("Enter the number of people: ");
    scanf("%d", &n);

    struct Person people[n];

    
    for (i = 0; i < n; i++) {
        printf("Enter name and height for person %d: ", i+1);
        scanf("%s %f", people[i].name, &people[i].height);
    }

    
    sort(people, n);

   
    printf("\nSorted list :\n");
    for (i = 0; i < n; i++) {
        printf("%s - %.2f\n", people[i].name, people[i].height);
    }

    return 0;
}
