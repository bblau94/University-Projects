/* StudentNetworkSimulator.java
 * Ben Blau (bblau94@bu.edu) U94434268
 * Due: September 30th 2014 1:00PM
 */

import java.util.*;
import java.io.*;

public class StudentNetworkSimulator extends NetworkSimulator
{
  /*
   * Predefined Constants (static member variables):
   *
   *   int MAXDATASIZE : the maximum size of the Message data and
   *                     Packet payload
   *
   *   int A           : a predefined integer that represents entity A
   *   int B           : a predefined integer that represents entity B 
   *
   * Predefined Member Methods:
   *
   *  void stopTimer(int entity): 
   *       Stops the timer running at "entity" [A or B]
   *  void startTimer(int entity, double increment): 
   *       Starts a timer running at "entity" [A or B], which will expire in
   *       "increment" time units, causing the interrupt handler to be
   *       called.  You should only call this with A.
   *  void toLayer3(int callingEntity, Packet p)
   *       Puts the packet "p" into the network from "callingEntity" [A or B]
   *  void toLayer5(String dataSent)
   *       Passes "dataSent" up to layer 5
   *  double getTime()
   *       Returns the current time in the simulator.  Might be useful for
   *       debugging.
   *  int getTraceLevel()
   *       Returns TraceLevel
   *  void printEventList()
   *       Prints the current event list to stdout.  Might be useful for
   *       debugging, but probably not.
   *
   *
   *  Predefined Classes:
   *
   *  Message: Used to encapsulate a message coming from layer 5
   *    Constructor:
   *      Message(String inputData): 
   *          creates a new Message containing "inputData"
   *    Methods:
   *      boolean setData(String inputData):
   *          sets an existing Message's data to "inputData"
   *          returns true on success, false otherwise
   *      String getData():
   *          returns the data contained in the message
   *  Packet: Used to encapsulate a packet
   *    Constructors:
   *      Packet (Packet p):
   *          creates a new Packet that is a copy of "p"
   *      Packet (int seq, int ack, int check, String newPayload)
   *          creates a new Packet with a sequence field of "seq", an
   *          ack field of "ack", a checksum field of "check", and a
   *          payload of "newPayload"
   *      Packet (int seq, int ack, int check)
   *          chreate a new Packet with a sequence field of "seq", an
   *          ack field of "ack", a checksum field of "check", and
   *          an empty payload
   *    Methods:
   *      boolean setSeqnum(int n)
   *          sets the Packet's sequence field to "n"
   *          returns true on success, false otherwise
   *      boolean setAcknum(int n)
   *          sets the Packet's ack field to "n"
   *          returns true on success, false otherwise
   *      boolean setChecksum(int n)
   *          sets the Packet's checksum to "n"
   *          returns true on success, false otherwise
   *      boolean setPayload(String newPayload)
   *          sets the Packet's payload to "newPayload"
   *          returns true on success, false otherwise
   *      int getSeqnum()
   *          returns the contents of the Packet's sequence field
   *      int getAcknum()
   *          returns the contents of the Packet's ack field
   *      int getChecksum()
   *          returns the checksum of the Packet
   *      int getPayload()
   *          returns the Packet's payload
   *
   */
  
  /*   Please use the following variables in your routines.
   *   int WindowSize  : the window size
   *   double RxmtInterval   : the retransmission timeout
   *   int LimitSeqNo  : when sequence number reaches this value, it wraps around
   */
  
  
  public static final int FirstSeqNo = 0;
  private int WindowSize;
  private double RxmtInterval;
  private int LimitSeqNo;
  
  //The expected sequence number of packet which will be received from A in a next turn
  int expectedSeqNo = 0;
  //Expected ackNo for A input
  int expectedAckNo = 0;
  
  
  int base = 0;
  //seq. no. of oldest unack packet = base
  int nextSeqNo = 0; 
  //next packed to send/smallest unused seq. no. = nextSeqNo
  
  Packet p;
  Packet ack;
  Packet[] buffer;
  Message[] bufferMsg;
  Packet[] ackBuf;
  Packet[] receivedAckBuf;
  //Buffer for received ack
  
  int ackBufferSize = 0;
  int bufSize = 0;
  //ack and buffer size
  
  int messageBufBase = 0;
  int messageBufSize = 0;
  int rttTime = 0;
  
  
  int corruptions = 0;
  int retransmits = 0;
  int numLost = 0;
  
  double rttReceived = 0.0;
  double rttTotal = 0.0;
  double rttSent = 0.0;
  
