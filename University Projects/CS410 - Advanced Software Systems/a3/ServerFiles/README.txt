CS 410 
Assignment 3
Team members: Ben Blau, Tyler Butler, Jeffery Zurita

Outline:

Our web server, webserv.c, is able to accomplish a variety of functions including:
	1. list contents of a directory
	2. retrieve file for viewing on client
	3. running cgi scripts
	4. Handle static/dynamic content requests.

The server can handle both static and dynamic content requests:
Static: Content is retrieved from a pre-existing file on the server
Dynamic: Run a program on the server, process data, and generate an HTML compliant file
  	            to send back to the client.

The server is able to accomplish these with a single thread or using multi-threading, enabled by the user on startup. 

The server handles multiple HTML states including:
  200 (Successful Request)
  404 (Not Found)
  501 (Not Implemented) - Server does not recognize the request method.

-----------------------------------------------------------------------------------------------------

Setup:

You must first run the make file on your computer with: "make all"
To clean type: "make clean"

Then, you can run the web server using '$./webserv port-number', declaring port-number between 5000-65536.

You will then be asked whether or not to enable or disable multithreading by entering 1 or 0.
Our threading solution uses pthreads.

After you make the choice, the web server should be running on your specified port. 

-----------------------------------------------------------------------------------------------------

Design:
The server sets up a socket connection on the specified port by using the line
servSocket = bindToPort(argv[1]);
and then listens for up to 50 connections. It executes an infinite while loop that accepts socket connections on the specified port. If multithreading is enabled, inside of this loop for each new 
connection 'pthread_create' is called to create a new thread for each client. When the client disconnects, the code to close the server socket and client sockets is called within this loop as well.

The 'bindToPort(char *port)' function works mainly through the 'socket' system call which creates an endpoint of network communication. The server socket is initialized and then binded to the specified port, then returned. 

Files, such as HTML files (and excluding CGI files), are sent to the client from the web server through the 'execFile' method. It calls the 'do_cat' method which essentially outputs the file's text contexts directly onto the socket to the client. 

CGI scripts are executed on the server through the method "execCGI". It takes in the path of the CGI file and any inputs, and prints the output of the CGI file to the socket.

The webserver is in the a3 folder. Inside a3 is ServerFiles. The server looks for this folder on requests. All files should be placed inside this folder if you wish to pull them up on a client. The server will default to an "index.html" file. If the file does not exist, the server will print the directory listing.
