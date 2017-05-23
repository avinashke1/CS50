#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "dictionary.h"
#define ASCII_OFFSET 97;

typedef struct node
{
    bool Word;
    struct node* Node[50];
}
node;
node* rootNode;
node* nextNode;

int wordCount = 0;

/**
 * Returns true if word is in dictionary else false.
 */

bool check(const char* word)
{
    int wordLength = strlen(word);

    for(int i = 0; i < wordLength; i++)
    {
        int check = tolower(word[i]) - ASCII_OFFSET;
        if(nextNode->Node[check] == NULL)
        {
            return false;
        }
        nextNode = nextNode->Node[check];
    }
    nextNode = rootNode;
    return (nextNode->Word);
}

/**
 * Loads dictionary into memory.  Returns true if successful else false.
 */

bool load(const char* dictionary)
{
    FILE* file = fopen(dictionary,"r");
    if(file == NULL)
    {
        return false;
    }
    rootNode = malloc(sizeof(node));
    nextNode = rootNode;

    int temp = fgetc(file) - ASCII_OFFSET;
    while(temp != EOF)
    {
        while(temp != '\n')
        {
            if(nextNode->Node[temp] == NULL)
            {
                nextNode->Node[temp] = malloc(sizeof(node));
                nextNode = nextNode->Node[temp];
            }
           
            else 
            {
                nextNode = nextNode->Node[temp];
            }
            temp = fgetc(file) - ASCII_OFFSET;
        }
        temp = fgetc(file) - ASCII_OFFSET;
        nextNode->Word = true;
        wordCount++;
        nextNode = rootNode;
    }


    fclose(file);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */

unsigned int size(void)
{
    return wordCount;
}

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */

bool unload(void)
{
    for(int i = 0; i < 26; i++)
    {
        if(nextNode->Node[i] != NULL)
        {
            nextNode = nextNode->Node[i];
            unload();
        }
    }

    free(nextNode);
    return true;
}