  /*
   double communicationTotal = 0.0;
   int communicationTime = 0;
   double communicationReceived = 0.0;
   double communicationSent = 0.0;
   */
  
  
  // Add any necessary class variables here.  Remember, you cannot use
  // these variables to send messages error free!  They can only hold
  // state information for A or B.
  // Also add any necessary methods (e.g. checksum of a String)
  
  // This is the constructor.  Don't touch!
  public StudentNetworkSimulator(int numMessages,
                                 double loss,
                                 double corrupt,
                                 double avgDelay,
                                 int trace,
                                 int seed,
                                 int winsize,
                                 double delay)
  {
    super(numMessages, loss, corrupt, avgDelay, trace, seed);
    WindowSize = winsize;
    LimitSeqNo = winsize+1;
    RxmtInterval = delay;
  }
  
  
  // This routine will be called whenever the upper layer at the sender [A]
  // has a message to send.  It is the job of your protocol to insure that
  // the data in such a message is delivered in-order, and correctly, to
  // the receiving upper layer.
  protected void aOutput(Message message)
  {
    //If the packet can be accomodated in the Window send it immediately
    if (nextSeqNo < (base + WindowSize)) {
      //No messages in the buffer, send the current message
      if (messageBufSize == 0) {
        helperA(message);
      }
      
      //Messages currently stored in buffer - start sending messages starting with earliest non-sent message in bufferMsg
      else {
        bufferMsg[messageBufSize] = message;
        messageBufSize++;
        //Sends earliest unsent message put in buffer
        System.out.println("Message from bufferMsg: " + messageBufBase);
        helperA(bufferMsg[messageBufBase]);
        messageBufBase++;
      }
    }
    
    //Tried to send message where max num of packets in window is still unacknowledged. Put msg in buffer for use at later time
    else {
      System.out.println("Adding messasge to buffer");
      System.out.println("bufferMsg adding message: " + messageBufSize);
      bufferMsg[messageBufSize] = message;
      messageBufSize++;
    }
    
  }
  
  //Helper method for creating and sending a packet from A to B
  private void helperA(Message message) {
    String data = message.getData();
    
    //Initial packet, use sequenceNo and ackNo of zero    
    int checkSum = calcCheckSum(data, nextSeqNo, 0);
    Packet p = new Packet(nextSeqNo, 0, checkSum, data);
    
    buffer[nextSeqNo] = p;
    bufSize++;
    
    //System.out.println("Added packet to buffer: " + nextSeqNo);
    
    toLayer3(0, p);
    rttTime++;
    //communicationTime++;
    rttSent = getTime();
    //communicationSent = getTime();
    System.out.println("Sending packet from A with sequence number: " + nextSeqNo + " and checksum: " + checkSum);
    //First packet sent - start timer
    if (base == nextSeqNo) {
      startTimer(0, 25.0);
    }
    nextSeqNo++;     
  }
  
  // This routine will be called whenever a packet sent from the B-side 
  // (i.e. as a result of a toLayer3() being done by a B-side procedure)
  // arrives at the A-side.  "packet" is the (possibly corrupted) packet
  // sent from the B-side.
  protected void aInput(Packet packet)
  {
    
    int ackNo = packet.getAcknum();
    //Received corrupt ACK, timeout. 
    if (!notCorrupt(packet)) {
      System.out.println("A: Received corrupt ACK");
      rttReceived = getTime();
      rttTotal = rttReceived - rttSent;
      rttSent = 0.0;
      rttReceived = 0.0;
      corruptions++;
    }
    
    //Not a duplicate ACK and isn't corrupt, slide the window forward. 
    if (notCorrupt(packet) && (receivedAckBuf[ackNo] == null)) {
      //communicationSent = 0.0;
      //communicationReceived = 0.0;
      //communicationReceived = getTime();
      //communicationTotal = (rttReceived - rttSent);
      
      rttReceived = getTime();
      rttTotal = rttReceived - rttSent;
      rttSent = 0.0;
      rttReceived = 0.0;
      receivedAckBuf[ackNo] = new Packet(packet);
      expectedAckNo++;
      base = ackNo + 1;
      System.out.println("Received non corrupt ACK: " + ackNo);
      
      //No outstanding, unacknowledged packets. Stop timer 
      if (base == nextSeqNo) {
        System.out.println("base=nextSeqNo on received ACK, stopping timer");
        stopTimer(0);
      }
      //Yes outstanding, unacknowledged packets. Restart timer 
      else {
        System.out.println("Restarting Timer");
        stopTimer(0);
        startTimer(0, 25.0);
      }
    }
    
    else {
      System.out.println("Duplicate ACK received, the expected ACK is: " + expectedAckNo + " the received ACK is: " + ackNo + " notCorrupt: " + notCorrupt(packet));
      System.out.println("Resending Window");
      numLost++;
      rttReceived = getTime();
      rttTotal = rttReceived - rttSent;
      rttSent = 0.0;
      rttReceived = 0.0;
      stopTimer(0);
      retransmitMsg();
    }
    
  }
  
