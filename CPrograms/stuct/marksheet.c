#include <stdio.h>

struct Student {
    char name[50];
    int roll;
    float gpa;
} student;

int main() {

    printf("Enter student name: ");
    scanf("%[^\n]s", student.name);

    printf("Enter student roll number: ");
    scanf("%d", &student.roll);

    printf("Enter student GPA: ");
    scanf("%f", &student.gpa);

    
    printf("\nStudent Details:\n");
    printf("Name: %s\n", student.name);
    printf("Roll Number: %d\n", student.roll);
    printf("GPA: %f\n", student.gpa);

    return 0;
}
