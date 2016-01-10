#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>

void swap(char *a, char *b) 
{ 
   char t = *a; *a = *b; *b = t; 
}

int factorial(int number) {
    int factorial;
    factorial = number;
    number--;
    while(number > 0) {
	factorial *= number;
	number--;
    }
    return factorial;
}

void permutePointer(char *a, int i, int n, int startCity,int *matrix[]) {
   int y, z, j,q, count;
   char* b;
   int nfactdn = factorial(n)/n;

   static char* bestPath;
   static int counter = 0;
   static int bpc = 0; //currently unused, can be toggled
   static int minDist = 255;
   b = (char*) malloc(18); //given random value > what would be needed to handle single digit n's


   if (counter == 0) { //only allocate memory for bestPath the first time through this function
       bestPath = (char*) malloc(n+1);
   }

   // If we are at the last letter, print it
   if (i == (n-1)){
	   //after we create a string of size n+1 (as in 010, 0120, 01230, etc.
	   //permutations returning to starting point).
	if (*a == (startCity + '0')) {
	   int currentDist = 0;
	   counter++;
       strcpy(b, a);
	   strncat(b, b, 1);

           for (y = 0; y < n; y++) {
		if (matrix[*(b+y) - '0'][*(b+y+1) - '0'] != -1) {
		    currentDist += matrix[*(b+y) - '0'][*(b+y+1) - '0'];
                } else {
		    //printf("Invalid Path");
		    currentDist = 9001; //IT'S OVER 9000!!!
		    break;
		}
	   }

	   if (currentDist != 9001) {
	       //printf("Path: %s has a distance of %d\n", b, currentDist);
	       //printf("%s       %d \n", b, currentDist);

	       //write(fd, b, 20);
		   
		   //below formats the string with paths/pathlengths
	       char distance[10];
	       snprintf(distance, 10, "%d", currentDist);
	       strcat(distance, "  ");
	       strcat(distance, b);
	       printf("%s\n",distance);
		   /*
	       FILE *cfp;
  	       char myfifo[]= "/tmp/myfifo";
    
    	       //write to the FIFO
               cfp = fopen(myfifo, "w");


	       fprintf(cfp,"%s",distance);
	       fflush(cfp);*/
	//fclose(cfp);
	/*
		if(startCity == n)
		{
		unlink(cfp);
		}
	*/
	   }

	   //compares current distance to the lowest distance and swaps accordingly
	  if (currentDist < minDist) {
 	        minDist = currentDist;
		if (*bestPath == '\0') {
	            strcat(bestPath, b);
		} else {
		   free(bestPath);
		   bestPath = (char*) malloc(n+1);
	           strcat(bestPath, b);
		}
		free(b);
	  }  
	}
   } else {
     // Show all the permutations with the first i-1 letters fixed and 
     // swapping the i'th letter for each of the remaining ones.
       for (j = i; j < n; j++) {
           swap((a+i), (a+j));
           permutePointer(a, i+1, n, startCity,matrix);
           swap((a+i), (a+j));
       }
    }

	//If the current bestPath does not exist, do nothing
	if (*bestPath == '\0') {
	
	} else {
	//otherwise, the check below compares the number of paths (counter) with (n!/n)
	//This will cause Best Path to only print after all paths have been calculcated.

		//If you want the best path at each starting city to print out
		//for each process/thread, uncomment the print statement here.
	    if (counter == nfactdn) {
		//below if makes sure we only print the best path once - otherwise recursion causes
		//multiple Best Path prints
                if (bpc == 0) {
   	        //printf("Best Path: %s has a distance of %d\n", bestPath, minDist);
		free(bestPath);
 		bpc++;
		}
	    }
	}
	//close(fd);
	//unlink("/tmp/myfifo");

}

void main(int argc, char *argv[]) {

    //write(fd, "Hi", sizeof("Hi"));
//-------------------------------------

    //example of string accepting 4=n numbers
    //n > 9 does not work.
    int i;
    int j;
    int startCity = 2;
    int counter = 0;
    int n=0;
    char* str;
    char* temp;
    char* matfile;
    char stdbuf[60];
    int dist;	
    char *token;

    if (argc > 1)
    {
        n = atoi(argv[1]);
	//printf("n = %d\n",n);
        startCity = atoi (argv[2]);
        matfile = argv[3];
        //matfile = argv[2];
	//however we take the the D matrix
        //D = argv[3];
    }

   int** matrix=malloc(1000*sizeof(int*)); 
   for(i=0;i<1000;++i)
   {
      matrix[i]=malloc(4*sizeof(int));
   }

   FILE* fz;
   fz = fopen (matfile, "r");

   for(i = 0; i < n; i++)
   {
      for(j = 0; j < n; j++) 
      {
       if (!fscanf(fz, "%d", &matrix[i][j])) 
           break;
      }

   }	
   
    temp = (char*) malloc(n);
    str = (char*) malloc(n);
    int nfact = factorial(n);
    int size = (nfact*(n+1) + nfact); // +factorial(n) is for n! newline chars
	
	//creates char pointer of path size n
	//ex: n = 2 ; str = 01 | n = 3 ; str = 012 |...
    while (counter < n) {
        *temp = (char)(counter + '0');
        strcat(str, temp);
        counter++;
    }
 
    free(temp);    
    //generates all potential paths of size n and copies into paths char*
    permutePointer(str, 0, n, startCity, matrix);
    free(str);
    
}