  // This routine will be called when A's timer expires (thus generating a 
  // timer interrupt). You'll probably want to use this routine to control 
  // the retransmission of packets. See startTimer() and stopTimer(), above,
  // for how the timer is started and stopped. 
  protected void aTimerInterrupt()
  {
    System.out.println("Timer interupt for A hit - resending packets");
    retransmitMsg();
  }
  
  //Resends packets when a timer interupt happens or a duplicate ACK is received
  private void retransmitMsg() {
    //Resend all packets in buffer
    for (int i = base; i < bufSize; i++) {
      System.out.println("Resending packet in buffer no.: " + i);
      toLayer3(0, buffer[i]);
    }
    //Restart timer
    startTimer(0, 25.0);    
    retransmits++;
    rttTime++;
  }
  
  // This routine will be called once, before any of your other A-side 
  // routines are called. It can be used to do any required
  // initialization (e.g. of member variables you add to control the state
  // of entity A).
  protected void aInit()
  {
    buffer = new Packet[1000];
    receivedAckBuf = new Packet[1000];
    bufferMsg = new Message[1000];
    nextSeqNo = 0;
  }
  
  // This routine will be called whenever a packet sent from the B-side 
  // (i.e. as a result of a toLayer3() being done by an A-side procedure)
  // arrives at the B-side.  "packet" is the (possibly corrupted) packet
  // sent from the A-side.
  
  protected void bInput(Packet packet)
  {
    int sequenceNo = packet.getSeqnum();
    String data = packet.getPayload();
    System.out.println("Current incoming packet seq. no.: " + sequenceNo);
    
    if (notCorrupt(packet)) {
      if (expectedSeqNo == sequenceNo) {
        toLayer5(data);
        int ackCsum = calcCheckSum("a", sequenceNo, expectedSeqNo);
        ack = new Packet(sequenceNo, expectedSeqNo, ackCsum, "a");
        ackBuf[expectedSeqNo] = ack;
        System.out.println("B receieved correct packet, sending ACK number: " + expectedSeqNo);
        toLayer3(1, ack);
        expectedSeqNo++;
      }
      else {
        System.out.println("Unexpected received seq. no. from packet: " + sequenceNo + ", resending ACK " + (expectedSeqNo - 1));
        if (expectedSeqNo == 0) {
        }
        else {
          toLayer3(1, ackBuf[expectedSeqNo - 1]);
        }
      }
    }
    
    else {
      System.out.println("B received corrupted packet");
      System.out.println("Checksum of Packet: " + packet.getChecksum() + ", Calculated Checksum: " + calcCheckSum(packet.getPayload(), packet.getSeqnum(), packet.getAcknum()));
    }
  }
  
  // This routine will be called once, before any of your other B-side 
  // routines are called. It can be used to do any required
  // initialization (e.g. of member variables you add to control the state
  // of entity B).
  protected void bInit()
  {
    ackBuf = new Packet[1000];
    expectedSeqNo = 0;
  }
  
  // Use to print final statistics
  protected void Simulation_done()
  {
    //double commAverage = communicationTotal/rttTime;
    double rttAverage = rttTotal/rttTime;
    System.out.println("Avg RTT: " + rttAverage);
    System.out.println("Packets Lost: " + numLost);
    System.out.println("Packets Corrupted: " + corruptions);
    System.out.println("Retransmitted Packets: " + retransmits);
    
  } 
  
  //This uses the number of bytes in the payload multiplied by the sum of the seq. no. and ack no. to determine the checksum
  private int calcCheckSum(String data, int sequenceNo, int ackNo) {
    int sizeOfBytes = data.length();
    int sumOfBytes = 0;
    for (int i = 0; i < sizeOfBytes; i++) {
      sumOfBytes += data.charAt(i);
    }
    
    int calculatedCheckSum = (sequenceNo + ackNo + (sizeOfBytes * sumOfBytes));
    return calculatedCheckSum;
  }
  
  private boolean notCorrupt(Packet packet) {
    return packet.getChecksum() == calcCheckSum(packet.getPayload(), packet.getSeqnum(), packet.getAcknum());
  }
  
}