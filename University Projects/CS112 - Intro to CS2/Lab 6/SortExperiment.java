

/* File: SortExperiment.java
 * Authors: Brian Borucki and Wayne Snyder
 * Date: 9/10/13
 * Purpose: This is the starter code for Lab 06; you will take this code and add
 *          functionality to print out the number of calls to less() while sorting
 *          worst-case and average-case arrays. 
 */

import java.util.Random;

public class SortExperiment {
  public static int numComparisons;
  /**************
    * Merge Sort *
    **************/
  public static void mergeSort(int[] a) {
    int[] aux = new int[a.length];
    mergeSort(a, aux, 0, a.length-1);
  }
  
  private static void mergeSort(int[] a, int[] aux, int lo, int hi) {
    if (hi <= lo) return;
    int mid = lo + (hi - lo) / 2;
    mergeSort(a, aux, lo, mid);
    mergeSort(a, aux, mid + 1, hi);
    merge(a, aux, lo, mid, hi);
  }
  
  private static void merge(int[] a, int[] aux, int lo, int mid, int hi) {
    for (int k = lo; k <= hi; k++) {
      aux[k] = a[k]; 
    }
    
    int i = lo, j = mid+1;
    for (int k = lo; k <= hi; k++) {
      if      (i > mid)              a[k] = aux[j++];
      else if (j > hi)               a[k] = aux[i++];
      else if (less(aux[j], aux[i])) a[k] = aux[j++];
      else                           a[k] = aux[i++];
    }
  }
  
  /**************
    * Quick Sort *
    **************/
  public static void quickSort(int[] a) {
    quickSort(a, 0, a.length - 1);
    
  }
  
  private static void quickSort(int[] a, int lo, int hi) { 
    if (hi <= lo) return;
    int j = partition(a, lo, hi);
    quickSort(a, lo, j-1);
    quickSort(a, j+1, hi);
  }
  
  private static int partition(int[] a, int lo, int hi) {
    int i = lo;
    int j = hi + 1;
    int v = a[lo];
    while (true) { 
      
      while (less(a[++i], v))
        if (i == hi) break;
      
      while (less(v, a[--j]))
        if (j == lo) break; 
      
      if (i >= j) break;
      
      exch(a, i, j);
    }
    
    exch(a, lo, j);
    
    return j;
  }
  
  /*****************
    * SelectionSort *
    *****************/
  private static void selectionSort(int[] a) {
    int N = a.length;
    for (int i = 0; i < N; i++) {
      int min = i;
      for (int j = i+1; j < N; j++) {
        if (less(a[j], a[min])) min = j;
      }
      exch(a, i, min);
    }
    
  }
  
  /*****************
    * InsertionSort *
    *****************/
  public static void insertionSort(int[] a) {
    int N = a.length;
    for (int i = 0; i < N; i++) {
      for (int j = i; j > 0 && less(a[j], a[j-1]); j--) {
        exch(a, j, j-1);
      }
    }
  }
  
  /******************
    * Helper Methods *
    ******************/
  private static boolean less(int v, int w) {
    numComparisons++;
    return (v - w < 0);
  }
  
  private static void exch(int[] a, int i, int j) {
    int swap = a[i];
    a[i] = a[j];
    a[j] = swap;
  }
  
  /***************************
    * Our methods for the lab *
    ***************************/
  
  private static Random rnd = new Random();
  
  public static int[] genRandomArray(int size){
    
    int a[] = new int[size];
    for(int i = 0; i < a.length; i++){
      a[i] = rnd.nextInt();
    }
    return a;
  }
  
  public static int[] genReverseSortedArray(int size){
    int a[] = new int[size];
    for(int i = 0; i < a.length; i++){
      a[i] = a.length-i;
    }
    return a;
  }
  
  public static int[] genSortedArray(int size){
    int a[] = new int[size];
    for(int i = 0; i < a.length; i++){
      a[i] = i;
    }
    return a;
  }
  
  // Create a worst-case array for merge sort by reversing a sorted list, doing opposite of merge sort
  
  private static int [] unMerged( int SIZE) {
    int [] A = new int[SIZE]; 
    for(int i = 0; i < SIZE; ++i)           // create sorted list
      A[i] = i; 
    int [] aux = new int[A.length];
    unMergeSort(A,aux,0,A.length-1);
    return A; 
  }
  
  private static void unMergeSort(int A [], int [] aux, int lo, int hi) {
    
    if(hi <= lo)          // base case, size is <= 2
      return;
    
    int mid = lo + (hi - lo)/2;    // m is rightmost element of left side
    
    distribute(A,aux, lo, mid, hi);
    
    unMergeSort(A,aux,lo,mid);
    unMergeSort(A,aux,mid+1,hi); 
  }
  
  private static void distribute(int A[], int aux[], int lo, int mid, int hi) {
    
    for(int i = lo; i <= hi; ++i)     // copy A to auxiliary array
      aux[i] = A[i]; 
    
    for(int i = lo, j = lo; i <= mid; i++, j += 2)       // fill  A[lo...m] with aux[lo], aux[lo + 2], etc.
      A[i] = aux[j];
    
    for(int i = mid+1, j = lo+1; i <= hi; i++, j += 2)      // fill A[m+1...hi] with aux[lo+1], aux[lo + 3], etc.
      A[i] = aux[j];
    
  } 
  
