#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc,string argv[])
{
    if(argc==1 || argc>2)
    {
        printf("k");
    }
    else
    {
        string k=argv[1];
        int klen=strlen(k);
        int kindex=0;
        int asciiA=65;
        int asciia=97;
        int alpha=26;
        
        for (int i=0;i<klen;i++)
        {
            if(!isalpha(k[i]))
            {
                printf("k");
                return 1;
            }
        }
        
        for (int i=0;k[i];i++)
        {
            k[i]=toupper(k[i]);
        }
        
        string s=get_string();
        
        for (int i=0;i<strlen(s);i++)
        {
            char mapping=k[(kindex%klen)];
            
            if(isupper(s[i]))
            {
                printf("%c",((s[i]-asciiA+(mapping-asciiA))%alpha)+asciiA);
                kindex++;
            }
            
            else if(islower(s[i]))
            {
                printf("%c",((s[i]-asciia+(mapping-asciiA))%alpha)+asciia);
                kindex++;
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