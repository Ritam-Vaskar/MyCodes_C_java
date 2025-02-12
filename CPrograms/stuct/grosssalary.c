#include<stdio.h>

struct employee
{
    int empid;
    char name[100];
    float basicsalary;
};

float cal(struct employee E1,struct employee E2,struct employee E3)
{
    float DA1,HRA1,GrossSalary1;
    float DA2,HRA2,GrossSalary2;
    float DA3,HRA3,GrossSalary3;

    DA1=(0.1*E1.basicsalary);
    DA2=(0.1*E2.basicsalary);
    DA3=(0.1*E3.basicsalary);

    HRA1=(0.2*E1.basicsalary);
    HRA2=(0.2*E2.basicsalary);
    HRA3=(0.2*E3.basicsalary);

    GrossSalary1=(DA1)+(HRA1)+E1.basicsalary;
    GrossSalary2=(DA2)+(HRA2)+E2.basicsalary;
    GrossSalary3=(DA3)+(HRA3)+E3.basicsalary;

    printf("ID\tName\tBasicSalary\tGrossSalary \n");
    printf ("%d\t%s\t%f\t%f \n" , E1.empid,E1.name,E1.basicsalary,GrossSalary1 );
    printf ("%d\t%s\t%f\t%f \n" , E2.empid,E2.name,E2.basicsalary,GrossSalary2 );
    printf ("%d\t%s\t%f\t%f \n" , E3.empid,E3.name,E3.basicsalary,GrossSalary3 );

}

int main()
{
    struct employee E1,E2,E3;
    printf("enter the 1st employee details:");

    scanf("%d%s%f",&E1.empid,E1.name,&E1.basicsalary);

    printf("enter the 2nd employee details:");
    scanf("%d%s%f",&E2.empid,E2.name,&E2.basicsalary);

    printf("enter the 3rd employee details:");
    scanf("%d%s%f",&E3.empid,E3.name,&E3.basicsalary);

    cal(E1,E2,E3);

    return 0;
}