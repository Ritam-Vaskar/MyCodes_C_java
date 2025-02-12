#include<stdio.h>
int main()
{
char a[100],c;
int i;
scanf("%[^\n]s",a);
printf("The original string is\n%s",a);
for(i=0;a[i]!= '\0';i++);
for(int s=0,e=i-1;s<e;s++,e--)
{
c=a[s];
a[s]=a[e];
a[e]=c;
}
printf("The reversed string is:\n%s",a);
return 0;
}