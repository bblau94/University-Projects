#define _GNU_SOURCE
#include <malloc.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

//Source for threading outline: http://www.evanjones.ca/software/threading.html

// 64kB stack
#define FIBER_STACK 1024*64
#define MAX_BUF 1024

//struct to hold information passed through find_paths
struct S {
	char* matrix;
	int start;
	int locations;
};



// The child thread will execute this function
int threadFunction( void* argument )
{
	struct S *testStruct = (struct S*) argument;
	int start2, locations2;
	char* matfile2;
	//pull information from struct object, then feed into thread function
	start2 = testStruct->start;
	matfile2 = testStruct->matrix;
	locations2 = testStruct->locations;
    
	//convert ints to chars
	char citystart[100];
	snprintf(citystart, 100, "%d", start2);
	
	char numcities[100];
	snprintf(numcities, 100, "%d", locations2);

	 char* args[] = {"./find_paths", numcities, citystart, matfile2, NULL};
	 execv("./find_paths", args);
     return 0;
}

int main(int argc, char *argv[])
{

	char matfile[10];
	int num_threads = 0;
	char stdbuf[60];
	
/*
 if (argc > 1)
    {
        matfile = argv[1];
    }
*/

   fgets(matfile, 10,stdin); 


   FILE * fp;

   fp = fopen(matfile, "r");

   if(fp == NULL) 
   {
      perror("Error opening file");
   }

   while ((fgets(stdbuf, 60, fp) != NULL)) 
   {
      num_threads++; 
   }

    close(fp);


	//FIFO accross processes
    	//int fd;
    	//char * myfifo = "/tmp/myfifo";
    	//char buf[MAX_BUF];
    	/* create the FIFO (named pipe) */
    	//mkfifo(myfifo, 0666);

	

    void* stacks[num_threads];

	//Thread IDs
    pid_t pids[num_threads];
        
    // Allocate the stacks
	int k = 0;
	for (k; k < num_threads; k++) {
        stacks[k] = malloc( FIBER_STACK );
        if ( stacks[k] == 0 ) {
                	 perror( "malloc: could not allocate stack" );
                 	exit( 1 );
        }
    }
	
    struct S args[num_threads]; 
	int i = 0;
	for (i; i < num_threads; i++) {
		args[i].start = i;
		args[i].matrix = matfile;
		args[i].locations = num_threads;

		
		// Call the clone system call to create the child threads
        pids[i] = clone( &threadFunction, (char*) stacks[i] + FIBER_STACK,
                SIGCHLD | CLONE_FS | CLONE_FILES | CLONE_SIGHAND | CLONE_VM, &args[i]);
	
        if ( pids[i] == -1 ) {
			perror( "clone" );
        	exit( 2 );
        }
	}
    
    	/* open, read, and display the message from the FIFO */
    	//fd = open(myfifo, O_RDONLY);
        //if (fcntl(fd, F_GETFD) == -1) {
	//	perror("fd failed");
	//	exit(1);
	//}


	int j = 0;
	for (j; j < num_threads; j++) {
         // Wait for the child threads to exit
    	//read(fd, buf, MAX_BUF);
    	//printf("Received: %s\n", buf);
         pids[j] = waitpid( pids[j], 0, 0 );
	 	//Prints the answers that were computed in the child threads
         if ( pids[j] == -1 ) {
            perror( "waitpid" );
            exit( 3 );
        	}
    }
         // Free the stacks
	 int l = 0;
	 for (l; l < num_threads; l++) {
         	free( stacks[l] );
	 }
	 sleep(3);
     return 0;
}
