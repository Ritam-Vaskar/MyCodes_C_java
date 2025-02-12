#include <stdio.h>

struct Student {
    int rollNo;
    int semester;
    int subjects[3];
    float average;
};

// calculate average and update it
void calculateAverage(struct Student *student) {
    int sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += student->subjects[i];
    }
    student->average = (float)sum / 3.0;
}

int main() {
    
    struct Student student;

    printf("Enter student roll: ");
    scanf("%d", &student.rollNo);

    printf("Enter student semester: ");
    scanf("%d", &student.semester);

    
    for (int i = 0; i < 3; i++)
    {
        printf("Enter Number of %d Subject: ", i+1);
        scanf("%d", &student.subjects[i]);
        
    }
    
    calculateAverage(&student);

    printf("Student Details:\n");
    printf("Roll No: %d\n", student.rollNo);
    printf("Semester: %d\n", student.semester);
    printf("Subject Marks: %d, %d, %d\n", student.subjects[0], student.subjects[1], student.subjects[2]);
    printf("Average: %.2f\n", student.average);

    return 0;
}
