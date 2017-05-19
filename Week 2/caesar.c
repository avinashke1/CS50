#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc,string argv[])
{
    if(argc<=1 || argc>2)
    {
        printf("k");
    }
    else
    {
        int k = atoi(argv[1]);
        string s=get_string();
        int asciiA=65;
        int asciia=97;
        int alpha=26;
        for (int i=0;i<strlen(s);i++)
        {
            if(isupper(s[i]))
            {
                printf("%c",((s[i]-asciiA+k)%alpha)+asciiA);
            }
            else if(islower(s[i]))
            {
                printf("%c",((s[i]-asciia+k)%alpha)+asciia);
            }
            else
            {
                printf("%c",s[i]);
            }
        }
    }
    printf("\n");
    return 0;
}