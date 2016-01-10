'''
Created by Ben Blau: bblau94@bu.edu
October 14th 2014
Professor Lapets CS320
Homework 3 compile
Filename: compile.py
Collab with Nick Papadopoulos
Collab with Tyler Butler
'''

from random import randint
exec(open("machine.py").read())
exec(open("parse.py").read())
Node = dict
Leaf = str

'''	
memory address -2 to -...: the address of the rest of the stack
memory address -1: the address of the top of the stack
memory address 0: the address of the result of an add operation;
memory address 1: the address of the first input to an add operation;
memory address 2: the address of the second input to an add operation;
memory address 3: the address containing the "from" address for a copy operation;
memory address 4: the address containing the "to" address for a copy operation;
memory address 5: the output buffer (set to −1 after every step);
memory address 6: the address of the program's control index.
memory address 7: the address that points to the to of the stack
memory address 8: the address of the top of the heap
The meaning of each instruction is described below:
label l: there is no effect and control is passed to the next instruction;
goto l: control immediately moves to the program instruction label l;
branch l a: control immediately moves to the program instruction label l if memory address a contain a non-zero integer;
jump a: if the integer i is stored in memory address a, control moves immediately to the ith instruction in the program;
set a n: memory address a is set to the integer n;
copy: if a is the integer stored in memory address 3, and b is the integer stored in memory address 4, then the contents of memory address a are copied to memory address b;
add: the contents of memory location 1 and memory location 2 are added and stored in memory location 0.	
'''	


#env = fresh, t = term parse tree (instructions), heap = heap
def compileTerm(env, t, heap):
	if type(t) == Node:
		for label in t:
			# changing name of env to fresh
			children = t[label]
			if label == 'Plus':
				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				t1 = children[0]
				t2 = children[1]
			
				#print('PLUS HEAP')
				#print(heap)
				
				(insts1, addr1, heap2) = compileTerm(env, t1, heap)
				#heap2 = heap2 + 1
				
				#print('PLUS HEAP2')
				#print(heap2)
				#print()
				#print('INSTS1 IN PLUS')
				#print(insts1)
				#print()
				
				(insts2, addr2, heap3) = compileTerm(env, t2, heap2 + 1)
				heap4 = heap3 + 1
				#print('PLUS HEAP3')
				#print(heap3)
				

				#print('INSTS2 IN PLUS')
				#print(insts2)
				#heap3 = heap3 + 1
				#print()
				#print('PLUS HEAP4')
				#print(heap4)
				#print()
				# Add instructions that compute the result of the
				# Plus operation.
				#put an if statement here for if plus variables?
				instsPlus = \
					copy(heap2, 1)\
					+copy(heap3, 2)\
					+[\
					"add"\
					]\
					+copy(0,heap4)\
					
					
				return (insts1 + insts2 + instsPlus, heap3, heap4)
			
			if label == 'Number':
				t1 = children[0]
				#pull out the number (child) from the tree
				# Find a new memory address on the heap.
				# Generate instruction to store the integer on the heap
				inst = 'set ' + str(heap) + ' ' + str(t1)
				# Return the instruction list and top of the heap.
				return ([inst], heap, heap)
			if label == 'Variable':
				# Return the instruction list and top of the heap.
				# fresh is not changed
				# heap is not changed because we are not setting anything here
				
				
				print('hi')
				print(env)
				
				instsVariable =\
					copy(env[children[0]], heap)\
				
			
				return (instsVariable, heap, heap)
	
	
			
#test = compileTerm({},{'Plus': [{'Number': [5]}, {'Number': [7]}]}, 8)
#test = compileTerm({'x': 10},{'Plus': [{'Variable': ['x']}, {'Variable': ['x']}]}, 8)
#(insts, addr, heap) = test
#print(addr, heap)
#print(simulate(insts))
	#insts = list of machine language (string)
	#addr = address of result
	#heap = integer representing the memory of the top of the heap after the computation is performed
	#return(insts, addr, heap)		
			#fresh
				
