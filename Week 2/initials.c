#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
    printf("Enter the name: ");
    string s= get_string();
    if (s!=NULL)
    {
        int i=0,j=0;
        printf("%c",toupper(s[i]));
        for(i=1;i<strlen(s);i++)
        {
            if(s[i]==' ')
            {   j=i+1;
                printf("%c",toupper(s[j]));
            }
        }
        printf("\n");
    }
    
}