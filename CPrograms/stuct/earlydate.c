#include <stdio.h>

struct date {
    int dd;
    int mm;
    int yy;
};

void com (struct date s1,struct date s2){

    if(s1.yy>s2.yy) printf("%d %d %d" , s2.dd , s2.mm , s2.yy);
    else if(s1.mm>s2.mm && s1.yy==s2.yy) printf("%d %d %d" , s2.dd , s2.mm , s2.yy);
    else if(s1.dd>s2.dd && s1.mm==s2.mm && s1.yy==s2.yy ) printf("%d %d %d" , s2.dd , s2.mm , s2.yy);
    else printf("%d %d %d" , s1.dd , s1.mm , s1.yy);
}

int main() {

    struct date d1;
    struct date d2;

    printf("Enter 1st Date: ");
    scanf("%d %d %d", &d1.dd , &d1.mm , &d1.yy);

    printf("Enter 2nd Date: ");
    scanf("%d %d %d", &d2.dd , &d2.mm , &d2.yy);

    com(d1,d2);
    return 0;
}
