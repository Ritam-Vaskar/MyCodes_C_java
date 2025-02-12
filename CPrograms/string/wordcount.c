 #include<stdio.h>

int main()

{
    

    char a[100];
    int w=0;
    
    scanf("%[^\n]s",a);

    for(int i=0;a[i]!='\0';i++)
    {
       if(a[i]==' '){
       	w++;
       }
    }
    printf("%d",w+1);
	
    
    return 0;
}