def compileFormula(env, f, heap):
	if type(f) == Leaf:
		if f == 'True':
			# Find a new memory address on the heap.
			heap = heap
			# Generate instruction to store the integer representing True on the heap.
			inst = 'set ' + str(heap) + ' 1'
			# Return the instruction list and top of the heap.
			return ([inst], heap, heap)
		if f == 'False':
			# Find a new memory address on the heap.
			heap = heap
			# Generate instruction to store the integer representing False on the heap.
			inst = 'set ' + str(heap) + ' 0'
			# Return the instruction list and top of the heap.
			return ([inst], heap, heap)
			
		return (['**NOT FORMULA**'], fresh, heap) #FOR compileExpression - if compileFormula doesn't work - go back and do term
	if type(f) == Node:
		for label in f:
			children = f[label]
			if label == 'Not':
				fresh = freshStr()
				# Compile the subtree f to obtain the list of
				# instructions that computes the value represented
				# by f.
				f = children[0]
				#print('before HEAP')
				#print(heap)
				(insts, addr, heap) = compileFormula(env, f, heap)
				#print('HEREEEEHEAP')
				heap2 = heap + 1
				#print(heap)
				# Generate more instructions to change the memory
				# location in accordance with the definition of the
				# Not operation.
				instsNot = \
					["branch setZero" + str(fresh) + " " + str(heap),\
					"set " + str(heap2) + " 1",\
					"goto finish" + str(fresh),\
					"label setZero" + str(fresh),\
					"set " + str(heap2) + " 0",\
					"label finish" + str(fresh)\
					]
					
				return (insts + instsNot, heap, heap2)
					
			if label == 'Or':
				fresh1 = freshStr()
				fresh2 = freshStr()
				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				f1 = children[0]
				f2 = children[1]
				(insts1, addr1, heap2) = compileFormula(env, f1, heap)
				#heap2 = heap2 + 1
				(insts2, addr2, heap3) = compileFormula(env, f2, heap2 + 1)
				heap4 = heap3 + 1
				# Increment the heap counter so we store the
				# result of computing Or in a new location.
				# Add instructions that compute the result of the
				# Or operation.
				
				instsOr = \
					copy(heap2, 1)\
					+copy(heap3, 2)\
					+["add",\
					"branch setOne" + str(fresh2) + " 0",\
					"goto finish" + str(fresh2),\
					"label setOne" + str(fresh2),\
					"set 0 1",\
					"label finish" + str(fresh2)\
					]\
					+copy(0, heap4)\
					
				return (insts1 + insts2 + instsOr, heap4, heap4)
					
			if label == 'And':
				fresh1 = freshStr()
				fresh2 = freshStr()
				
				# Compile the two subtrees and get the instructions
				# lists as well as the addresses in which the results
				# of computing the two subtrees would be stored if someone
				# were to run those machine instructions.
				f1 = children[0]
				f2 = children[1]
				#print(heap)
				(insts1, addr1, heap2) = compileFormula(env, f1, heap)
				#print('HEAP 2 IN AND')
				#print(heap2 + 1)
				#heap2 = heap2 + 1
				#print(heap2)
				(insts2, addr2, heap3) = compileFormula(env, f2, heap2 + 1)
				heap4 = heap3 + 1
				#print("IN AND")
				#print(addr1, addr2)
				#print('HEAP3')
				#print(heap3)

				# Increment the heap counter so we store the
				# result of computing Or in a new location.
				# Add instructions that compute the result of the
				# And operation.
				
				instsAnd = \
					copy(heap2, 1)\
					+["branch next" + str(fresh2) + " 1",\
					"set 0 0",\
					"goto finish" + str(fresh2),\
					"label next" + str(fresh2)\
					]\
					+copy(heap3, 2)\
					+["branch setOne" + str(fresh2) + " 2",\
					"set 0 0",\
					"goto finish" + str(fresh2),\
					"label setOne" + str(fresh2),\
					"set 0 1",\
					"label finish" + str(fresh2)\
					]\
					+copy(0, heap4)\
					
				return (insts1 + insts2 + instsAnd, heap4, heap4)

			if label == 'Variable':
				# Return the instruction list and top of the heap.
				# heap is not changed because we are not setting anything here
				instsVariable =\
					copy(env[children[0]], heap)\
				
				return (instsVariable, heap, heap)
			return (['**NOT FORMULA**'], heap, heap) #FOR compileExpression - if compileFormula doesn't work - go back and do term		
				
