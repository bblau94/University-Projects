#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <signal.h>
#include <readline/readline.h>
#include <unistd.h>

#define shellPipe(x,y) _shellPipe(x,y,-1)

//default process id for foreground processes - used to keep track of process occurrence
pid_t fg_process = -1;

//return size of array
size_t sizeof_array(char* arr[]) {
   int i;
   for (i = 0; arr[i] != NULL; i++);
   return i;
}

//handles exec on each arg
//throws appropriate errors
void shellExec(char *args[]) {
   if (execvp(args[0], args) < 0) {
      switch (errno) {
         case ENOENT: {
                         printf("%s: command not found\n", args[0]);
                         break;
                      }
         case EACCES: {
                         printf("%s: permission denied\n", args[0]);
                         break;
                      }
         default: {
                     printf("%s: unknown error\n", args[0], errno);
                     break;
                  }
      }
      exit(0);
   }
}

void printFileError(char *path) {
   switch(errno) {
      case EACCES: {
         printf("shell: %s: permission denied\n", path);
         break;
      }
      case EISDIR: {
         printf("shell: %s is a directory\n", path);
         break;
      }
      default: {
         printf("shell: %s: an error occurred opening this file\n", path);
         break;
      }
   }
}

//returns 1 if redirected as a result of '<' or '>'
int shellRedirect(char *args[]) {
   int redirect_flag = 0;
   int i;
   for (i = 0; args[i] != NULL; i++) {
      int length = strlen(args[i]);
      //says whether their needs to be a redirection or not
      //and in what way 
      if (args[i][length-1] == '>' || args[i][length-1] == '<') {
         if (args[i+1] == NULL) {
            printf("shell error: filename not specified after '%c'\n", args[i][length-1]);
            exit(-1);
         }

	 //place new fd into appropriate location to be redirected
         if (args[i][length-1] == '>') {

            /* open the file for write, create or append */
            char *path = args[i+1];
            int fd = open(path, O_WRONLY|O_APPEND|O_CREAT, S_IRUSR|S_IWUSR|S_IRGRP|S_IRGRP);

            if (fd < 0) {
               printFileError(path);
               exit(-1);
            } 

            if (length == 1) { 
               dup2(fd,1);
			} else { 
	      //handles special format cases
              switch (args[i][length-2]) {
                 case '&': 
                    dup2(fd, 1);
                 case '1':
                    dup2(fd, 1);
                    break;
                 case '2': 
                    dup2(fd, 2);  
                    break;

                 default:
                    printf("shell: invalid specifier: %s\n", args[i]);
                    exit(-1);
              }
			}
         } else if (args[i][length-1] == '<') {
            //opens file to be read
            char *path = args[i+1];
            int fd = open(path, O_RDONLY);

            if (fd < 0) {
               printFileError(path);
               exit(-1);
            } 

            dup2(fd, 0);
         }
      void* negOne = (void*)-1;
      redirect_flag = 1;
      args[i] = negOne;
      args[i+1] = negOne;
      i++;
      }
   }
   return redirect_flag;
}


void collapseShell(char *args1[], char *oldArgs[]) {
   int i;
   int newArgsInd = 0;
   void* negOne = (void*) -1;
   for (i = 0; oldArgs[i] != NULL; i++) 
      if (oldArgs[i] != negOne)
        args1[newArgsInd++] = oldArgs[i];

   args1[newArgsInd] = NULL;
}


void _shellPipe(char* args1[], char* args2[], int fd_read) {
   int i, additionalPipes_flag = 0;
   int fd[2];
   char* args3[sizeof_array(args1)];

   //handles the third possible command for an input of form "cmd1 | cmd2 | cmd3"
   if (args2[0] != NULL) {
      //pipelines the output of cmd before '|' to input of cmd after the same '|'
      pipe(fd);
      additionalPipes_flag = 1;
      
      for(i = 0; args2[i] != NULL; i++) {
        if (strcmp(args2[i], "|") == 0) {
            int j;
            int args3Ind = 0;
            for (j = i + 1; args2[j] != NULL; j++)
               args3[args3Ind++] = args2[j];
   
            args3[args3Ind] = NULL;
            args2[i] = NULL;
            break;
		}
      }

      //No second '|' found
      args3[0] = NULL;
   }

   pid_t pid, wpid;
   pid = fork();
   int status;

   if (pid < 0 ) {
      printf("myshell: error in pipe - fork() unable to create child process\n");
      return;
   //fork() successfully creates child process "returns 0 to child process"
   } else if (pid == 0) {
      //if there is a third command in "cmd1 | cmd2 | cmd3"
      //then redirect the stdout to to the pipe
      if (additionalPipes_flag) {
	 //close the "read" section
         close(fd[0]);
	 //dup2 closes "write" section and redirects the fd output to the stdout
         dup2(fd[1],1);
      }
      if (fd_read > 0) {
         dup2(fd_read, 0);
      }

      //checks for exec errors
      shellExec(args1);
   //parent
   //when pid > 0
   } else {
      //setting foreground processes to pid (is running)
      fg_process = pid;

      if (additionalPipes_flag) {
         close(fd[1]);
      }
      //wait for change in status of working process
      wpid = waitpid(pid, &status, 0);
      fg_process = -1;
      
      if (additionalPipes_flag) {
         _shellPipe(args2, args3, fd[0]);
     }
   }
}

