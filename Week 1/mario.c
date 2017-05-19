#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int i,j,k;
    printf("Enter the height: ");
    int n = get_int();
    printf("Height: %i\n",n);
    if(n>=1)
    {
        for (i=1;i<=n;i++)
        {
            for(j=n;j>i;j--)
                printf(" ");
            for(k=1;k<=i;k++)
            {
                printf("#");
            }
            printf("\n");
        }
    }
    else
    {
        printf("Enter a suitable integer value!");
    }
}