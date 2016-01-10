/*
 * Created by Ben Blau: bblau94@bu.edu
 * Due: October 2nd 2014
 * Professor Matta CS455
 * PA1 Client Part 2
 * Filename: Client.java
 * Example of client-server from source http://docs.oracle.com/javase/tutorial/networking/sockets/readingWriting.html
 */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Date;

public class Client {
  public static void main(String[] args) throws IOException {
    
    if (args.length != 2) {
      System.err.println("Usage: java Client <host name> <port number>");
      System.exit(1);
    }
    
    String hostName = args[0];
    int portNum = Integer.parseInt(args[1]);
    
    try {
            
//making connection
      
      Socket socket = new Socket(hostName, portNum);
      PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
      BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            
//make parameters for probe message
      
      //the server delay
      int sDelay = 0;
      //number of probes
      int probes = 10;
      //payload size
      int plSize = 100;
  
            
//count to exit while loop
      
      int count = 1;
            
//total RTT will be used to calculate the average RTT
      double tTPUT = 0;
      long tRTT = 0;
           
//build and deliver CSP Message to server
     
      //ui = user input
      String uI = "s rtt " + probes + " " + plSize + " " + sDelay;
      out.println(uI);
      System.out.println("From Server: " + in.readLine());
      
      while (count <= probes) {
        String payload = "";
                
//constructs (string)payload with a specific number of bytes
        int i = 0;
        
        while (i < plSize) {
          payload = payload + 'i';
          i++;
        }
        
        
//build measurement method

        uI = "m " + count + " " + payload;
        
//current time

        Date sentTime = new Date();
        long sendTime = sentTime.getTime();
        
//send message
        
        out.println(uI);
        
//server reply

        String sReply = in.readLine();
        System.out.println("From server: " + sReply);
        
//time of received message
       
        Date receivedTime = new Date();
        long recTime = receivedTime.getTime();
             
//compute RTT
        
        System.out.println("RTT: " + (recTime - sendTime) + "ms");      
 
//computer throughput
        
        double rttdouble = recTime - sendTime;
        double tput = plSize / rttdouble;
        System.out.println("TPUT: " + (tput * 8) + "kbps");
        tTPUT = tTPUT + (tput * 8); 
//compute average
        
        tRTT = tRTT + (recTime - sendTime);
        count++;

      }
      
//computer average throughput using total throughput
      System.out.println("Average Throughput: " + (tTPUT/probes) + "kbps");
      
//compute average RTT using total RTT
  
      System.out.println("Avg RTT: " + (tRTT/probes) + "ms");
      
//construct and send termination message
      
      String terminationMessage = "t";
      out.println(terminationMessage);
      System.out.println("From Server: " + in.readLine());
            
//close connection
    
      socket.close();
    
    }
    
    catch (UnknownHostException e) {
      System.err.println("Unknown Host: " + hostName);
      System.exit(1);
    } 
    
    catch (IOException e) {
      System.err.println("I/O error for connection to " + hostName);
      System.exit(1);
    } 
  }
}