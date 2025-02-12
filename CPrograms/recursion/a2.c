#include <stdio.h>
int Sum(int n){  
    if (n == 0) {
        return 0;
    }
    int res = n + Sum(n - 1);
    return res;
}
int main(){
    int n ;
    printf("Enter no. of terms: ");
    scanf("%d",&n);
    int Total= Sum(n);
    printf("Sum of First %d Numbers: %d", n,Total);
    return 0;
}