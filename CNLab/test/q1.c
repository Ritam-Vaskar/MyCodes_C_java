#include <stdio.h>

struct info {
    int roll_no;
    char name[50];
    float CGPA;
};

void display(struct info *s) {
    printf("\nStudent Details:\n");
    printf("Roll No: %d\n", s->roll_no);
    printf("Name: %s\n", s->name);
    printf("CGPA: %.2f\n", s->CGPA);
}

int main() {
    struct info s1;

    printf("Enter Roll No: ");
    scanf("%d", &s1.roll_no);
    printf("Enter Name: ");
    scanf("%s", s1.name);
    printf("Enter CGPA: ");
    scanf("%f", &s1.CGPA);

    display(&s1);
    return 0;
}
