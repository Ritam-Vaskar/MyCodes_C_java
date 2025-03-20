#include <stdio.h>
#include <stdlib.h>

struct Employee {
    int id;
    char name[50]; 
    float bs; 
    int hra; 
    int da; 
};

// Function to calculate gross salary
float GS(struct Employee emp) {
    return emp.bs + (emp.bs * emp.hra / 100) + (emp.bs * emp.da / 100);
}

// Function to display employee information
void displayEmployeeInfo(struct Employee emp) {
    float grossSalary = GS(emp);
    printf("Employee ID: %d\n", emp.id);
    printf("Employee Name: %s\n", emp.name);
    printf("Basic Salary: %.2f\n", emp.bs);
    printf("HRA: %d\n", emp.hra);
    printf("DA: %d\n", emp.da);
    printf("Gross Salary: %.2f\n", grossSalary);
}

int main() {
    int n;
    printf("Enter number of employees: ");
    scanf("%d", &n);

    struct Employee *employees = (struct Employee *) malloc(n * sizeof(struct Employee));
    if (employees == NULL) {
        printf("Memory allocation failed");
        return 1;
    }

    // Input employee details
    for (int i = 0; i < n; i++) {
        printf("Enter Employee ID: ");
        scanf("%d", &employees[i].id);
        printf("Enter Employee Name: ");
        scanf("%s", employees[i].name);
        printf("Enter Basic Salary: ");
        scanf("%f", &employees[i].bs);
        printf("Enter HRA: ");
        scanf("%d", &employees[i].hra);
        printf("Enter DA: ");
        scanf("%d", &employees[i].da);
    }

    // Display employee information
    for (int i = 0; i < n; i++) {
        displayEmployeeInfo(employees[i]);
    }

    free(employees); // Free the allocated memory
    return 0;
}
