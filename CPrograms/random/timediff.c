#include<stdio.h>

int main()
{
    //starting time

    printf("enter the starting hour,minutes and seconds:- ");
    int start_hour,start_minutes,start_seconds;
    scanf("%d : %d : %d",&start_hour,&start_minutes,&start_seconds);

    //ending time

    printf("enter the ending hour,minutes and seconds:- ");
    int end_hour,end_minutes,end_seconds;
    scanf("%d : %d : %d",&end_hour,&end_minutes,&end_seconds);

    int hour_diff,minute_diff,second_diff;


    if (end_hour <= start_hour) 
    {
        hour_diff=start_hour-end_hour;
        minute_diff=start_minutes-end_minutes;
        second_diff=start_seconds-end_seconds;

        if(second_diff<0)
        {
            second_diff+=60;
            minute_diff--;
        }
        if(minute_diff<0)
        {
            minute_diff+=60;
            hour_diff--;
        }
    }

    if (end_hour > start_hour) 
    {
        hour_diff=end_hour-start_hour;
        minute_diff=end_minutes-start_minutes;
        second_diff=end_seconds-start_seconds;

        if(second_diff<0)
        {
            second_diff+=60;
            minute_diff--;
        }
        if(minute_diff<0)
        {
            minute_diff+=60;
            hour_diff--;
        }
    }

    
    
    printf("the difference in time is:- ");
    printf("%d : %d : %d",hour_diff,minute_diff,second_diff);
    return 0;
}