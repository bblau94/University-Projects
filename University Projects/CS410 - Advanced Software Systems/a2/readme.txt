README for cs410 assignment2
	-Jeffrey Zurita	(u90084243)
	-Ben Blau (u94434268)
	-Tyler Butler (u42006468)

Program Limitations:
	Shell:
	1) Cannot use ctrl-c command to exit forground processes
	2) pipes will not work in conjuction with input/output (</>)
	
		-./tsp_p < input_graphs | ./tspsort > a.out 
		will not work but the individual parts will

		i.e ./tsp_p < input_graphs 
		    ls | more
		    ./helloworld > a.out
			

Assumptions:
1) input graphs is a file holding the name of the matrix file which is
read in by tsp_p and tsp_t

Program Compilation:
1) Open the parent directory and run the makefule:
	make

Program Use:
1) Call upon the functions in this manner for both :
	
	./tsp_p < input_graphs | ./tspsort > a.out

2) First example for using processes and second for threads
3) Return in the form:

smallest	
   |	   dist  path
   |	   dist  path
   |	   dist  path
   |	   .
   |	   .
   |	   .
largest	   dist  path
	
Notes:
-find_paths does the actual tsp algorithmn
-is passed the number of cities, the starting city, and the matrix file name
-tries every combination of paths that hits every city once, starting and ending with the starting city
	-if a value in the path is (-1), it is discarded
-returns every working path
-tsp_t and tsp_p will both run and output the path and path length for any NxN array up to 9x9
	-however, the tspsort takes very long to (bubble) sort the distances with their corresponding paths.
-There is a variable bpc: If you want the best path at each starting city to print out
	-for each process/thread, uncomment the print statement at the location below bpc in find_paths.
	-"ctrl-f" and type "bpc" to find the location more easily.