//creates child process then execs appropriate args
void shellCommand(char* args[], int bg) {
   pid_t cproc, wpid;
   int status;
   
   //create a child process using fork
   cproc = fork();
   //child process wasn't successfully created
   if (cproc < 0) {
      printf("shell {error piping} : Error creating child process with fork()\n");
      return;
   } else if (cproc == 0) { 
      //if there was a redirect - shrink arg array then exec - otherwise just exec
	if (shellRedirect(args)) {
         char *args1[sizeof_array(args)];
	 //fill args1 array with pertinent information
         collapseShell(args1, args);
         shellExec(args1);
	} else {
         shellExec(args);
      }
   } else {
      //allows for the current process to be the foreground process
      //until process execs
      if (!bg) {
         fg_process = cproc;
         wpid = waitpid(cproc, &status, 0);
         fg_process = -1;

	//flushes output buffer of the stream
         fflush(stdout);
      }
   }
}


void parse(char *command) {
   int i;
   //nothing was added to the line so return
   if (command == NULL || command[0] == '\0') {
      return;
   }
   // handles the first case format by splitting the commands by the ';'
   for (i = 0; command[i] != '\0'; i++) {
      if (command[i] == ';') {
         parse(command + i + 1);
         command[i] = '\0';
         break;  
      }
   }
   
   //preset pipe, redirect, and background flags
   int pipe_flag = 0, redirect_flag = 0, bg_flag = 0;
   //runs through string comparing symbols to the specific cases
   for (i = 0; command[i] != '\0'; i++) {
      switch (command[i]) {
         //handles the pipe case where a '|' is used to link the cmds
         case '|': {
            pipe_flag = 1;
            break;
         }
	 
	 //leaves the redirect_flag as 0 to redirect stdout of cmd to the file
         case '>':
	 //flags to redirect the stdin of the cmd to a file
         case '<': {
            redirect_flag = 1;
            break;
         }
	 //flags to redirect the stdout and stderr of the cmd to a file
         case '&': {
            if (command[i+1] == '>') {
               break;
			}
            if (command[i+1] != '\0') {
               printf("shell: syntax error by '&'\n");
               return;
            }
	    //set flag to inform background process is running
            bg_flag = 1;
            //allows for the processing command to continue, skipping where the '&' was 
            command[i] = '\0';
            i--;
            break;
         }
      }
   }

   //if both flags at 1, print appropriate error
   if ((pipe_flag && redirect_flag)) {
      printf("myshell: error: '|' operator incompatible with '>' or '<'\n");
      return;
   }
   //if both flags at 1, print appropriate error
   if ((pipe_flag && bg_flag)) {
      printf("myshell: error: '|' operator incompatible with '&'\n");
      return;
   }

  
   char *args[50]; /* support up to 50 args */
   int argindex;
   //set first arg to " "
   args[0] = strtok(command, " ");
   //increment argindex if not NULL command
   for (argindex = 1; (args[argindex] = strtok(NULL, " ")) != NULL; argindex++);
   
   //special case for commands "exit()", "exit", and "ctrl-d" to close myshell
   if ((strcmp(args[0], "exit()") == 0) || (strcmp(args[0], "exit") == 0) || (strcmp(args[0], "ctrl-d") == 0) ) {
      exit(0);
   }
  /*
   //handles "ctrl-c" case
   if (strcmp(args[0], "ctrl-c") == 0) {
      doSigint(SIGINT, &int_act, NULL);
   }
  */

   //if command line had a '|'
    if (pipe_flag) {
      //determines location of '|'
      for (i = 0; args[i] != NULL; i++) {
         if (strcmp(args[i], "|") == 0) {
            //set '|' location to a null pointer
			args[i] = NULL;

	    //create a duplicate array of the size of the argument
            char* args2[sizeof_array(args)];
            int j;
            int args2Ind = 0;
            //splits the arguments at the '|'
	    //create and use second argument char array to handle input after '|'
            for (j = i + 1; args[j] != NULL; j++) {
               args2[args2Ind++] = args[j];
            }

	    //ends string
            args2[args2Ind] = NULL;
	    //connects commands through pipes
            shellPipe(args, args2);
         }
      }
   //if no pipe flag ( no '|' )
    } else {
      shellCommand(args, bg_flag);
   }
}

static void doSigchild(int sig, siginfo_t *siginfo, void *context) { 
   int status;
   //create the pid object
   pid_t pid;
   //sets pid to wait for any child processes
   pid = wait(&status);
}

static void doSigint(int sig, siginfo_t *siginfo, void *context) {
   if (fg_process > 0) {
      kill(fg_process, SIGINT);
   }
}

int main() {
   struct sigaction child_act;
   //copies null charecter to the sigaction child_act adress for the size of the sigaction 
   memset(&child_act,'\0', sizeof(child_act));
   //sets sigaction handler
   child_act.sa_sigaction = doSigchild;

   struct sigaction int_act;
   memset(&int_act, '\0', sizeof(int_act));
   int_act.sa_sigaction = doSigint;

   //prevents zombie children
   if (sigaction(SIGCHLD, &child_act, NULL) < 0) {
      printf("sigaction error\n");
      exit(-1);
   }

   //kills foreground processes
   if (sigaction(SIGINT, &int_act, NULL) < 0) {
      printf("sigaction error\n");
      exit(-1);
   }

   char *line;

   while (1) {
      //prompts for input into shell starting with the myshell introduction
      line = readline("myshell> ");
      //parses the new input from the shell
      parse(line);
   }
}
