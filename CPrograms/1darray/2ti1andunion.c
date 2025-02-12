#include <stdio.h>
void Union(int fac1[], int fac2[], int c, int c1)
{
    for(int i = 0; i < c; i++) {
        printf("%d ", fac1[i]);
    }
    printf("\n");
    for(int i = 0; i < c1; i++) {
        printf("%d ", fac2[i]);
    }
    printf("\n");
    int count = c;
    for (int i = 0; i < c1; i++)
    {
        int flag = 1;
        for (int j = 0; j < c; j++)
        {
            if (fac2[i] == fac1[j])
            {
                flag = 0;
                break;
            }
        }
        if (flag == 1)
        {
            count++;
        }
    }

    printf("%d\n", count);
    int fac3[count];
    int k = 0;
    for (int i = 0; i < c; i++)
    {
        fac3[k] = fac1[i];
        k++;
    }
    for (int i = 0; i < c1; i++)
    {
        int f = 1;
        for (int j = 0; j < c; j++)
        {
            if (fac2[i] == fac1[j])
            {
                f = 0;
                break;
            }
        }
        if (f == 1)
        {
            fac3[k] = fac2[i];
            k++;
        }
    }

    //sorting
    int temp;
    for(int i=0;i<count-1;i++)
    {
        for(int j=0;j<count-i-1;j++)
        {
            if(fac3[j]>fac3[j+1])
            {
                temp=fac3[i];
                fac3[i]=fac3[j];
                fac3[j]=temp;
            }
        }
    }
    for (int i = 0; i < count; i++)
    {
        printf("%d ", fac3[i]);
    }
}
int main()
{
    printf("enter two numbers: ");
    int a, b;
    scanf("%d%d", &a, &b);

    int c = 0;

    for (int i = 1; i <= a; i++)
    {
        if (a % i == 0)
        {
            c++;
        }
    }

    int fac1[c];
    int j = 0;

    for (int i = 1; i <= a; i++)
    {
        if (a % i == 0)
        {
            fac1[j] = i;
            j++;
        }
    }

    int c1 = 0;

    for (int i = 1; i <= b; i++)
    {
        if (b % i == 0)
        {
            c1++;
        }
    }

    int k = 0;
    int fac2[c1];
    for (int i = 1; i <= b; i++)
    {
        if (b % i == 0)
        {
            fac2[k] = i;
            k++;
        }
    }

    Union(fac1, fac2, c, c1);
    return 0;
}