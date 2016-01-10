/*
 * Created by Ben Blau: bblau94@bu.edu
 * Due: October 2nd 2014
 * Professor Matta CS455
 * PA1 Server Part 2
 * Filename: Server.java
 * Listens, interprets, and returns messages to client.
 * Example of client-server from source http://docs.oracle.com/javase/tutorial/networking/sockets/readingWriting.html
 */

import java.net.*;
import java.io.*;

public class Server {
  public static void main(String[] args) throws IOException {
//checking arguments    
    if (args.length != 1) {
      
      System.err.println("Usage: java Server <port number>");
      System.exit(1);
      
    }
//sets port number    
    int portNum = Integer.parseInt(args[0]);
    
    try {
//listening for a connection      
      ServerSocket sSocket = new ServerSocket(portNum);
      Socket cSocket = sSocket.accept();
      PrintWriter out = new PrintWriter(cSocket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(cSocket.getInputStream()));
      
//variable declaration      
      String input;
      String protocolPhase;
      String measurementType;
      String payload;
      String messageSize;
      int probes = 0;
      int sDelay = 0;
      int count = 0;
      int probeSeq = 0;
      
      
      if ((input = in.readLine()) != null) {
        
        String[] elements = input.split(" ");
//testing for proper CSP message        
        if (elements[0].equals("s")) {
          
          try {
            
            protocolPhase = elements[0];
            if (elements[1].equals("rtt") || elements[1].equals("tput")) {
              measurementType = elements[1];
              
            }
            
            else {
              
              out.println("404 ERROR: Invalid Connection Setup Message");
              
            }
//setting variables to data contained in CSP            
            probes = Integer.parseInt(elements[2]);
            messageSize = elements[3];
            sDelay = Integer.parseInt(elements[4]);
            out.println("200 OK: Ready");
            
          }
          
          catch (Exception e) {
            
            out.println("404 ERROR: Invalid Connection Setup Message");
            
          }
          
        }
        
        else {
          
          out.println("404 ERROR: Invalid Connection Setup Message");
          
        }
        
      }
//repeat for expected number of probes      
      while(count < probes) {
        
        input = in.readLine();
        String[] elements = input.split(" ");
//checking for correct formating of measurement message        
        if (elements[0].equals("m")) {
          
          try {
            
            protocolPhase = elements[0];
            probeSeq = Integer.parseInt(elements[1]);
            
            if (probeSeq != (count+1)) {
              
              out.println("404 ERROR: Invalid Measurement Message");
              
            }
            
            payload = elements[2];
//if server delay, sleep the thread            
            if (sDelay > 0) {
              
              try {
                
                Thread.sleep(sDelay);
                
              }
              
              catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
                
              }
              
            }
            
            out.println(input);
            
          }
          
          catch (Exception e) {
            
            out.println("404 ERROR: Invalid Measurement Message");
            
          }
          
        }
        
        else {
          
          out.println("404 ERROR: Invalid Measurement Message");
          
        }
        
        count++;
        
      }
      
      input = in.readLine();
      String[] elements = input.split(" ");
//checking for a termination message      
      if (elements[0].equals("t")) {
        
        try {
//closes connection          
          out.println("200 OK: Closing Connection");
          sSocket.close();
          
        }
//various error checking        
        catch (Exception e) {
          
          out.println("404 ERROR: Invalid Connection Termination Message");
          
          sSocket.close();
          
        }
        
      }
      
      else {
        
        out.println("404 ERROR: Invalid Connection Termination Message");
        sSocket.close();          
        
      }
      
    }
    
    catch (IOException e) {
      
      System.out.println("Exception when listening on port " + portNum);
      System.out.println(e.getMessage());       
      
    }
    
  }
  
}