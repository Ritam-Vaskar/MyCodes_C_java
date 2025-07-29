#include <stdio.h>
#include <stdlib.h>

int gcd(int a, int b)
{
    if (b == 0)
        return a;
    else
        return gcd(b, a % b);
}

int main()
{
    FILE *fp1, *fp2;
    int a, b;

    fp1 = fopen("D:\\DAA_1246\\lab2\\input2.txt", "r");
    if (fp1 == NULL)
    {
        printf("error: could not open the input file\n");
        return 1;
    }

    fp2 = fopen("D:\\DAA_1246\\lab2\\output2.txt", "w");
    if (fp2 == NULL)
    {
        printf("error: could not open the output file\n");
        fclose(fp1);
        return 1;
    }

    while (fscanf(fp1, "%d %d", &a, &b) == 2)
    {
        int result = gcd(a, b);
        fprintf(fp2, "GCD of %d and %d is %d\n", a, b, result);
        printf("GCD of %d and %d is %d\n", a, b, result);
    }

    fclose(fp1);
    fclose(fp2);

    return 0;
}
