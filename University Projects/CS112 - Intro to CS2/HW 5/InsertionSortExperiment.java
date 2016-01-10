/* File: InsertionSortExperiment.java
 * Authors: Brian Borucki and Wayne Snyder
 * Date: 9/10/13
 * Purpose: This is the starter code for Lab 05; you will take this code and add
 *          functionality to print out the number of calls to less() while sorting
 *          worst-case and average-case arrays. 
 */

import java.util.Random; 

public class InsertionSortExperiment {
public static int counter = 0;   
   private static Random R = new Random();                // Global random object, has method 
                                                          // R.nextInt() to return random integers
   
   // insertion sort, adapted from Sedgewick and Wayne, Algorithms
   private static void sort(int [] a) { 
      int N = a.length; 
      for (int i = 1; i < N; i++) { 
         for (int j = i; j > 0 && less(a[j], a[j-1]); j--) { 
            exch(a, j, j-1); 
            counter++;
         } 
      } 
   }  
   
   
   // is v < w ?
   private static boolean less(int  v, int  w) {
      return (v < w);
   }      
   
   // exchange a[i] and a[j]
   private static void exch(int[] a, int i, int j) {
      int swap = a[i];
      a[i] = a[j];
      a[j] = swap;
   }
   
   private static int[] genReverseArray(int size){
     int[] A = new int[size];
     for (int i = 0; i < A.length; i++) {
       A[i] = (size - i);
     }
      // create an array of integers in reverse order, i.e., A[i] = (size - i)
      return A;                    // return your reverse array instead of null
   }
   
    private static int[] genRandomArray(int size){
      //use your GLOBAL random object to create an
      //array of random integers
      int[] r = new int[size];
      
      for (int i = 0; i < r.length; i++) {
        int n = R.nextInt();
        r[i] = n;
      }
      return r;                    // return your random array instead of null
   }
     
    public static void printArray(int[] A) {
      for (int i = 0; i < A.length; i++) {
        System.out.print(A[i] + " ");
      }
      System.out.println();
    }
   public static void main(String[] args) {
      System.out.println("Experiment One");
      //first, find a way of modifying the sort() method to return the number of comparisons made
      for (int i = 5; i <= 100; i+= 5) {
        int[] A = genReverseArray(i);
        sort(A);
        System.out.println("Number of sorts for reverse array of size " + i + ": " + counter);
        counter = 0;
      }
     System.out.println();
      
      //First experiment
      //create a reverse array of size 5, sort it, and print out the number of comparisons
      //should be of the format "size     numComparisons" (ex. "5     3")
      //where the space is a tab
      
      //now do this for an array of size 10, 15, 20, up to 100
      //you will then use your output to plot a graph in Excel
      
      //Second experiment: do the same thing, but use the random arrays!
      
      
      System.out.println("Experiment Two");
      //first, find a way of modifying the sort() method to return the number of comparisons made
      for (int i = 5; i <= 100; i+= 5) {
        int[] A = genRandomArray(i);
        sort(A);
        System.out.println("Number of sorts for reverse array of size " + i + ": " + counter);
        counter = 0;
      }
   }
}