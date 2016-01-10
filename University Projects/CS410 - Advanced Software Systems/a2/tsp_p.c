#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAX_BUF 1024

int main(int argc, char *argv[]) {
	
	//number of seperate processes to create
	//hard coded for now, will change to accomodate graph
	//int num_processes = 4;
	int i = 0;
        
	//FIFO accross processes
	int ret;
	char value[100];
    FILE *cfp;
	FILE *pfp;
    char myfifo[] = "/tmp/myfifo";
	ret=mknod(myfifo, S_IFIFO | 0666, 0); 

    	char buf[MAX_BUF];

        //extracts the number of cities and the matrix file name
        int j;
        int n=0;
        char stdbuf[60];
        char matfile[10];
	/*
        if (argc >= 1)
        {
        matfile = argv[1];
 
        }
	*/

	fgets(matfile, 10, stdin);

         FILE * fp;
         fp = fopen (matfile, "r");
	
         if(fp == NULL) 
         {
         perror("Error opening file");
         }
	
         while ((fgets(stdbuf, 60, fp) != NULL)) 
         {
         n++; 
         }
	
   	/* create the FIFO (named pipe) */
    	//mkfifo(myfifo, 0666);

	for (i; i < n; i++) 
	{
	sleep(4);
	pid_t pid = fork();
	if (pid == 0) {
		//child now exec's
		//replace find_pathsargs with graph

		//cfp = fopen(fifoName,"r");
		char totalnum[10];
		snprintf(totalnum, 10, "%d", n);
		char citystart[10];
		snprintf(citystart, 10, "%d", i);
		//printf("totalnum = %s      citystart = %s\n",totalnum,citystart);
		char* args[] = {"./find_paths",totalnum,citystart,matfile, NULL};
		sleep(1);
		execv("./find_paths", args);

		exit(0);
	}
       }

    	/* open, read, and display the message from the FIFO */
	//Wait for child processes to finish
	/*
	wait(NULL);
	while (fgets(buf, 100, pfp) != NULL)
   	 puts(buf);
*/
	//Close
	sleep(3);
	/*
	pfp = fopen(myfifo,"r");
	while(fgets(value, 100, fp)) {
    	   printf("%s\n", value);
	}

	//fscanf(pfp,"%s",value);
  	//puts(value);
	unlink(myfifo);*/
	return 0;
}
