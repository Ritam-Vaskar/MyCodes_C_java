#include <stdio.h>

int main() {
    printf("Enter a number : ");
    int n;
    scanf("%d", &n);

    int pow = 1;
    for(int i = 1; i <= n / 2; i++) {
        pow *= 10;

        
    }
    int firstNum = (n / pow) % 10;
    int secondNum = (n % pow) / 10;
    printf("The two middle numbers are %d && %d", firstNum, secondNum);

    // int count = 0;
    // int copy = n;
    // while(copy != 0) {
    //     copy /= 10;
    //     count++;
    // }

    // if(count % 2 == 0) {
    //     int firstNum = (n / pow) % 10;
    //     int secondNum = (n % pow) / 10;
    //     printf("The two middle numbers are %d && %d", firstNum, secondNum);
    // } else {
    //     int middle = (n / pow) % 10;
    //     printf("The two middle numbers are %d", middle);
    // }

    return 0;
}