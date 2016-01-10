Ben Blau (bblau94@bu.edu)
October 2nd 2014
Professor Matta - CS 455 PA 1
My graphs and experiment data were submitted to the CS 455 box.
In order to run the file you must compile both the server and client program using the javac command. After that you can start the Server.java by typing “java Server <port number>”. To run the Client.java type “java Client <host name> <port number>”. For part two of the assignment the default settings are as follows: Server Delay = 0 (ms), Payload Size = 1 (byte), Number of Probes = 10. These can be changed by going into the client program and changing the probes, plsize, and sDelay variables.
Design and Specifications:
Part 1:
For error checking, exceptions will be thrown in these cases: If an incorrect number of arguments is fed in to the program it will close. If an IO exception occurs during runtime of the server then the exception is caught. In both cases a proper error message is returned.

Client.java (type into command line: java Client <host name> <port number>)
I began by researching client-server methods online (source provided in code). The echo client here is very similar to the client created in part two. The only difference here is that there is a variable denoted “uI” which stands for the user’s input which is the output to the server. Following this the server’s response is returned to the console and the connection is closed. See part 2 for more details on how the clients work. 

Server.java (type into command line: java Server <port number>)
In the server client I started by putting in an integer variable to store the port number for execution purposes. The server makes a socket to use as a connection with the client side socket on a specific port. Using a PrintWriter object the server writes data to the connection which is read with a BufferedReader object. Following this the server records the incoming information from the client using the in.readLine() command. Following this the recorded information is pushed back to the client at which point the process is finished, the socket closes, and the server shuts down.



Part 2:
Client.java Client.java (type into command line: java Client <host name> <port number>)
For error checking, exceptions will be thrown in these cases: If the input host name is not found the program will throw an UnknownHostException and if it is found but there is no socket available then an IO exception will be caught. If an incorrect amount of arguments are fed in then the program will close. In all of these cases an error message will be returned. 
The client program starts by putting the input host name and port number into two variables and then starting a socket (socket name in code: socket) connection to the server. The initial setup with the number of probes, server delay, and payload size needs to be input in the code by the user and changed for desired output. Following this the connection setup phase message gets sent to the server at which point a response will then also be output by the server. Using a loop I iterated the number of probes and following that the payload is constructed in another loop by iterating the number contained in “plSize.” Every iteration of the while loop a character is added into the payload string representing a single byte of data. After this a reply from the server is received and sent to the console. The RTT (ms) is the calculated by subtracting the time it takes to send from the time it takes for the message to be received. Every time this happens the RTT is added to a total which is later used to calculate the average. After this the client sends a message to the server to terminate the process at which point the server closes the socket.
Server.java (type into command line: java Server <port number>)
This server client starts up the same as the last one. The server starts by declaring all of the necessary variables/objects and then looks for a connection setup phase (CSP) message in the first line. The message is read and its information is processed accordingly. Exceptions are thrown in necessary situations where incorrect information is given. Looping through the number of probes given in the message, a message is formed. Based on the assigned server delay the thread will wait a specific amount of time (ms) by using the command “Thread.sleep(sDelay).” The measurement is then returned to the client and completes the iteration of the loop. Upon completion the server then looks for a message to terminate from the client, outputs an appropriate response, and closes the socket. An error is thrown and the client is closed if the client sends an incorrect termination message. 

How I tested my code:
For part 1 I started by error checking my client and server on the bu (csa2.bu.edu) server. I started with a low server delay and payload and my programs ran fine. I slowly added in different ways to test for errors in my program which seemed to be the biggest issue. I tested for incorrect inputs into the programs and throw appropriate errors in the case that any were found. I also had to check for improper formatting within the measurement message, termination message, and the CSP message. If any were found I printed the proper error message and had the connection close. Similarly, I used the NYU server (pcvm2-2.genirack.nyu.edu) to test my part two programs. 

Possible tradeoffs and extensions:
You could extend the client and server programs in a few different ways. Some good ways would be to make the server multi-threaded. This would allow for more clients to connect at any point in time. Another extension we could add would to be to test the RTT at much higher payload sizes than 1000 bytes to see how the RTT is effected by this. 


