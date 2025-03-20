#include <stdio.h>
void rev(int arr[], int start, int end)
{
    if (start >= end)
    {
        return;
    }

    int temp = arr[start];
    arr[start] = arr[end];
    arr[end] = temp;

    rev(arr, start + 1, end - 1);
    return;
}
int main()
{
    int arr[] = {1, 2, 3, 4, 5, 6};
    rev(arr, 0, 5);
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", arr[i]);
    }
}