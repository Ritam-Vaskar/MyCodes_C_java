#include <stdio.h>
#include <stdlib.h>

void insert(int *ptr, int *n, int pos, int num)
{
    if (pos > *n || pos < 0)
    {
        ptr = realloc(ptr, (*n + 1) * sizeof(int));
        *(ptr + (*n)++) = num;
        printf("Undefined Index :(:( %d was added in index number: %d", num, (*(n)-1));
    }
    else
    {
        ptr = realloc(ptr, ++*n * sizeof(int));
        for (int i = *n - 1; i > pos; i--)
            *(ptr + i) = *(ptr + i - 1);
        *(ptr + pos) = num;
        printf("%d was added in index number: %d", num, pos);
    }
}
void delete(int *ptr, int *n, int pos)
{
    if (pos >= *n || pos < 0)
        printf("\nInvalid Index :(:(");
    else
    {
        for (int i = pos; i < *n - 1; i++)
            *(ptr + i) = *(ptr + i + 1);
        ptr = realloc(ptr, --*n * sizeof(int));
        printf("\nElement deleted successfully.");
    }
}
int search(int *ptr, int n, int key)
{
    for (int i = 0; i < n; i++)
        if (key == *(ptr + i))
            return i;
    return -1;
}
void traverse(int *ptr, int n)
{
    printf("\nThe array : ");
    for (int i = 0; i < n; i++)
        printf("%d ", *(ptr + i));
    printf("\n");
}

int main()
{
    int n = 0;
    int *ptr = (int *)calloc(n, sizeof(int));

    int isTrue = 1;
    while (isTrue)
    {
        printf("\nPress :-");
        printf("\n1: Insertion\n2: Deletion\n3: Search\n4: Traverse\n5: Quit.");
        printf("\nEnter you choice: ");
        int choice, num, pos, key;
        scanf("%d", &choice);
        switch (choice)
        {
            case 1:
                printf("\nEnter the number: ");
                scanf("%d", &num);
                printf("Enter the position:  ");
                scanf("%d", &pos);
                insert(ptr, &n, pos, num);
                break;
            case 2:
                printf("\nEnter the index to be removed: ");
                scanf("%d", &pos);
                delete (ptr, &n, pos);
                break;
            case 3:
                printf("\nEnter the number to be searched: ");
                scanf("%d", &key);
                if (search(ptr, n, key) == -1)
                    printf("No such element exist :(:(");
                else
                    printf("%d found at index: %d", key, search(ptr, n, key));
                break;
            case 4:
                if (n == 0)
                    printf("Empty array :(:(");
                else
                    traverse(ptr, n);
                break;
            case 5:
                isTrue = 0;
                printf("\nProgram ended.");
                break;           default:
                printf("Wrong input :(:(");
                break;
        }
    }
    free(ptr);
    return 0;
}