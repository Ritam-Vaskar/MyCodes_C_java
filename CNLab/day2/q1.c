// 2. Write a C program to assign values to each
// members of the following structure. Pass the
// populated structure to a function Using call-by
// address and print the value of each member of the
// structure with in that function.
// struct info{
// int roll_no;
// char name[50];
// float CGPA;
// }
#include <stdio.h>
#include <string.h>

struct info {
    int roll_no;
    char name[50];
    float CGPA;
};

void printInfo(struct info *s) {
    printf("Roll Number: %d\n", s->roll_no);
    printf("Name: %s\n", s->name);
    printf("CGPA: %.2f\n", s->CGPA);
}

int main() {
    struct info student;


    student.roll_no = 12345;
    strcpy(student.name, "Ritam Vaskar");
    student.CGPA = 8.75;

   
    printInfo(&student);

    return 0;
}