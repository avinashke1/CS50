/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    //Implementing Binary Search
    
    int s=0;
    int l=n-1;
    int m=0;
    while(s<=l)
    {
        m=(s+l)/2;
        if(value==values[m])
        {
            printf("Available.");
            return true;
        }
        else if(value<values[m])
        {
            l=m-1;
        }
        else
        {
            s=m+1;
        }
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    int i;
    int j;
    for (i=0;i<n;i++)
    {
        int z=i;
        for(j=i+1;j<n;j++)
        {
            if(values[j]<values[z])
            {
                z=j;
            }
        }
        int temp=values[i];
        values[i]=values[z];
        values[z]=temp;
    }
    return;
}
