$(shell export LD_LIBRARY_PATH=$PWD:LD_LIBRARY_PATH)

all: myshell find_paths tsp_p tsp_t tspsort

tsp_p: tsp_p.c
	gcc -o tsp_p tsp_p.c

tsp_t: tsp_t.c
	gcc -o tsp_t tsp_t.c	
	
tspsort: tspsort.c
	gcc -o tspsort tspsort.c

myshell: myshell.c
	gcc -g -o myshell myshell.c -lreadline

find_paths2: find_paths.c
	gcc -o find_paths find_paths.c

clean:
	-rm -f *.a *.o *~ *.so myshell find_paths tsp_p tsp_t tspsort
