#include <stdio.h> 
#include <string.h>  
void premio()
{
     printf("ANGEL¡¡¡ has alterado el flujo del programa\n"); 
}  
int main(int argc, char *argv[]) 
{
    char buffer[100];
    if (argc != 2)
   {
         printf("Uso: %s argumento\n",argv[0]);
         return -1;
    }
    strcpy(buffer,argv[1]);
    printf ("%s\n",buffer);
    return 0; 
}

