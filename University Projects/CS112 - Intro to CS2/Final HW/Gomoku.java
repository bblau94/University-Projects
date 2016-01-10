/* Title:  Gomoku.java
 * Author: Ben Blau (bblau94@gmail.com)
 * Date: 12/8/13
 * Class: CS 112, Fall 2013
 * Purpose: This code is the extended version of TicTacToe by Wayne Synder. This is Gomoku.
 * Starter code for the final project assignment provided by Wayne Snyder. The final edit is by Ben Blau
 * and Tyler Butler.
 * ***NOTE***!! - The code from here contains 100% of Wayne Snyders TicTacToe.java with the exceptions of
 *                any code that may have been deleted in the process of modifying the code to fit the
 *                homework criteria.
 */ 

import java.util.*;

public class Gomoku {
  
  private static int[][] B = new int[5][5];
  
  // pieces are encoded as 10 and 1, so that summing across rows or columns will
  //    give a simple method for finding how many pieces occur: the 10's place
  //    gives how many X's, and the 1's place gives how many O's: e.g., XBO = 10+0+1 = 11. 
  //    11 / 10 = 1 X, and 11 % 10 = 1 O. 
  
  private final static int X = 10;    
  private final static int O = 1; 
  private final static int Blank = 0; 
  
  // just to conveniently print out names of pieces: Piece[X] = "X" etc.
  
  private static String[] Piece =  {" ", "O", "", "", "", "", "", "", "", "", "X" }; 
  
  private static final int maxDepth = 5;         // maximum search depth
  
  // moves are represented by integers 0 .. 24, e.g.
  //     0  1  2  3  4
  //     5  6  7  8  9
  //     10 11 12 13 14
  //     15 16 17 18 19
  //     20 21 22 23 24
  // so can recover row and column using / and %:
  
  private static  int column(int move) {
    return move % 5;
  }
  
  private static  int row(int move) {
    return move / 5;
  }
  
  // return true if 4 X's occur in any row, column, or diagonal; this is same as
  // checking if sum = 40:
  
  private static boolean winForX(int[][] B) {
    return (
            ((B[0][0]+B[0][1]+B[0][2]+B[0][3]) == 40) ||     //Horizontal win possibilities
            ((B[0][1]+B[0][2]+B[0][3]+B[0][4]) == 40) ||
            ((B[1][0]+B[1][1]+B[1][2]+B[1][3]) == 40) ||
            ((B[1][1]+B[1][2]+B[1][3]+B[1][4]) == 40) ||
            ((B[2][0]+B[2][1]+B[2][2]+B[2][3]) == 40) ||    
            ((B[2][1]+B[2][2]+B[2][3]+B[2][4]) == 40) ||
            ((B[3][0]+B[3][1]+B[3][2]+B[3][3]) == 40) ||
            ((B[3][1]+B[3][2]+B[3][3]+B[3][4]) == 40) ||
            ((B[4][0]+B[4][1]+B[4][2]+B[4][3]) == 40) ||
            ((B[4][1]+B[4][2]+B[4][3]+B[4][4]) == 40) ||
            
            ((B[0][0]+B[1][0]+B[2][0]+B[3][0]) == 40) ||      //Vertical win possibilities
            ((B[1][0]+B[2][0]+B[3][0]+B[4][0]) == 40) ||
            ((B[0][1]+B[1][1]+B[2][1]+B[3][1]) == 40) ||
            ((B[1][1]+B[2][1]+B[3][1]+B[4][1]) == 40) ||
            ((B[0][2]+B[1][2]+B[2][2]+B[3][2]) == 40) ||
            ((B[1][2]+B[2][2]+B[3][2]+B[4][2]) == 40) ||
            ((B[0][3]+B[1][3]+B[2][3]+B[3][3]) == 40) ||
            ((B[1][3]+B[2][3]+B[3][3]+B[4][3]) == 40) ||
            ((B[0][4]+B[1][4]+B[2][4]+B[3][4]) == 40) ||
            ((B[1][4]+B[2][4]+B[3][4]+B[4][4]) == 40) ||
            
            ((B[0][0]+B[1][1]+B[2][2]+B[3][3]) == 40) ||     //Diagonal win possibilities
            ((B[1][1]+B[2][2]+B[3][3]+B[4][4]) == 40) ||
            ((B[4][0]+B[3][1]+B[2][2]+B[1][3]) == 40) ||
            ((B[0][4]+B[1][3]+B[2][2]+B[3][1]) == 40) ||
            ((B[3][0]+B[2][1]+B[1][2]+B[0][3]) == 40) ||
            ((B[4][1]+B[3][2]+B[2][3]+B[1][4]) == 40) ||
            ((B[1][0]+B[2][1]+B[3][2]+B[4][3]) == 40) ||
            ((B[0][1]+B[1][2]+B[2][3]+B[3][4]) == 40) 
              
           );
  }
  
