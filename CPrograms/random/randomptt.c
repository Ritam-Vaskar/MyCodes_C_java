int main() {
    int i,j;
    for(i=0;i<5;i++)
    {
        if(i%2==0)
            {
              for(j=1;j<=5-i;j++)
              {
                  printf("%d",j);
              }
            }
              else
              {
                  for(j=1;j<=i;j++)
                  {
                      printf(" ");
                  }
                  for(j=i+1;j<=5;j++)
                  {
                      printf("%d",j);
                  }
              }
              printf("\n");
    }
    

    return 0;
}
