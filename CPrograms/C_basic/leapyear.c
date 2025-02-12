#include<stdio.h>
int main(){

    int year;
    printf("Enter the Year: ");

    scanf("%d",&year);

    if(year%100==0 && year%400==0) {
        printf("Leap Year");

        
    }

    

    else {

        if(year%100!=0 && year%4==0) {
            printf("Leap Year");
        }

        else{
            printf("Not A Leap Year");

        }
        
    }
    
}