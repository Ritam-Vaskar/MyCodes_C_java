
#include <stdio.h>

int main() {
   int year;
   printf("Enter Year:- ");
   scanf("%d" , &year);

   long days= (year-1)*365 + (year-1)/4 - (year-1)/100 + (year-1)/400;

   int remday = days%7;


   if (remday == 0)
   {
    printf("The day is Monday \n");
    printf("Number of Friday in this year is 52");
   }


   if (remday == 1)
   {
    printf("The day is Tuesday \n");
    printf("Number of Friday in this year is 52");
   }


   if (remday == 2)
   {
    printf("The day is Wednesday \n");
    printf("Number of Friday in this year is 52");
   }



   if (remday == 3)
   {
    printf("The day is Thursday \n");

    if ((year%100==0 && year%400==0) || (year%100!=0 && year%4==0))
    {
        printf("Number of Friday in this year is 53");
    }
    else{
        printf("Number of Friday in this year is 52");
    }
   }



   if (remday == 4)
   {
    printf("The day is Friday \n");
    printf("Number of Friday in this year is 53");
    }
    
   

   if (remday == 5)
   {
    printf("The day is Saturday \n");
    printf("Number of Friday in this year is 52");
   }
   

   if (remday == 6)
   {
    printf("The day is Sunday \n");
    printf("Number of Friday in this year is 52");
   }
   
}