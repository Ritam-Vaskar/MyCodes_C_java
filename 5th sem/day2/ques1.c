#include <stdio.h>
#include <stdlib.h>

int convert(int n)
{
    if (n == 0)
    {
        return 0;
    }
    else
    {
        return (n % 2) + 10 * convert(n / 2);
    }
}

int main()
{
    FILE *fp1, *fp2;
    int number, n, count = 0;

    fp1 = fopen("D:\\DAA_1246\\lab2\\input1.txt", "r");
    if (fp1 == NULL)
    {
        printf("error : could not open the input file \n");
        return 1;
    }

    fp2 = fopen("D:\\DAA_1246\\lab2\\output1.txt", "w");
    if (fp2 == NULL)
    {
        printf("error : could not open the output file \n");
        fclose(fp1);
        return 1;
    }

    fscanf(fp1, "%d", &n);

    while (fscanf(fp1, "%d", &number) == 1 && count < n)
    {
        int binary = convert(number);

        fprintf(fp2, "%d = %016d\n", number, binary);

        printf("The binary equivalent of %d is %016d\n", number, binary);

        count++;
    }

    fclose(fp1);
    fclose(fp2);

    return 0;
}
