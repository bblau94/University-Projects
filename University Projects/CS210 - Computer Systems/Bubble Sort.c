// Ben Blau (bblau94@bu.edu)
// 1/30/2014
// Bubble Sort Program - Homework 1
// CS 210 with Matta
// Boston University
 
#include <stdio.h> 
 
int Array[12] = {20, 13, 6, -1, 15, 29, 4, 2, 18, 10, -4, 15}; 
int Array1[5] = {5, 0, 7, 21, -17}; 
 
void PrintArray(int Arr[], int n) { 
 int i; 
 for (i=0; i < n; i++) { 
 printf("%d ", Arr[i]); 
 } 
} 
 
void Swap(int *x, int *y) { 
 
 int temp; 
 temp = *x;
 *x = *y;
 *y = temp;
 
} 
   
 void BubbleSort(int Arr[], int n) { 
    int i, j; 
   
    for (i = n-2; i >= 0; i--) { 
     for (j = 0; j <= i; j++) { 
      if (Arr[j] > Arr[j+1]) { 
        Swap(&Arr[j], &Arr[j+1]); 
      } 
     } 
    }
 } 
             
              
int main() { 
  BubbleSort(Array, 12); 
  printf("The sorted array is: "); 
  PrintArray(Array, 12); 
  printf("\n"); 
  printf("A second sorted array to test Bubble Sort: ");
  BubbleSort(Array1, 5);
  PrintArray(Array1, 5);
  printf("\n");


} 
 
