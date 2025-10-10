//greedy algo for knapsack problem
#include <stdio.h>
#include <stdlib.h>

struct item
{
    int itemNo;
    int weight;
    int value;
    float ratio;
};
int compare(const void *a, const void *b)
{
    struct item *itemA = (struct item *)a;
    struct item *itemB = (struct item *)b;
    if (itemA->ratio < itemB->ratio)
        return 1;
    else if (itemA->ratio > itemB->ratio)
        return -1;
    else
        return 0;
}
void knapsack(struct item items[], int n, int capacity)
{
    qsort(items, n, sizeof(struct item), compare);
    int totalValue = 0;
    int currentWeight = 0;
    printf("Items included in the knapsack:\n");
    for (int i = 0; i < n; i++)
    {
        if (currentWeight + items[i].weight <= capacity)
        {
            currentWeight += items[i].weight;
            totalValue += items[i].value;
            printf("Item %d: weight = %d, value = %d\n", items[i].itemNo, items[i].weight, items[i].value);
        }
        else
        {
            int remainingWeight = capacity - currentWeight;
            if (remainingWeight > 0)
            {
                totalValue += items[i].value * ((float)remainingWeight / items[i].weight);
                currentWeight += remainingWeight;
                printf("Item %d: weight = %d (fractional), value = %.2f\n", items[i].itemNo, remainingWeight, items[i].value * ((float)remainingWeight / items[i].weight));
            }
            break;
        }
    }
    printf("Total value in the knapsack: %.2f\n", (float)totalValue);
}

int main()
{
    int n, capacity;
    printf("Enter the number of items: ");
    scanf("%d", &n);
    struct item items[n];
    for (int i = 0; i < n; i++)
    {
        items[i].itemNo = i + 1;
        printf("Enter weight and value for item %d: ", i + 1);
        scanf("%d %d", &items[i].weight, &items[i].value);
        items[i].ratio = (float)items[i].value / items[i].weight;
    }
    printf("Enter the capacity of the knapsack: ");
    scanf("%d", &capacity);
    knapsack(items, n, capacity);
    return 0;
}
