#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("Enter the shower time in minutes: \n");
    int n=get_int();
    int i=n*12;
    printf("Minutes: %i\n",n);
    printf("Bottles: %i\n",i);
}