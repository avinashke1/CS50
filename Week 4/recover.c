#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint8_t  BYTE;
int main(int argc, char* argv[])
{
    if(argc!=2 || argv[1]==NULL)
    {
        printf("Enter card.raw for the argument.");
        return 2;
    }
    
    FILE* inptr = fopen("card.raw", "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", "card.raw");
        return 1;
    }
    
    FILE* outptr = NULL;
    BYTE b[512];
    BYTE arr[50];
    BYTE pichex[4] = {0xff, 0xd8, 0xff, 0xe0};
    int picnum = 0;
    char picname[50];
    while (fread(&b, sizeof(b), 1, inptr) > 0)
    {
	for (int i = 0; i < 4; i++)
	{
	    arr[i] = b[i];
	}
	arr[3] = (arr[3] >> 4) << 4;
        if (memcmp(arr, pichex, sizeof(pichex)) == 0)
        {
            if (outptr == NULL)
            {
                sprintf(picname, "%03d.jpg", picnum);
                outptr = fopen(picname, "a");
                fwrite(&b, sizeof(b), 1, outptr);
            }
            else
            {
                fclose(outptr);
                picnum++;
                sprintf(picname, "%03d.jpg", picnum);
                outptr = fopen(picname, "a");
                fwrite(&b, sizeof(b), 1, outptr);
            }
        }
        
        else
        {
            if (outptr != NULL)
            {
                fwrite(&b, sizeof(b), 1, outptr);
            }
        }
    }
    fclose(inptr);
    fclose(outptr);
    return 0;
}