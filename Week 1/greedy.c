#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    int cent, left, quarter_c, dime_c, nickel_c, penny_c, coin_c;
    int quarter = 25, dime = 10, nickel = 5;
    
    do
    {
        printf("O hai! How much change is owed?\n");
        dollars = get_float();    
    }
    while (dollars < 0);
    
    cent = (int)round(dollars * 100);
    
    quarter_c = cent / quarter;
    left = cent % quarter;
    
    dime_c = left / dime;
    left = left % dime;
    
    nickel_c = left / nickel;
    left = left % nickel;
    
    penny_c = left;
    
    coin_c = quarter_c + dime_c + nickel_c + penny_c;
    printf("%i\n",coin_c);
 
} 