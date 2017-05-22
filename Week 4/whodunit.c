#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        fprintf(stderr,"Must Enter input file and output file\n");
        return 1;
    }

    char* input = argv[1];
    char* output = argv[2];

    FILE* inputptr = fopen(input, "r");
    if (inputptr == NULL)
    {
        fprintf(stderr,"Could not open.");
        return 2;
    }

    FILE* outputptr = fopen(output, "w");
    if (outputptr == NULL)
    {
        fclose(inputptr);
        fprintf(stderr, "Could not open.");
        return 3;
    }

    BITMAPFILEHEADER bfh;
    fread(&bfh, sizeof(BITMAPFILEHEADER), 1, inputptr);
    BITMAPINFOHEADER bih;
    fread(&bih, sizeof(BITMAPINFOHEADER), 1, inputptr);

    if (bfh.bfOffBits != 54 || bih.biSize != 40 || bih.biBitCount != 24)
    {
        fclose(outputptr);
        fclose(inputptr);
        fprintf(stderr, "Not a BMP File.\n");
        return 4;
    }
    
    fwrite(&bfh, sizeof(BITMAPFILEHEADER), 1, outputptr);
    fwrite(&bih, sizeof(BITMAPINFOHEADER), 1, outputptr);
    int height=abs(bih.biHeight);
    int width=abs(bih.biWidth);
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE t;
            fread(&t, sizeof(RGBTRIPLE), 1, inputptr);
            
            if (t.rgbtBlue == 0x00 && t.rgbtGreen == 0x00 && t.rgbtRed == 0xff) {
                t.rgbtBlue = 0xff;
                t.rgbtGreen = 0xff;
                t.rgbtRed = 0xff;
            }

            fwrite(&t, sizeof(RGBTRIPLE), 1, outputptr);
        }

    }
    
    
}