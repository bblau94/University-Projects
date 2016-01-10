//Ben Blau (bblau94@bu.edu)
//1/30/2014
//Binary Search Program for Homework 1 - Expanding on Bubble Sort
//CS 210 with Matta
//Boston University


#include <stdio.h>

int Array[12] = {20, 13, 6, -1, 15, 29, 4, 2, 18, 10, -4, 15};

void PrintArray(int Arr[], int n) {
 int i;
 for (i=0; i < n; i++) {
 printf("%d ", Arr[i]);
 }
}

void BinarySearch(int Arr[], int size, int key) {
//size represents the size of the array, key represents the value being searched for
  int first, middle, last;
  first = 0;
  last = size - 1;
  middle = (first + last)/2;

  while(first <= last)
  {
    if (Arr[middle] < key)
      first = middle + 1;
    else if (Arr[middle] == key)
      {
        printf("Key = %d found in position %d\n", key, middle);
        break;
      }
    else
      last = middle - 1;
      middle = (first + last)/2;
  }

  if (first > last)
    printf("Key = %d Not Found\n", key);
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
  int key;
  BubbleSort(Array, 12);
  printf("The sorted array is: ");
  PrintArray(Array, 12);
  printf("\n");
  printf("Enter the value you are looking for:  ");
  scanf("%d", &key);
  printf("\n");
  BinarySearch(Array, 12, key);

}


