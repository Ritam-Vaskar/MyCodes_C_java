#include<stdio.h>
main(){
    int i,j,p1,p2;
    printf("Enter number of terms in Polynomial 1\n");
    scanf("%d",&p1);
    printf("Enter number of terms in Polynomial 2\n");
    scanf("%d",&p2);

    int a[p1],b[p2],prod[p1+p2];


    printf("Enter Elements of Polynomial 1\n");

    for(i=0;i<p1;i++){
        printf("Enter x^%d Co efficient of Polynomial 1\n",i);
        scanf("%d",&a[i]);
    }
    
    printf("Enter Elements of Polynomial 2\n");

    for(i=0;i<p2;i++){
        printf("Enter x^%d Co efficient of Polynomial 2\n",i);
        scanf("%d",&b[i]);
    }


    // ye power k liye
    for(i=0;i<p1+p2;i++){
        prod[i]=0;
    }

 
    for(i=0;i<p1;i++){
        for(j=0;j<p2;j++){
            if(a[i]!=0 && b[j]!=0) prod[i+j]+=a[i]*b[j];
        }
    }
    
    for(i=p1+p2-1;i>=0;i--){
        if(prod[i]!=0){
            if(i!=0) printf("%d x^%d + ",prod[i],i);
            else printf("%d x^%d\n",prod[i],i);
        }
    }
}