  // similarly for O:
  
  private static boolean winForO(int[][] B) {
    return (
            ((B[0][0]+B[0][1]+B[0][2]+B[0][3]) == 4) ||     //Horizontal win possibilities
            ((B[0][1]+B[0][2]+B[0][3]+B[0][4]) == 4) ||
            ((B[1][0]+B[1][1]+B[1][2]+B[1][3]) == 4) ||
            ((B[1][1]+B[1][2]+B[1][3]+B[1][4]) == 4) ||
            ((B[2][0]+B[2][1]+B[2][2]+B[2][3]) == 4) ||    
            ((B[2][1]+B[2][2]+B[2][3]+B[2][4]) == 4) ||
            ((B[3][0]+B[3][1]+B[3][2]+B[3][3]) == 4) ||
            ((B[3][1]+B[3][2]+B[3][3]+B[3][4]) == 4) ||
            ((B[4][0]+B[4][1]+B[4][2]+B[4][3]) == 4) ||
            ((B[4][1]+B[4][2]+B[4][3]+B[4][4]) == 4) ||
                        
            ((B[0][0]+B[1][0]+B[2][0]+B[3][0]) == 4) ||      //Vertical win possibilities
            ((B[1][0]+B[2][0]+B[3][0]+B[4][0]) == 4) ||
            ((B[0][1]+B[1][1]+B[2][1]+B[3][1]) == 4) ||
            ((B[1][1]+B[2][1]+B[3][1]+B[4][1]) == 4) ||
            ((B[0][2]+B[1][2]+B[2][2]+B[3][2]) == 4) ||
            ((B[1][2]+B[2][2]+B[3][2]+B[4][2]) == 4) ||
            ((B[0][3]+B[1][3]+B[2][3]+B[3][3]) == 4) ||
            ((B[1][3]+B[2][3]+B[3][3]+B[4][3]) == 4) ||
            ((B[0][4]+B[1][4]+B[2][4]+B[3][4]) == 4) ||
            ((B[1][4]+B[2][4]+B[3][4]+B[4][4]) == 4) ||
            
            ((B[0][0]+B[1][1]+B[2][2]+B[3][3]) == 4) ||     //Diagonal win possibilities
            ((B[1][1]+B[2][2]+B[3][3]+B[4][4]) == 4) ||
            ((B[4][0]+B[3][1]+B[2][2]+B[1][3]) == 4) ||
            ((B[0][4]+B[1][3]+B[2][2]+B[3][1]) == 4) ||
            ((B[3][0]+B[2][1]+B[1][2]+B[0][3]) == 4) ||
            ((B[4][1]+B[3][2]+B[2][3]+B[1][4]) == 4) ||
            ((B[1][0]+B[2][1]+B[3][2]+B[4][3]) == 4) ||
            ((B[0][1]+B[1][2]+B[2][3]+B[3][4]) == 4) 
              
           );
    
  }
  
  // return true if no blank slots or if is a win for X or O
  
  private static  boolean isLeaf(int[][] B) {
    if(winForX(B) || winForO(B))
      return true;
    
    for(int row = 0; row < 5; ++row) {        // check if any slot != 0
      for(int col = 0; col < 5; ++col) {
        if(B[row][col] == Blank) 
          return false;                    // if found, return false
      }
    }
    return true;                              // didn't find one, return true
  }
  
  // Evaluation function: count the number of available rows, columns, or 
  // diagonals that X or O could complete for a win, by counting pieces in each.
  // But first check if is a win for either player, and make a win at a closer level
  // worth more than a win further down, by using 1000-depth (so win one level down
  // is worth 999 and win at 3 levels down is worth 997.  Any win will be worth more
  // than a non-win, but comparing wins at different levels will prefer the closer win.
  
  private static  int eval(int[][] B, int depth) {
    
    if(winForX(B))
      return 1000-depth;               // win at smaller depth is preferred
    else if(winForO(B))
      return -(1000-depth);
    
    int sum = 0;
    
    // count rows
    for(int r = 0; r < 5; ++r) 
      sum += countPieces(B[r][0],B[r][1],B[r][2],B[r][3],B[r][4]);
    
    // count columns
    for(int c = 0; c < 5; ++c) 
      sum += countPieces(B[0][c],B[1][c],B[2][c],B[3][c],B[4][c]);
    
    // count diagonals
    sum += countPieces(B[0][0],B[1][1],B[2][2],B[3][3],B[4][4]);
    
    sum += countPieces(B[4][0],B[3][1],B[2][2],B[1][3],B[0][4]);
    
    return sum;
    
  }
  
  
  // Given three board values (where X = 10, O = 1, blank  = 0), 
  // counts number of X's if only X's occur, result is positive;
  // counts number of O's if only O's occur, result is negative. 
  // Sum of these two is returned.
  
