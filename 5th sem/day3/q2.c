
//generate 5 random numbers and store them in a file
#include <stdio.h>
#include <stdlib.h>
int main()
{
    FILE *fptr;
    fptr = fopen("random3.txt", "w");
    for (int i = 0; i < 50; i++)
    {
        int num = rand() % 100 + 1;
        fprintf(fptr, "%d\n", num);
    }
    fclose(fptr);
    return 0;
}