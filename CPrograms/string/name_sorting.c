#include<stdio.h>
#include<string.h>
void count(){

}
int main(){
    int n;
    printf("Enter the number of names : ");
    scanf("%d",&n);
    char names[n][100];
    for(int i=0;i<n;i++){
        scanf(" %[^\n]s",names[i]);
    }
    int min=0;
    for(int i=0;i<n;i++){
        for(int k=0;k<n;k++){
            if(names[i][0]<names[k][0]){
                for(int l=0;names[i][l]!='\0';l++){
                    char temp=names[i][l];
                    names[i][l]=names[k][l];
                    names[k][l]=temp;
                }
            }
        }
    }
    for(int i=0;i<n;i++){
        if(names[i][0]==names);
    }

    // printing names
    for(int i=0;i<n;i++){
        puts(names[i]);
    }
}