Ben Blau (bblau94@bu.edu)
1/31/2014
CS 210 with Matta
Homework 1
(Sort.c and Search.c)

These two files both work with the Bubble Sort algorithm which is one of the slowest sorting algorithms. This sort.c file does just the bubble sort and search.c utilizes bubble sort and then
allows you to use binary search to find a specific int within an array. In order to use the file properly you must create an array manually from within the file. The file does not allow you
to create an array on your own. Once you have an array (which the file has by default) created you can start to use binary search. Run the search.c file and it will ask you to input an number
that you are looking for. Once you do that binary search will look through the (already sorted) array to find the number you asked it to, it will tell you that the number was either not found
or found at a specific location.

The bubble sort algorithm works by comparing two numbers, moving the larger one to the right, and then moving through the array repeating the process until the largest number reaches the end of the array.
Then it starts over from the beginning of the array, moving the largest numbers to the very end in reverse order until the array is sorted.