#test = compileFormula({}, {'Or': ['False', 'True']},8)
#test = compileFormula({}, {'Not': ['False']},8)
#(insts, addr, heap) = test
#print(addr, heap)
#print(simulate(insts))


def freshStr():
	return str(randint(0,100000))

def compileProgram(env, s, heap):
	if type(s) == Node:		
		for label in s:
			children = s[label]
		
			if label == 'Assign':
				s1 = children[0]['Variable'][0]
				s2 = children[1]
				s3 = children[2]
				
				#print('CURRENT s2 and s3')
				#print(s2)
				#print(s3)
				#print()
				#print('ENVIRON ASSIGN BEFORE CHANGE')
				#print(env)
				#print()
				#print("children")
				#print(s2)
				(insts1, addr1, heap2) = compileExpression(env, s2, heap)
				#heap2 = heap2 + 1
				#print('heap (position of value variable s1)')
				#print(heap)
				#print(heap2)
				#print()
				#print('what is being put in env - s1 - addr1')
				#print(s1)
				#print(addr1)
				#print()
				env[s1] = addr1
				#print('FINAL ENV')
				#print(env)
				#print()
				
				#print('s3 about to go into compileProgram')
				#print(s3)
				(env, insts2, heap3) = compileProgram(env, s3, heap2 + 1)
				#print('HEAP3 - where rest of program goes')
				#print(heap3)
				#print()
				#heap4 = heap3 + 1
				#print('HEAP4')
				#print(heap4)
				#this makes it so that if mem[8] holds x (heap) and addr1 holds what x is, 8 points to addr1
				#instsAssign = \
				#["set " + str(heap3) + " " + str(addr1)\
				#]
				#THIS IS REDUNDANT AND NOT NEEDED? OK...?
				
				#copy(addr1, heap)\
				#print('ENVIRON ASSIGN AFTER CHANGE')
				#print(env)
				return (env, insts1 + insts2, heap3)

		
			elif label == 'While':
				e = children[0]
				fresh1 = freshStr()
				fresh2 = freshStr()
				fresh3 = freshStr()
				(insts1, addr1, heap1) = compileExpression(env, e, heap)
				s1 = children[1]
				(env2, insts2, heap) = compileProgram(env, s1, heap1 + 1)
				(insts3, env, heapLoop) = compileExpression(env, e, heap)
				s2 = children[2]
				(env2, insts4, heap) = compileProgram(env, s2, heap1 + 1)

				heap2 = heap + 1

				instWhile = insts1\
							+ ['branch true' + str(fresh1) + ' ' + str(heap1)]\
							+ insts4\
							+ ['goto finish' + str(fresh2)]\
							+ ['label true' + str(fresh1)]\
							+ ['label true' + str(fresh3)]\
							+ insts2\
							+ insts3\
							+ ['branch true' + str(fresh3) + ' ' + str(heapLoop)]\
							+ ['label finish' + str(fresh2)]
							
				return (env, instWhile, heap2)
				

			elif label == "If":
				e = children[0]
				s2 = children[2]
				s1 = children[1]
				fresh1 = freshStr()
				fresh2 = freshStr()
				(insts1, addr1, heap1) = compileExpression(env, e, heap)
				(env, insts2F, heap) = compileProgram(env, s2, heap1 + 1)
				(env, insts2T, heap) = compileProgram(env, s1, heap1 + 1)
				(env, insts3, heap) = compileProgram(env, s2, heap)

				heap2 = heap + 1

				instsIf = insts1 \
							+ ['branch true' + str(fresh1) + ' ' + str(heap1)]\
							+ insts2F\
							+ ['goto finish' + str(fresh2)]\
							+ ['label true' + str(fresh1)]\
							+ insts2T\
							+ insts3\
							+ ['label finish' + str(fresh2)]


				return (env, instsIf, heap2)

				
			elif label == 'Print':
				s1 = children[0]
				s2 = children[1]
				#print()
				#print('s1 and s2 in print')
				#print(s1)
				#print(s2)
				#print()
				#print('PRINT HEAP BEFORE IN PRINT')
				#print(heap)
				#print()
				
				(insts1, addr1, heap2) = compileExpression(env, s1, heap)
				
				
				#print('PRINT HEAP2 AFTER compile expression in Print')
				#print(heap2)
				#print()
				#print('PRINT ADDR1 after compileExpression in Print')
				#print(addr1)
				#print()
				#print('insts print 1')
				#print(insts1)
				#print()
				
				(env, insts2, heap3) = compileProgram(env, s2, heap2 + 1)
				#print('heap3 after compProg in print')
				#print(heap3)
				#print()
				#print('What is heap2 print')
				#print(heap2)
				instsPrint = \
					copy(heap2, 5)\
				
				return (env, insts1 + instsPrint + insts2, heap3)
			
			elif label == 'Procedure':
				name = children[0]['Variable'][0]
				body = children[1]
				s = children[2]
				#print()
				#print('environment Proc')
				#print(env)
				#print()
				#print(body)
				#print()
				#print('heap before proc body')
				#print(heap)
				
				(env, instsBody, heap2) = compileProgram(env, body, heap)
				#print(instsBody)
				#print()
				#print('HEAP HERE')
				#print(heap)
				#print(heap2)
				#print()
				#print('after env')
				#print(env)				
				#print()
				#print('instsBODY')
				#print(instsBody)
				#print()
				instsProcedure = procedure(name, instsBody)
				(env, insts1, heap3) = compileProgram(env, s, heap2)
				#heap4 = heap3 + 1
				#print()
				#print('THE FINAL HEAP')
				#print(heap3)
				#print(heap4)
				#print()
				#print('INSTS PROCEDURE')
				#print(instsProcedure)
				#print()
				#print(insts1)
				
				instsProcedureSet =\
				["set 7 0"\
				]\
				
				
				return (env, instsProcedureSet + instsProcedure + insts1, heap3)
		

		
			elif label == 'Call':
				name = children[0]['Variable'][0]
				s = children[1]
				#print('call children')
				#print(children[0])
				instsCall = call(name)
				(env, insts1, heap2) = compileProgram(env, s, heap)
				#print('call insts')
				#print()
				#print(instsCall)
				#print(heap)
				#print(heap2)
				
				instsCallSet =\
				["set 7 0"\
				]\
				
				#print(insts1, env, heap)
				return (env, instsCall + insts1, heap2)

				
				
	elif type(s) == Leaf:
		if s == 'End':
			return (env, [''], heap)
		

