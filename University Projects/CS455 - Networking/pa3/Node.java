/**
 * This is the class that students need to implement. The code skeleton is provided.
 * Students need to implement rtinit(), rtupdate() and linkhandler().
 * printdt() is provided to pretty print a table of the current costs for reaching
 * other nodes in the network.
 * 
 * Ben Blau (U94434268) (bblau94@bu.edu)
 * In order to run, compile needed files and run "Project3.java"
 */ 
public class Node{ 
  
  public final int INFINITY = 9999;
  
  int[] lkcost;  /*The link cost between node 0 and other nodes*/
  int[][] costs;    /*Define distance table*/
  int nodename;               /*Name of this node*/
  
  /* Class constructor */
  public Node() { }
  
  void rtinit(int nodename, int[] initial_lkcost) {
    
    lkcost = initial_lkcost;
    int size = initial_lkcost.length;
    costs = new int[size][size];
    this.nodename = nodename;
    
    //initialize distance table
    for (int i = 0; i < size; i++) {
      for (int j = 0; j < size; j++) {
        //when there is no connection
        if (i != j) {
          costs[i][j] = INFINITY;
        } else {
          costs[i][j] = initial_lkcost[i]; 
        }
      }
    }
    System.out.println("\nt= " + NetworkSimulator.clocktime + " Initialize Node - " + nodename + "\n");
    transferMinimumCosts();
  }    
  
  //updates the array storing the cost by using the info from rcvdpkt
  void rtupdate(Packet rcvdpkt) {  
    
    int[] distance = rcvdpkt.mincost;
    boolean toSend = false;
    int start = rcvdpkt.sourceid;
    int costTo = costs[start][start];
    //update column x when receiving a packet from node x
    for (int i = 0; i < 4; i++) {
      if (i != nodename) {
        //stop update when going from a node to itself
        if ((distance[i] + costTo) < costs[i][start]) {
          //update the array in the event of new info
          costs[i][start] = distance[i] + costTo;
          toSend = true;
        }
      }
    }
    //prints info
    System.out.println("t = " + NetworkSimulator.clocktime + " Routing packet received from Node " + start + " by Node " + nodename);
    if (toSend) {
      System.out.println("\nModification to Distance Array");
    } else {
      System.out.println("\nDistance Array Unmodified");
    }
    printdt();
    //transfer info to other connected nodes
    if (toSend) {
      transferMinimumCosts();
    }
  }
  
  
  void linkhandler(int linkid, int newcost) {
    
    System.out.println();
    System.out.println("Node link between " + nodename + " and " + linkid + " changed to " + newcost + " from " + costs[linkid][linkid] + "************************************");
    //add difference to entries in column when link change
    for (int i = 0; i < 4; i++) {
      if (costs[i][linkid] != INFINITY) {
        costs[i][linkid] += (newcost - costs[linkid][linkid]);
      }
    }
    transferMinimumCosts();    
  }    
  
  
  //makes/updates the array which contains the minimum cost between nodes - also sends to other routers.
  private void transferMinimumCosts() {
    
    //construct minimum cost array as well as an array to hold the direction taken by the shortest path
    int[] minimum = {costs[0][0], costs[1][0], costs[2][0], costs[3][0]};
    int[] direction = {0, 0, 0, 0}; 
    //adds the minimum distances to nodes
    for (int to = 0; to < 4; to++) {
      for (int from = 0; from < 4; from++) {
        if (costs[to][from] < minimum[to]) {
          direction[to] = from;
          minimum[to] = costs[to][from];
        }
      }
    }
    //duplicate the link for event of poisoning and prevent loops - specific points will be changed to true in the event of a poisoned value
    int[] duplicateArray = {minimum[0], minimum[1], minimum[2], minimum[3]};
    boolean[] poisonArray = {false, false, false, false};  
    
    //sends the array to immediately connected nodes but if the shortest path goes through the node being sent to, link will be poisoned
    for (int receiving = 0; receiving < 4; receiving++) {
      for (int x = 0; x < 4; x++) {
        duplicateArray[x] = minimum[x];
        poisonArray[x] = false;
      }
      //this resets the values at each new node
      
      //if the link exists and the node receiving is not this one, send to appropriate node
      if((receiving != nodename) && (costs[receiving][receiving] < INFINITY)){ 
        
        System.out.println("t= " + NetworkSimulator.clocktime + " Node " + nodename + " send packet to node " + receiving);
        
        for (int i = 0; i < 4; i++){
          
          //poison node - if direction of shortest path goes through node being sent to
          if (direction[i] == receiving) {
            duplicateArray[i] = INFINITY; 
            poisonArray[i] = true;
            System.out.println("Shortest path goes through node " + receiving + " to node " + i  + " - link will be poisoned to prevent loops");
          }
        }
        NetworkSimulator.tolayer2(new Packet(nodename, receiving, duplicateArray));
      }
    }
  }
 
  
  
  
  /* Prints the current costs to reaching other nodes in the network */
  void printdt() {
    switch(nodename) {
      case 0:
        System.out.printf("                via     \n");
        System.out.printf("   D0 |    1     2    3 \n");
        System.out.printf("  ----|-----------------\n");
        System.out.printf("     1|  %3d   %3d   %3d\n",costs[1][1], costs[1][2],costs[1][3]);
        System.out.printf("dest 2|  %3d   %3d   %3d\n",costs[2][1], costs[2][2],costs[2][3]);
        System.out.printf("     3|  %3d   %3d   %3d\n",costs[3][1], costs[3][2],costs[3][3]);
        break;
      case 1:
        System.out.printf("                via     \n");
        System.out.printf("   D1 |    0     2 \n");
        System.out.printf("  ----|-----------------\n");
        System.out.printf("     0|  %3d   %3d \n",costs[0][0], costs[0][2]);
        System.out.printf("dest 2|  %3d   %3d \n",costs[2][0], costs[2][2]);
        System.out.printf("     3|  %3d   %3d \n",costs[3][0], costs[3][2]);
        break;
        
      case 2:
        System.out.printf("                via     \n");
        System.out.printf("   D2 |    0     1    3 \n");
        System.out.printf("  ----|-----------------\n");
        System.out.printf("     0|  %3d   %3d   %3d\n",costs[0][0], costs[0][1],costs[0][3]);
        System.out.printf("dest 1|  %3d   %3d   %3d\n",costs[1][0], costs[1][1],costs[1][3]);
        System.out.printf("     3|  %3d   %3d   %3d\n",costs[3][0], costs[3][1],costs[3][3]);
        break;
      case 3:
        System.out.printf("                via     \n");
        System.out.printf("   D3 |    0     2 \n");
        System.out.printf("  ----|-----------------\n");
        System.out.printf("     0|  %3d   %3d\n",costs[0][0],costs[0][2]);
        System.out.printf("dest 1|  %3d   %3d\n",costs[1][0],costs[1][2]);
        System.out.printf("     2|  %3d   %3d\n",costs[2][0],costs[2][2]);
        break;
    }
  }
}