  // generate best case for quick sort
  
  private static int[] bestQuick(int n ) {
    int [] A = new int[n]; 
    for(int i = 0; i < n; ++i)       // generate sorted list
      A[i] = i; 
    bestQuickHelper(A, 0, n-1);        // scramble it
    return A;    
  }
  
  // removes median from list and moves it all the way to the left
  private static void bestQuickHelper(int[] A, int lo, int hi) {
    if(hi - lo < 3) return; 
    int m = (lo + hi)/2;
    int v = A[m];
    for(int i = m; i > lo; --i)
      A[i] = A[i-1];
    A[lo] = v; 
    bestQuickHelper(A, lo+1, m);
    bestQuickHelper(A, m+1, hi);    
  }
  
  
  public static void printArray(int[] a){
    System.out.print("[ ");
    for(int i = 0; i < a.length; i ++){
      if(i == 0)
        System.out.print(a[0]);
      else
        System.out.print(" , " + a[i]);
    }
    System.out.println(" ]");
  }
  //***************DIVIDER********************************************************************
  public static void main(String[] args) {
    int[] bCSSresults = new int[40];
    int[] bCISresults = new int[40];
    int[] bCMSresults = new int[40];
    int[] bCQSresults = new int[40];
    int[] aCISresults = new int[40];
    int[] aCMSresults = new int[40];
    int[] aCQSresults = new int[40];
    int[] wCISresults = new int[40];
    int[] wCMSresults = new int[40];
    int[] wCQSresults = new int[40];
    //Best Case example:
    System.out.println("Best Case:");
    System.out.println();
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genSortedArray(i);
      // record results here
      insertionSort(a);
      bCISresults[i/5] = i;
      bCISresults[(i/5) + 1] = numComparisons;
      System.out.println("Best Case insertion sort results array: ");
      printArray(bCISresults);
      //System.out.println("Best Case: number of comparisons for insertion sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genSortedArray(i);
      // record results here
      mergeSort(a);
      bCMSresults[i/5] = i;
      bCMSresults[(i/5) + 1] = numComparisons;
      System.out.println("Best Case merge sort results array: ");
      printArray(bCMSresults);
      //System.out.println("Best Case: number of comparisons for merge sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    
    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genSortedArray(i);
      // record results here
      quickSort(a);
      bCQSresults[i/5] = i;
      bCQSresults[(i/5) + 1] = numComparisons;
      System.out.println("Best Case quick sort results array: ");
      printArray(bCQSresults);
      //System.out.println("Best Case: number of comparisons for quick sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }       
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genSortedArray(i);
      // record results here
      selectionSort(a);
      bCSSresults[i/5] = i;
      bCSSresults[(i/5) + 1] = numComparisons;
      System.out.println("Best Case selection sort results array: ");
      printArray(bCSSresults);      
      //System.out.println("Best Case: number of comparisons for selection sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    System.out.println();
    //Average Case example:
    System.out.println("Average Case:");
    System.out.println();
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genRandomArray(i);
      // record results here
      insertionSort(a);
      aCISresults[i/5] = i;
      aCISresults[(i/5) + 1] = numComparisons;
      System.out.println("Average Case insertion sort results array: ");
      printArray(aCISresults);
      //System.out.println("Average Case: number of comparisons for insertion sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genRandomArray(i);
      // record results here
      mergeSort(a);
      aCMSresults[i/5] = i;
      aCMSresults[(i/5) + 1] = numComparisons;
      System.out.println("Average Case merge sort results array: ");
      printArray(aCMSresults);
      //System.out.println("Average Case: number of comparisons for merge sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genRandomArray(i);
      // record results here
      quickSort(a);
      aCQSresults[i/5] = i;
      aCQSresults[(i/5) + 1] = numComparisons;
      System.out.println("Average Case quick sort results array: ");
      printArray(aCQSresults);
      //System.out.println("Average Case: number of comparisons for quick sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }       
    
    System.out.println();
    //Worst Case
    System.out.println("Worst Case:");
    System.out.println();
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genReverseSortedArray(i);
      // record results here
      insertionSort(a);
      wCISresults[i/5] = i;
      wCISresults[(i/5) + 1] = numComparisons;
      System.out.println("Worst Case insertion sort results array: ");
      printArray(wCISresults);
      //System.out.println("Worst Case: number of comparisons for insertion sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genReverseSortedArray(i);
      // record results here
      mergeSort(a);
      wCMSresults[i/5] = i;
      wCMSresults[(i/5) + 1] = numComparisons;
      System.out.println("Worst Case merge sort results array: ");
      printArray(wCMSresults);
      //System.out.println("Worst Case: number of comparisons for merge sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }    
    
    for(int i = 5; i <= 100 ; i+=5){
      int[] a = genReverseSortedArray(i);
      // record results here
      quickSort(a);
      wCQSresults[i/5] = i;
      wCQSresults[(i/5) + 1] = numComparisons;
      System.out.println("Worst Case quick sort results array: ");
      printArray(wCQSresults);
      //System.out.println("Worst Case: number of comparisons for quick sort array size of [" + i + "]: " + numComparisons);
      numComparisons = 0;
      }   
    
   // printArray(bestQuick(30)); 
    
    }
}