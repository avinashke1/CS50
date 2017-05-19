#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    int cent, left, quarter, dime, nickel, penny, coin;
    int quarter = 25, dime = 10, nickel = 5;
    
    do
    {
        printf("O hai! How much change is owed?\n");
        dollars = get_float();    
    }
    while (dollars < 0);
    
    cent = (int)round(dollars * 100);
    
    quarter = cent / quarter;
    left = cent % quarter;
    
    dime = left / dime;
    left = left % dime;
    
    nickel = left / nickel;
    left = left % nickel;
    
    penny = left;
    
    coin = quarter + dime + nickel + penny;
    printf("%i\n",coin);
 
} 
