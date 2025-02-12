#include<stdio.h>
#include<string.h>
int main()
{
    char a[100];
    char c1,c2;
    int i;
    printf("Enter a string: ");
    scanf("%[^\n]s",a);
    printf("Enter a character: ");
    scanf(" %c",&c1);
    printf("Enter a character to replace in place of c1:");
    scanf(" %c",&c2);
    
    int length = 0;
    while (a[length] != '\0') {
        length++;
    }
    
        for(i=0;i<=length;i++)
        {
            if(a[i]==c1)
            {
                a[i]=c2;
            }
        }
        printf("the string is: %s",a);
        return 0;


}