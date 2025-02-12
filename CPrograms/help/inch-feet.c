#include <stdio.h>

struct add {
    int inch;
    int feet;
} input1,input2,sum;

int main(){
    printf("Enter first: ");
    scanf("%d %d", &input1.feet , &input1.inch);
    printf("Enter second no.: ");
    scanf("%d %d", &input2.feet , &input2.inch);
    sum.feet=input1.feet+input2.feet;
    sum.inch=input1.inch+input2.inch;
    if(sum.inch>=12){
        sum.feet++;
        sum.inch-=12;
    }
    printf("addition is %d feet %d inch",sum.feet,sum.inch);

}