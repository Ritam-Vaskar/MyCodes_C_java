#include<stdio.h>
int main(){
    int s1,s2;
    printf("Enter array sizes : ");
    scanf("%d %d",&s1,&s2);
    int arr1[s1],arr2[s2],resultArr[s1+s2];
    printf("Enter elements for array 1 :\n");
    for(int i=0;i<s1;i++){
        scanf("%d",&arr1[i]);
    }
    printf("Enter elements for array 2 :\n");
    for(int i=0;i<s2;i++){
        scanf("%d",&arr2[i]);
    }
    for(int i=0;i<s1+s2;i++){
        resultArr[i]=(i<s1?arr1[i]:arr2[i-s1]);
    }
    for(int i=0;i<s1+s2;i++){
        for(int j=0;j<s1+s2;j++){
            if(resultArr[i]<resultArr[j]){
                int temp=resultArr[i];
                resultArr[i]=resultArr[j];
                resultArr[j]=temp;
            }
        }
    }
    for(int i=0;i<s1+s2;i++){
        printf("%d\t",resultArr[i]);
    }

    return 0;
}