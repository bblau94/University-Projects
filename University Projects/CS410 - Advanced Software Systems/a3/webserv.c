/* BU CS410 a3 - webserv.c
 * Benjamin Blau, Tyler Butler, Jeffrey Zurita
 *
 * Used tinyhttpd as a foundation for our server.
 * Source: http://sourceforge.net/projects/tinyhttpd/
 */

#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/sendfile.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <fcntl.h>
#include <pthread.h>
#include <strings.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

void nextRequest(int);
void cat(int, FILE *);
void do_cat(int, FILE *, char *);
void errorControl(const char *);
void execCGI(int, const char *, const char *, const char *);
int readLine(int, char *, int);
void header(int, const char *, char*);
void notFound(int);
void execFile(int, const char *);
int bindToPort(char *);
void notImplemented(int);

//handle the next request
void nextRequest(int client) {
	char buf[2048];
	char buff[1024];
	int line;
	char fType[255];
	char fullPath[512];
	char *shortPath;
	char request[2048];
	char *str = NULL;
	FILE *file = NULL;
	size_t i, j;
	i = 0;
	j = 0;
	struct stat stats;
	int cgi = 0; //set to 1 to toggle cgi case

	line = readLine(client, buf, sizeof(buf));
	
	while (!(isspace((int)buf[j])) && (i < sizeof(request) - 1)) {
		request[i] = buf[j];
		i++;
		j++;
	}
	request[i] = '\0';
	
	//handle improper request
	if (strcasecmp(request, "GET") && strcasecmp(request, "POST")) {
		notImplemented(client);
		return;
	}
	//toggle cgi if working with a cgi script
	if (strcasecmp(request, "POST") == 0) {
		cgi = 1;
	}
	
	//reset i
	i = 0;
	//skip over white space
	while ((isspace((int)buf[j])) && (j < sizeof(buf))) {
		j++;
	}
	while ((!isspace((int)buf[j])) && (i < sizeof(fType) - 1) && (j < sizeof(buf))) {
		fType[i] = buf[j];
		i++;
		j++;
	}
	fType[i] = '\0';

	if (strcasecmp(request, "GET") == 0) {
		str = fType;
		while ((*str != '?') && (*str != '\0')) {
			str++;
		}
		if (*str == '?') {
			cgi = 1;
			*str = '\0';
			str++;
		}
	}
	

	sprintf(fullPath, "ServerFiles%s", fType);
	//duplicate the path for testing without /index.html below	
	shortPath = strdup(fullPath);
	//strcat html file name to end of full path
	if (fullPath[strlen(fullPath) - 1] == '/') {
		strcat(fullPath, "index.html");
	}
	
	//if index.html file does not exist in ServerFiles directory, treat as directory listing
	//handle directory listing
	int skip = 0;
	if ((file = fopen(fullPath, "r")) == NULL) {
		skip = 1; //skip == 1 tells the program to skip execution if we are looking at a DIR
		DIR *directory;
		struct dirent *d;
		//check if in directory
		//help from: http://stackoverflow.com/questions/3554120/open-directory-using-c
		if ((directory = opendir(shortPath)) != NULL) {
			// Write content type to client
			sprintf(buff, "Directory Listing: \n\n");
 			write(client, buff, strlen(buff));
			// Write the file/folder names to client
			while((d = readdir(directory)) != NULL){
				sprintf(buff, d->d_name);
				// Ignore current and parent directory links
				if(strcmp(buff, ".") != 0 && strcmp(buff, "..") != 0){
					write(client, buff, strlen(buff));
					write(client, "\n", 1);
				}
			}
			closedir(directory);
		}
	}
	
	if (stat(fullPath, &stats) == -1) {
		while ((line > 0) && strcmp("\n", buf)) {
			line = readLine(client, buf, sizeof(buf));
		}
		if (skip == 0) {
			notFound(client);
		}
	} else {
		if ((stats.st_mode & S_IFMT) == S_IFDIR) {
			strcat(fullPath, "/index.html");
		}
		if (skip == 0) { //skip execution if looking at a directory
			/* S_IXGRP to exec/search for permission bit for group owner of file
			 * S_IXUSR to search for directories permission bit for owner of file
			 * S_IXOTH = (S_IROTH | S_IWOTH | S_IXOTH)
			 * S_IFDIR = directory check
			 */
			if ((stats.st_mode & S_IXGRP) || (stats.st_mode & S_IXUSR) || (stats.st_mode & S_IXOTH)) {
				cgi = 1;
			}
			//run appropriate function for cgi or !cgi case
			if (!cgi) {
				execFile(client, fullPath);
			} else {
				execCGI(client, fullPath, request, str);
			}
		}
	}

	close(client);
}


