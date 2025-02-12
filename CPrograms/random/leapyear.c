#include<stdio.h>
int main(){
    int yr;
    printf("Enter the Year:- ");
    scanf("%d" , &yr);
    if((yr%100==0 && yr%400==0) || (yr%100!=0 && yr%4==0)) {
        printf("Leap year");
    } else {
        printf("Not a Leap Year");
    }
}