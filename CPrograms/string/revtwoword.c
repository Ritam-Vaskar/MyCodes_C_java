#include <stdio.h>
#include <string.h>
void rev(char a[100], int start, int end)
{
    for (int s = end; s <= start; s++)
    {
        printf("%c", a[s]);
    }
    printf(" ");
}
int main()
{
    char a[100];
    scanf("%[^\n]s", a);
    int len = strlen(a);
    int end = len, start = len;
    for (int i = len; i >= -1; i--)
    {
        if (a[i] == ' ' || i == -1)
        {
            rev(a, start, end);
            start = end - 2;
            end = start;
        }
        else
        {
            end = i;
        }
    }
    return 0;
}