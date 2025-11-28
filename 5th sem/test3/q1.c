//Longest Common Subsequence
#include <stdio.h>
#include <string.h>

int max(int a, int b)
{
    return (a > b) ? a : b;
}
int main()
{
    char x[100], y[100];
    int m, n, i, j;
    printf("Enter the first string: ");
    scanf("%s", x);
    printf("Enter the second string: ");
    scanf("%s", y);
    m = strlen(x);
    n = strlen(y);
    int L[m + 1][n + 1];
    for (i = 0; i <= m; i++)
    {
        for (j = 0; j <= n; j++)
        {
            if (i == 0 || j == 0)
                L[i][j] = 0;
            else if (x[i - 1] == y[j - 1])
                L[i][j] = L[i - 1][j - 1] + 1;
            else
                L[i][j] = max(L[i - 1][j], L[i][j - 1]);
        }
    }
    printf("Length of Longest Common Subsequence: %d", L[m][n]);
    
    printf("\nLongest Common Subsequence: ");
    i = m;
    j = n;
    while (i > 0 && j > 0)
    {
        if (x[i - 1] == y[j - 1])
        {
            printf("%c", x[i - 1]);
            i--;
            j--;
        }
        else if (L[i - 1][j] > L[i][j - 1])
            i--;
        else
            j--;
    }
    printf("\n");
    return 0;
}