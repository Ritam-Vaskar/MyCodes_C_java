#include <stdio.h>

int main() {
    int d1, m1, y1; // First date
    int d2, m2, y2; // Second date
    int days_in_month[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}; // Days in each month

    // Input for the first date
    printf("Enter first date (DD MM YYYY): ");
    scanf("%d %d %d", &d1, &m1, &y1);

    // Input for the second date
    printf("Enter second date (DD MM YYYY): ");
    scanf("%d %d %d", &d2, &m2, &y2);

    // Function to check if the year is a leap year
    #define IS_LEAP_YEAR(year) (((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0))

    // Function to calculate the number of days in a given date
    #define DAYS_IN_DATE(day, month, year) ((year - 1) * 365 + (year - 1) / 4 - (year - 1) / 100 + (year - 1) / 400 + (day + (153 * month + 8) / 5))

    // Calculate the number of days for each date
    int days1 = DAYS_IN_DATE(d1, m1, y1);
    int days2 = DAYS_IN_DATE(d2, m2, y2);

    // Calculate the difference between the two dates
    int difference = days2 - days1;

    // Adjust for leap years between the two dates
    for (int i = y1; i < y2; i++) {
        if (IS_LEAP_YEAR(i))
            difference++;
    }

    // Output the result
    printf("Number of days between the two dates: %d\n", difference);

    return 0;
}
