#include <stdio.h>

int main() {
    int year, day, month;

    
    printf("Enter the day and month of the date (DD MM YY): ");
    scanf("%d %d %d", &day, &month , &year);


    //day of the 1st of January
    

    long days= (year-1)*365 + (year-1)/4 - (year-1)/100 + (year-1)/400;
    int firstjan = days%7;


    // Calculate the day of the given date
    
    int totalDays = 0;
    int i = 1; 
    while (i < month) {
        if (i == 4 || i == 6 || i == 9 || i == 11) {
            totalDays += 30;
        } else if (i == 2) {
             if ((year%100==0 && year%400==0) || (year%100!=0 && year%4==0)){
                 totalDays += 29;
             }
             else {
                 totalDays += 28;
             }
        } else {
            totalDays += 31;
        }
        i++;
    }
    totalDays += day;
    

    // the day of the given date based on the day of January 1st

    int dayOfWeek = (totalDays + firstjan - 1) % 7;
    printf("The day of the given date is: ");
    switch(dayOfWeek) {
        case 0:
            printf("Monday\n");
            break;
        case 1:
            printf("Tuesday\n");
            break;
        case 2:
            printf("Wednesday\n");
            break;
        case 3:
            printf("Thursday\n");
            break;
        case 4:
            printf("Friday\n");
            break;
        case 5:
            printf("Saturday\n");
            break;
        case 6:
            printf("Sunday\n");
            break;
        default:
            printf("Invalid day\n");
            break;
    }

    return 0;
}

