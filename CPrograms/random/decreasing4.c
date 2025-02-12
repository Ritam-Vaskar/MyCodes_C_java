#include <stdio.h>

int main() {
    
//     int a, b, c, d;

//     // Input from the user
//     printf("Enter the first number: ");
//     scanf("%d", &a);

//     printf("Enter the second number: ");
//     scanf("%d", &b);

//     printf("Enter the third number: ");
//     scanf("%d", &c);

//     printf("Enter the fourth number: ");
//     scanf("%d", &d);

    
//     if (a < b) {
//         int temp = a;
//         a = b;
//         b = temp;
//     }

//     if (b < c) {
//         int temp = b;
//         b = c;
//         c = temp;
//     }

//     if (c < d) {
//         int temp = c;
//         c = d;
//         d = temp;
//     }

//     if (a < b) {
//         int temp = a;
//         a = b;
//         b = temp;
//     }

    
//     printf("Fourth , Third , Second & Most Minimum numbers consecutivly are: %d, %d, %d, %d\n", a, b, c, d);

//     return 0;
// 

    int a, b, c, d, first, second, third, fourth;
    printf("Enter the first number: ");
    scanf("%d", &a);

    printf("Enter the second number: ");
    scanf("%d", &b);

    printf("Enter the third number: ");
    scanf("%d", &c);

    printf("Enter the fourth number: ");
    scanf("%d", &d);

    if ((a < b) && (c < d))
    {
        if ((a < c) && (a < d))
        {
            first = a;
        }
    }
    else if ((a < b) && (c > d))
    {
        
    }
    else if ((a > b) && (c < d))
    {
        
    }
    else if ((a > b) && (c > d))
    {
        
    }
    else if ((a < c) && (b < d))
    {
        
    }
    else if ((a < c) && (b > d))
    {
        
    }
return 0;
}