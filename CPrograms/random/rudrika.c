#include <stdio.h>

int main() {
//     int n, i = 1, term = 7;

//     printf("Enter the number of terms: ");
//     scanf("%d", &n);

//     printf("Series:1 2 ");
//     while (i <= n-2) {
//         printf("%d ", term);
//         term = term * 2 + 1;
//         i++;
//     }

//     return 0;
// }
int n;
int yr;
scanf("%d",&n);
int dayOfWeek = n;
    printf("The day of the given date is: ");
    switch(dayOfWeek) {
        case 0:
            
        case 3:
            
        case 5: printf("31");
        break;
            
        case 2:
            
            printf("Enter the Year:- ");
            scanf("%d" , &yr);
            if((yr%100==0 && yr%400==0) || (yr%100!=0 && yr%4==0)) {
                printf("29");
            } else {
                printf("28");
            }
            break;
        case 4:
            printf("Friday\n");
           // break;
        case 7:
            printf("Saturday\n");
           // break;
        case 6:
            printf("Sunday\n");
           // break;
        default:
            printf("Invalid day\n");
           // break;
    }

    return 0;
}