  private static int countPieces(int a, int b, int c, int d, int e) {
    int n = a + b + c + d + e;
    int numX = n / 10;
    int numO = n % 10;
    if(numX > 0 && numO > 0)
      return 0;        // no move for either in this row, return 0
    else if(numO == 0)  // only X's in this sequence
      return numX;
    else if(numX == 0)  // only O's in this sequence
      return -numO; 
    return 0;           // needed for compilation
  }
  
  // top level minMax method, returns move instead of value of node
  
  private static int chooseMove(int[][] B) { 
    int max = -1000;     
    int bestMove = -1;  
    for(int move = 0; move < 25; ++move) { 
      
      if(B[row(move)][column(move)] == Blank) {   // move is available
        
        B[row(move)][column(move)] = X;       // make the move 
        
        int val = minMax( B, 1 ); 
        if(val > max) {                       // if better move, remember it
          bestMove = move; 
          max = val; 
        } 
        B[row(move)][column(move)] = Blank;        // undo the move
        
      }  
    }  
    return bestMove; 
  }   
  
  
  
  // recursive minMax called by top level chooseMove; returns value of current board
  
  private static int minMax(int[][] B, int depth) { 
    if( isLeaf(B) || depth == maxDepth)  
      return eval(B, depth);  
    else if( depth % 2 == 0 ) {       // even levels are max, X player           
      int max = -1000; 
      for(int move = 0; move < 25; ++move) {
        if(B[row(move)][column(move)] == 0) {    // move is available
          
          B[row(move)][column(move)] = X;       // make the move  
          
          int val = minMax( B, depth + 1 );  
          if(val > max) { 
            max = val;                         // if this is best, update
          } 
          B[row(move)][column(move)] = Blank;       // undo the move and try next move 
        }
      }
      return max; 
    } else {                          // is a min node, O player
      int min = 1000; 
      for(int move = 0; move < 25; ++move) {
        if(B[row(move)][column(move)] == 0) {    // move is available
          
          B[row(move)][column(move)] = O;       // make the move  
          
          int val = minMax( B, depth + 1 ); 
          if(val < min) { 
            min = val;                         // if this is best, update
          }
          B[row(move)][column(move)] = Blank;   // undo the move and try next move    
        }
      }
      return min; 
    }
  }
  
  
  private static void printBoard(int [][] B) {
    
    System.out.println("\t---------------------");
    System.out.println("\t| " + Piece[B[0][0]] + " | " + Piece[B[0][1]] + " | " + Piece[B[0][2]] + " | " + Piece[B[0][3]] + " | " + Piece[B[0][4]] + " |"); 
    System.out.println("\t---------------------");
    System.out.println("\t| " + Piece[B[1][0]] + " | " + Piece[B[1][1]] + " | " + Piece[B[1][2]] + " | " + Piece[B[1][3]] + " | " + Piece[B[1][4]] + " |"); 
    System.out.println("\t---------------------");
    System.out.println("\t| " + Piece[B[2][0]] + " | " + Piece[B[2][1]] + " | " + Piece[B[2][2]] + " | " + Piece[B[2][3]] + " | " + Piece[B[2][4]] + " |"); 
    System.out.println("\t---------------------"); 
    System.out.println("\t| " + Piece[B[3][0]] + " | " + Piece[B[3][1]] + " | " + Piece[B[3][2]] + " | " + Piece[B[3][3]] + " | " + Piece[B[3][4]] + " |"); 
    System.out.println("\t---------------------"); 
    System.out.println("\t| " + Piece[B[4][0]] + " | " + Piece[B[4][1]] + " | " + Piece[B[4][2]] + " | " + Piece[B[4][3]] + " | " + Piece[B[4][4]] + " |"); 
    System.out.println("\t---------------------"); 
  }
  
