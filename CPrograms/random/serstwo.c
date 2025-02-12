#include <stdio.h>
int main()
{
int n, fac=1;
float sum = 0.0;
scanf("%d",&n);

for(int i=1;i<=n;i++){
    for(int j=1;j<=i;j++) {
        if(i%j==0)
        fac=fac*j;
    }
    if(i%2==1)
    sum = sum + 1.0/fac;
    else
    sum = sum + fac;

    fac = 1;
}
printf("%f",sum);
return 0;

}