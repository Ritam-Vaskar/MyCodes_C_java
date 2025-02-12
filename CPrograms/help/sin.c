#include <stdio.h>


int power(int base, int exponent) {
    int result = 1.0;
    int i;

   
    if (exponent < 0) {
        for (i = 0; i < -exponent; i++) {
            result *= 1.0 / base;
        }
    } else { 
        for (i = 0; i < exponent; i++) {
            result *= base;
        }
    }

    return result;
}


int fact(int x){
    int f=1;
    for(int i=2 ; i<=x ; i++){
      f=f*i;  
    }
    return f;
}

int main() {
    int n;
    printf("Enter no. of terms: ");
    scanf("%d",&n);
    int x;
    printf("Enter X: ");
    scanf("%d",&x);
    float sum = 0.0;
    int sign=1;
    for(int i=1;i<=n;i++){
        
            sum=sum+ sign * ((power(x,2*i+1))/fact(2*i+1));
            sign*=-1;
        
    }
    printf("The sum of the sin series: %f",sum);
    
    return 0;
}
