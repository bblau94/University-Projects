/*
 * Created by Ben Blau: bblau94@bu.edu
 * Due: October 2nd 2014
 * Professor Matta CS455
 * PA1 Client Part 1
 * Filename: Client.java
 */

import java.io.*;
import java.net.*;

public class Client {
  public static void main(String[] args) throws IOException {
//check arguments    
    if (args.length != 2) {
      
      System.err.println(
                         "Usage: java Client <host name> <port number>");
      System.exit(1);
      
    }
    
    
    String hostName = args[0];
    int portNum = Integer.parseInt(args[1]);
    
    
    try {
      
//create connection      
      Socket socket = new Socket(hostName, portNum);
      PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));      
      
//user input (uI)/message to send      
      String uI = "Hello World\n";
      
//sends the message to server      
      out.println(uI);
//receives reply from server      
      System.out.println("From server: " + in.readLine());
    }
    
    catch (UnknownHostException e) {
      
      System.err.println("Unknown Host: " + hostName);
      System.exit(1);
      
    } 
    catch (IOException e) {
      
      System.err.println("I/O for the connection to " + hostName + "could not be received.");
      System.exit(1);
      
    } 
    
  }
  
}