  /* List of ways to win with 4 in a row on a 5x5 board
   *      0  1  2  3  4   A[y][x]
   *                 ex.  A[2][3] = 13
   * 0    0  1  2  3  4
   * 1    5  6  7  8  9 
   * 2    10 11 12 13 14
   * 3    15 16 17 18 19
   * 4    20 21 22 23 24
   * 
   * Left-to-Right Win Possibilities - 10  ||  Up-Down Win Possibilities - 10
   * 00 01 02 03                           ||  00 10 20 30
   * 01 02 03 04                           ||  10 20 30 40
   * 10 11 12 13                           ||  01 11 21 31
   * 11 12 13 14                           ||  11 21 31 41
   * 20 21 22 23                           ||  02 12 22 32
   * 21 22 23 24                           ||  12 22 32 43
   * 30 31 32 33                           ||  03 13 23 33
   * 31 32 33 34                           ||  13 23 33 43
   * 40 41 42 43                           ||  04 14 24 34
   * 41 42 43 44                           ||  14 24 34 44
   * 
   * Diagonal Win Possibilities - 8
   * 00 11 22 33
   * 11 22 33 44
   * 40 31 22 13
   * 04 13 22 31
   * 30 21 12 03
   * 41 32 23 14
   * 10 21 32 43
   * 01 12 23 34
   */
  
  public static void main(String [] args) {
    
    System.out.println("Tic-Tac-Toe Game: You are playing O, and the computer");
    System.out.println("\twill play X; type in a move using digits 0 .. 24:");
    System.out.println("\t\t---------------------");
    System.out.println("\t\t| 0 | 1 | 2 | 3 | 4 |"); 
    System.out.println("\t\t---------------------");
    System.out.println("\t\t| 5 | 6 | 7 | 8 | 9 |");  
    System.out.println("\t\t---------------------");
    System.out.println("\t\t|10 |11 |12 |13 |14 |");  
    System.out.println("\t\t---------------------"); 
    System.out.println("\t\t|15 |16 |17 |18 |19 |");  
    System.out.println("\t\t---------------------");
    System.out.println("\t\t|20 |21 |22 |23 |24 |");  
    System.out.println("\t\t---------------------"); 
    System.out.println("\tTo end the game early, type Control-D."); 
    
    System.out.println("Would you like to move first or second? Type in 1 or 2: ");
    
    Scanner sc = new Scanner(System.in); 
    int selection = 0;
    selection = sc.nextInt();
    
    if (selection == 1) {
      System.out.println("What is your move?"); 
      
      while(sc.hasNextInt()) { 
        
        // O's move
        int moveO = sc.nextInt(); 
        
        if(B[row(moveO)][column(moveO)] == Blank) {    // if this is possible move
          
          B[row(moveO)][column(moveO)] = O;           // make the move
          
          System.out.println("O's Move:");
          printBoard(B);
          
          if(winForO(B)) {                            // if O wins, stop!
            System.out.println("Win for O!");
            break;
          }
          if(isLeaf(B)) {                             // O is last to move, so check if tie
            System.out.println("Tie Game!"); 
            break; 
          }
          
          int moveX  = chooseMove(B);                     // machine chooses a move
          
          B[row(moveX)][column(moveX)] = X;           // make the move
          
          System.out.println("\nX's Move:");
          printBoard(B);
          
          if(winForX(B)) {                            // if X wins, stop!
            System.out.println("Win for X!");
            break;
          }
          
          if(isLeaf(B)) {                             // X is last to move, so check if tie
            System.out.println("Tie Game!"); 
            break; 
          }
        }
        else {
          System.out.println("Illegal move, try again...."); 
        }
        System.out.println("What is your move?"); 
      }
    }else if (selection == 2) {      
      int moveX  = chooseMove(B);  // machine chooses first move
      B[row(moveX)][column(moveX)] = X;
      System.out.println("\nX's Move:");
      printBoard(B); 
      
      while(sc.hasNextInt()) { 
        
        // O's move
        int moveO = sc.nextInt(); 
        
        if(B[row(moveO)][column(moveO)] == Blank) {    // if this is possible move
          
          B[row(moveO)][column(moveO)] = O;           // make the move
          
          System.out.println("O's Move:");
          printBoard(B);
          
          if(winForO(B)) {                            // if O wins, stop!
            System.out.println("Win for O!");
            break;
          }
          
          moveX  = chooseMove(B);                     // machine chooses a move
          
          B[row(moveX)][column(moveX)] = X;           // make the move
          
          System.out.println("\nX's Move:");
          printBoard(B);
          
          if(winForX(B)) {                            // if X wins, stop!
            System.out.println("Win for X!");
            break;
          }
          
          if(isLeaf(B)) {                             // X is last to move, so check if tie
            System.out.println("Tie Game!"); 
            break; 
          }
        }
        else {
          System.out.println("Illegal move, try again...."); 
        }
        System.out.println("What is your move?"); 
      }
      
    }      
    
    
    
  }
  
}