char *filetype(char *f) {
	char *c;
	if ((c = strrchr(f, '.')) != NULL) {
		return c + 1;
	}
	return "";
}

/*For personal reference: ssize_t send(int sockfd, const void *buf, size_t len, int flags);
 * The send() call may be used only when the socket is in a connected state
 * (so that the intended recipient is known). The only difference between send()
 * and write(2) is the presence of flags.
 */
//prints the appropriate http header
void header(int client, const char *fileName, char* content) {
	char buf[1024];	
	strcpy(buf, "HTTP/1.1 200 OK\r\n");
	send(client, buf, strlen(buf), 0);
	strcpy(buf, "Server: http/1.1\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "Content-Type: %s\r\n\r\n", content);
	send(client, buf, strlen(buf), 0);
}

//do_cat places the file on a socket
void do_cat(int client, FILE *file, char* fd) {
	char buf[10240];
	int pic;
	int picToggle = 0; //are we looking at an image file

	//determining the file type using the pointer to the fd
	char *fType = filetype(fd);
	//default content setting
	char *content = "text/plain";
	//check and set content-type
	if (strcmp(fType, "html") == 0) {
		content = "text/html";
	} else if (strcmp(fType, "gif") == 0) {
		content = "image/gif";
		picToggle = 1;
	} else if (strcmp(fType, "jpeg") == 0) {
		content = "image/jpeg";
		picToggle = 1;
	} else if (strcmp(fType, "jpg") == 0) {
		content = "image/jpg";
		picToggle = 1;
	}  else if (strcmp(fType, "png") == 0) {
		content = "image/png";
		picToggle = 1;
	}

	header(client, fd, content);
	
	if (picToggle == 1) {
		//retrieve fd for picture
		pic = open(fd, O_RDONLY, 0);
		struct stat s;
		if (fstat(pic, &s) == -1) {
			perror("Error: Stat\n");
		}
		size_t total = 0;
		ssize_t bytesSent;
		int picSize = s.st_size;
		if(picSize == -1) {
			perror("Error: File Size\n");
		}
		// Send file to client
		while(total < picSize){
			bytesSent = sendfile(client, pic, 0, picSize - total);
			if(bytesSent <= 0) {
				perror("Error: File Sending\n");
			}
			total += bytesSent;
		}
		
	}
	fgets(buf, sizeof(buf), file);
	while (!feof(file)) {
		send(client, buf, strlen(buf), 0);
		fgets(buf, sizeof(buf), file);
	} 
}



//handles errno values
void errorControl(const char *c) {
	perror(c);
	exit(1);
}

//execCGI handles cgi file execution
//Help from - reading query_string from shell script:
//http://www.unix.com/shell-programming-and-scripting/229661-how-read-query-string-shell-script.html
void execCGI(int client, const char *path, const char *request, const char *query_string) {
	char buf[10240];
	char c;
	int state, i;
	int cgiOut[2];
	int cgiIn[2];
	char functionEnv[1024];
	char length[1024];
	char queryEnv[1024];
	int line = 1;
	int contentLen = -1;
	pid_t pid;
	buf[0] = 'A';
	buf[1] = '\0';

	//if request is a get
	if (strcasecmp(request, "GET") == 0) {
		while ((line > 0) && strcmp("\n", buf)) {
			line = readLine(client, buf, sizeof(buf));
		}
	} else { //if request is a post
		line = readLine(client, buf, sizeof(buf));
		while ((line > 0) && strcmp("\n", buf)) {
			buf[15] = '\0';
			if (strcasecmp(buf, "Content-Length:") == 0) {
				contentLen = atoi(&(buf[16]));
			}
			line = readLine(client, buf, sizeof(buf));
		}
		if (contentLen == -1) {
			errorControl("Error: Invalid contentLen.\n");
			return;
		}
	}

	sprintf(buf, "HTTP/1.1 200 OK\r\n");
	send(client, buf, strlen(buf), 0);
	
	if (pipe(cgiOut) < 0) {
		errorControl("Error: Unable to pipe cgiOut.\n");
		return;
	}
	if (pipe(cgiIn) < 0) {
		errorControl("Error: Unable to pipe cgiIn.\n");
		return;
	}

	if ((pid = fork()) < 0) {
		errorControl("Error: Unable to fork process.\n");
		return;
	} 

	if (pid == 0) { //child (cgi script)
		dup2(cgiOut[1], 1);
		dup2(cgiIn[0], 0);
		close(cgiOut[0]);
		close(cgiIn[1]);
		sprintf(functionEnv, "REQUEST_METHOD=%s", request);
		putenv(functionEnv);
		if (strcasecmp(request, "GET") == 0) { //if: get request
			sprintf(queryEnv, "QUERY_STRING=%s", query_string);
			putenv(queryEnv);
		} else { //else: post request
			sprintf(length, "CONTENT_LENGTH=%d", contentLen);
			putenv(length);
		}
		execl(path, path, NULL);
		exit(0);
	} else { //parent
		close(cgiOut[1]);
		close(cgiIn[0]);
		//post request
		if (strcasecmp(request, "POST") == 0) {
			for (i = 0; i < contentLen; i++) {
				recv(client, &c, 1, 0);
				write(cgiIn[1], &c, 1);
			}
		}
		while (read(cgiOut[0], &c, 1) > 0) {
			send(client, &c, 1, 0);
		}
		close(cgiOut[0]);
		close(cgiIn[1]);
		waitpid(pid, &state, 0);
	}
}

//place entire line in buffer. Take a line of the file from the socket.
//adds a newline char to the line if one is not already there.
int readLine(int fd, char *buf, int size) {
	int x;
	int i = 0;
	char randC = '\0';

	//read in each line in the file up until the '\n' char marks the end of the line
	while ((i < size - 1) && (randC != '\n')) {
		x = recv(fd, &randC, 1, 0);
		if (x > 0) {
			if (randC == '\r') {
				//MSG_PEEK - receive operation returns data from start of queue
				//without removing that data from the queue.
				x = recv(fd, &randC, 1, MSG_PEEK);
				if ((x > 0) && (randC == '\n')) {
					recv(fd, &randC, 1, 0);
				} else {
					randC = '\n';
				}
			}
			buf[i] = randC;
			i++;
		} else {
			randC = '\n';
		}
	}
	//reset buf[i]
	buf[i] = '\0';
	return(i);
}


//handle 404 error
void notFound(int client) {
	char buf[1024];
	sprintf(buf, "HTTP/1.1 404 NOT FOUND\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "Server: http/1.1\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "Content-Type: text/html\r\n\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "<HTML><TITLE>Error 404 Not Found</TITLE>\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "<BODY>The specified URL cannot be found. ERROR 404 \r\n</BODY></HTML>\r\n");
	send(client, buf, strlen(buf), 0);
}


//executes non-cgi files - separate file headers then output accordingly
void execFile(int client, const char *fileName) {
	int line = 1;
	char buf[2048];
	FILE *file = NULL;
	buf[0] = 'A';
	buf[1] = '\0';
	
	//print header then cat file
	while ((line > 0) && strcmp("\n", buf)) {
		line = readLine(client, buf, sizeof(buf));
	}
	file = fopen(fileName, "r");
	if (file == NULL) {
		notFound(client);
	} else {
		do_cat(client, file, fileName);
	}
	fclose(file);
}

//Listens for connections on some port.
int bindToPort(char *port) {
	int http = 0;
	struct sockaddr_in server;

	//First we open a new socket with the socket() call
	http = socket(PF_INET, SOCK_STREAM, 0);
	if (http == -1)
		errorControl("Error: Unable to open socket.\n");
		
	memset(&server, 0, sizeof(server));
	
	//initialize server socket
	//htons() converts unsigned short integer hostshort from host byte order to network byte order. 
	server.sin_family = AF_INET;
	server.sin_port = htons(atoi(port));
	server.sin_addr.s_addr = htonl(INADDR_ANY);
	
	//help understanding bind: http://stackoverflow.com/questions/27014955/socket-connect-vs-bind
	//bind "assigns a name to a socket"
	if (bind(http, (struct sockaddr *)&server, sizeof(server)) < 0)
		errorControl("Error: bind()");
	
	//if the int value of port == 0 then dynamically allocate port
	if (((int) strtol(port, (char**)NULL, 10)) == 0) {		
		/* int getsockname(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
		 * getsockname() returns the current address to which the socket sockfd
        	 * is bound, in the buffer pointed to by addr.
		 * Returns: 
		 * On success, zero is returned. On error, -1 is returned, and errno
		 * is set appropriately.
		 */
		int serverLen = sizeof(server);		
		if (getsockname(http, (struct sockaddr *)&server, &serverLen) == -1)
			errorControl("Error: getsockname()");
		
		*port = ntohs(server.sin_port);
	}
	if (listen(http, 5) < 0)
		errorControl("Error: listen()");
	return(http);
}

//handles 501 error
void notImplemented(int client) {
	char buf[1024];
	sprintf(buf, "HTTP/1.1 501 Method Not Implemented\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "Server: http/1.1\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "Content-Type: text/html\r\n\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "<HTML><HEAD><TITLE>Error 501 Method Not Implemented\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "</TITLE></HEAD>\r\n");
	send(client, buf, strlen(buf), 0);
	sprintf(buf, "<BODY>Requested method not implemented by server. \r\n</BODY></HTML>\r\n");
	send(client, buf, strlen(buf), 0);
}


int main(int argc, char*argv[]){
	int servSocket = -1;
	int cliSocket = -1;
	int port;
	port = (int) strtol(argv[1], (char**)NULL, 10); //make argv[1] (port) an int
	struct sockaddr_in clientName;
	int clientLen = sizeof(clientName);
	pthread_t nextThread;
	//u_short is unsigned short - uses only positive values instead of 2's compliment
	//u_short holds values between 0 and 65535
	//u_short port = 0; **instead, port will be an int from argv[1]
	if (port < 5000 || port > 65536) {
		fprintf(stderr, "Error: Improper port value. Port must be between 5000 and 65536.\n");
		exit(1);
	}
	
	char tempbuf[10];
	int toggle;
	printf("Enter 1 (enable) or 0 (disable) for multi-threading: \n");
	//read in from stdin - 1 for threading, 0 no threading
	fgets(tempbuf, 10, stdin);
	toggle = atoi(tempbuf);

	if (toggle != 0 && toggle != 1) {
		fprintf(stderr, "Error: Invalid value for thread-toggle feature. \n");
		exit(1);
	}
	servSocket = bindToPort(argv[1]); //open socket on port
	if(argc != 2) {
		fprintf(stderr, "Error: Invalid number of arguments. \n");
		exit(1);
	}

	//listen for (up to 50) connections
	if(listen(servSocket, 50) < 0) {
		fprintf(stderr, "Error: listen().\n");
	}

	printf("Server is running http on port: %s\n", argv[1]);
	while (1) {
		//bind the client's address and socket & return fd referring to socket
		cliSocket = accept(servSocket, (struct sockaddr *)&clientName, &clientLen);
		//check if accept worked
		if (cliSocket == -1) {
			errorControl("Error: accept()");
		}
		nextRequest(cliSocket);

		//user input 1 for threading, 0 for no threading
		//Note: threading with pthread
		if (toggle == 1) {
			if (pthread_create(&nextThread , NULL, nextRequest, cliSocket) != 0) {
				perror("Error: pthread_create()");
			}
		} else if (toggle == 0 && fork() == 0) {	
			close(servSocket);
			nextRequest(((void *)&cliSocket));
			close(cliSocket);
			exit(0);
		}
		
		close(cliSocket);
	}
	close(servSocket);
	return(0);
}