def compileExpression(env, e, heap):
	(insts1, addr, heap2) = compileFormula(env, e, heap)
	if insts1 == ['**NOT FORMULA**']:
		(insts1, addr, heap2) = compileTerm(env, e, heap)
	return (insts1, addr, heap2)



def compile(s):
	if s == '':
		return []
	
	tree = tokenizeAndParse(s)
	#print(tree)
	(env, insts, heap) = compileProgram({}, tree, 8)
	#print(insts, env, heap)
	return insts
	
	
	
#test = compileProgram({}, {'Print': ['True', 'End']} ,8)
#test = compileProgram({}, {'Print': ['False', 'End']} ,8)
#test = compileProgram({}, {'Print': [{'Number': [1203980]}, {'Print': [{'Number': [5]}, {'Print': ['False', 'End']}]}]} ,8)
#test = compileProgram({}, {'If': ['True', {'Print': [{'Number': [1203980]}, 'End']}, {'Print': [{'Number': [5]}, 'End']}]} ,8)
#test = compileProgram({}, {'While': ['False', {'Print': [{'Number': [1203980]}, 'End']}, {'Print': [{'Number': [5]}, 'End']}]} ,8)
#test = compileProgram({}, {'Assign': [{'Variable': ['x']}, {'Number': [15]}, {'Print': [{'Variable': ['x']}, 'End']}]} ,8)
#test = compileProgram({}, tokenizeAndParse("x := 10; print x + x;"), 8)
#test = compileProgram({}, tokenizeAndParse("x := true or false; print not(x) ;"), 8)
#test = compileProgram({}, tokenizeAndParse("x := true or false; print x ;"), 8)
#test = compileProgram({}, tokenizeAndParse("x := false and false; print x ;"), 8)
#test = compileProgram({}, tokenizeAndParse("x := true and false; print not(x) ;"), 8)
#test = compileProgram({}, tokenizeAndParse("print 3 + 4;"), 8)
#test = compileProgram({}, tokenizeAndParse("x := true or false; print x and not(x);"), 8)
#test = compile("x := 10; y := 2; z := 7; r := 5; g := 20; print g + r + x + r + y + z + r;")
#test = compile("x := 1; y := 2; z := 3; print x + y + z;")
#test = compileProgram({}, tokenizeAndParse("procedure f { print 55; } print 4;"), 8)
#test = compileProgram({}, tokenizeAndParse("procedure f { } print 4;"), 8)
#test = compile("procedure example {print 4;} call example;")
#test = compile("x := 123; y := 14; print x;")
#test = compileProgram({}, tokenizeAndParse("x := 123; print x;"), 8)
#test = compile("x := 123; procedure example {print x;} call example; call example;")
#test = compile("while true {print 3;} print 2;")
#test = compile("x := true ; y:= false; while x or y { if y { y:= false; } if x { x := false; } if not(y) { y:= true; } } print 2;")
#test = compile("x := false ; y:= true; x:= y; print x;")
#test = compile("procedure g {print 2;} procedure f { print 1; } call f;")
#test = compile("procedure g {print 2;} procedure f {call g; print 1; call g;} call f;") #FAIL
#test = compile("procedure g {print 2;} if true and true { call g; }") #PASS
#test = compile("procedure g {print 2;} procedure f {if true and true { call g; }} call g; call f;") #PASS
#test = compile("procedure h {print 3;} procedure g {print 2; call h; call h;} procedure f {call g; print 1; call g;} call f;") #FAIL
#test = compile("while false { print false; } print true;")
#test = compile("if true {print true;} print false; print 10;")
#test = compile("if true { } procedure x { }")
#test = compile("x := true; if true { x:= false; } print x;")
#test = compile("x := true; while false { x:= false; } print x;")
#test = compile("x := true; while not(x) { print false; } print true;")
#print(tokenizeAndParse("if true { x := 15; } print x;"))
test = compile("if true { x := 15; } print x;")
#test = compile("if true { print 15; } print 10;")
#test = compile("if true {procedure x { } } procedure x {}")
#test = compile("x := false or true and true and false; x := false")
#test = compile("x := false and not(true); x:= true or false;")
#test = compile("procedure x {procedure x {} }  call x;")
#test1 = compile("if false {print true;} print false; print 10;")
#test = compileProgram({}, {'Assign': [{'Variable': ['x']}, {'And': [{'Or': ['False', 'True']}, {'And': ['True', 'False']}]}, {'Assign': [{'Variable': ['x']}, 'False', 'End']}]}, 8)
#(insts, env, heap) = test	
#print(env, heap)
#print(simulate(insts))
print(simulate(test))
#print(simulate(test1))
#print(tokenizeAndParse("procedure x {procedure x {} }  call x;"))
	
