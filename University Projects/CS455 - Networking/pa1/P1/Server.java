/*
 * Created by Ben Blau: bblau94@bu.edu
 * Due: October 2nd 2014
 * Professor Matta CS455
 * PA1 Server Part 1
 * Filename: Server.java
 */

import java.net.*;
import java.io.*;

public class Server {
  public static void main(String[] args) throws IOException {
//check arguments    
    if (args.length != 1) {
      
      System.err.println("Usage: java Server <port number>");
      System.exit(1);
      
    }
//set port number    
    int portNum = Integer.parseInt(args[0]);        
    
    try {
      
//create connection      
      ServerSocket sSocket = new ServerSocket(Integer.parseInt(args[0]));
      Socket cSocket = sSocket.accept();
      PrintWriter out = new PrintWriter(cSocket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(cSocket.getInputStream()));
      
      
      String input;
//reads the user input (uI) from client      
      while ((input = in.readLine()) != null) {
//echos message back to client     
        out.println(input);
        
      }
      
      sSocket.close();
            
    }
    
    catch (IOException e) {
      
      System.out.println("I/O Exception while listening on port " + portNum);
      System.out.println(e.getMessage());       
      
    }
    
    
  }
}