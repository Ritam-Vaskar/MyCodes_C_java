// #include<stdio.h>

// int main()

// {
    

//     char a[100];
//     int w=1;
    
//     scanf("%[^\n]s",a);

//     for(int i=0;i!='\0';i++)
//     {
//        if(a[i]==' '){
//        	w++;
//        }
//     }
//     printf("%d",w);
	
    
//     return 0;
// }

#include<stdio.h>

int main()

{
    

    char a[100];
    
    char temp;
    scanf("%[^\n]s",a);
    
    
    for(int i=0;a[i]!='\0';i+=2)
    {
        temp=a[i+1];
        a[i+1]=a[i];
        a[i]=temp;
    }
	printf("%s",a);
    
    return 0;
}

