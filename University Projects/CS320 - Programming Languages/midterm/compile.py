#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
# Ben Blau U94434268
# Due: October 29th 2014

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

#Invalid cases that follow the correct type will simply not work.
#If you attempt to print from some array - "print @a[3];" you will get nothing
#in return. If you have "print 3; print @a[3]; print 4;" you will get your 3 back
#but nothing past the improper case will be returned.


def freshStr():
	return str(randint(0,10000000))

#copyAddressWithinTo is his copyFromRef
#copyToRef(6,7) if 7 points to -1, mem[-1] = program location (in 6)	
def compileExpression(env, e, heap):
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == 'Number':
				#print("WHY")
				n = children[0]
				heap = heap + 1
				return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
			elif label == 'Plus':
				#print('HI')
				[e1, e2] = children
				(insts1, addr1, heap2) = compileExpression(env, e1, heap)
				(insts2, addr2, heap3) = compileExpression(env, e2, heap2)
				#heap4 = heap3 + 1
				#print('PLUS')
				#print(heap2, heap3)
				#print(addr1, addr2)
				
				instsPlus = \
					copy(addr1, 1)\
					+copy(addr2, 2)\
					+[\
					"add"\
					]\
					+copy(0,heap3)\
					
				return (insts1 + insts2 + instsPlus, heap3, heap3)
			elif label == 'Array':
			#@ variable [ expression ]
				x = children[0]['Variable'][0]
				e = children[1]
				fresh = freshStr()
				(instsE, addr, heap2) = compileExpression(env, e, heap)
				instsArray =\
					['set 1 -2']\
					+ copy(heap2, 2)\
					+ ['add']\
					+ ['branch notTwo' + fresh + ' 0']\
					+ ['label kIsTwo' + fresh]\
					+ ['set 1 2']\
					+ ['set 2 ' + str(env[x])]\
					+ ['add']\
					+ copy(0, heap2)\
					+ copyFromRef(heap2, heap2)\
					+ ['goto finish' + fresh]\
					+ ['label notTwo' + fresh]\
					+ ['set 1 -1']\
					+ copy(heap2, 2)\
					+ ['add']\
					+ ['branch notOne' + fresh + ' 0']\
					+ ['label kIsOne' + fresh]\
					+ ['set 1 1']\
					+ ['set 2 ' + str(env[x])]\
					+ ['add']\
					+ copy(0, heap2)\
					+ copyFromRef(heap2, heap2)\
					+ ['goto finish' + fresh]\
					+ ['label notOne' + fresh]\
					+ ['set 1 0']\
					+ copy(heap2, 2)\
					+ ['add']\
					+ ['branch invalidK!' + fresh + ' 0']\
					+ ['label kIsZero' + fresh]\
					+ ['set ' + str(heap2) + ' ' + str(env[x])]\
					+ copyFromRef(heap2, heap2)\
					+ ['goto finish' + fresh]\
					+ ['label invalidK!' + fresh]\
					+ ['goto endPrint']\
					+ ['set ' + str(heap2) + ' 0']\
					+ ['label finish' + fresh]\
					
		#goto endPrint will skip the print statement if an invalid k is used
		#the set heap2 0 was my original method that would simply output 0 if given an invalid k
		#but this would also change any value to 0 if you tried reassigning part of an array into
		#a new one. Left it in for the sake of remembering.
		#This will also prevent reassigning variables in a way such as assign x := [1,2,3]
		# print @x[1] , 2, 3 then assign x := [@x[3], 2, 1] followed by print @x[0]..1...2.
		# If this was attempted and you tried to print out the new @x[0] 1 or 2 it would no longer work.
		
		
		#		instsArray =\
		#			['set 1 ' + str(env[x])]\
		#			+ copy(heap2, 2)\
		#			+ ['add']\
		#			+ copy(0,heap2)\
		#			+ copyFromRef(heap2, heap2)\
					
				return(instsE + instsArray, heap2, heap2)
				
				
	elif type(e) == Leaf:
		if e == 'True':
			heap = heap + 1
			inst = 'set ' + str(heap) + ' 1'
			return ([inst], heap, heap)
		if e == 'False':
			heap = heap + 1
			inst = 'set ' + str(heap) + ' 0'
			return ([inst], heap, heap)
			
	#pass # Complete 'True', 'False', 'Array', and 'Plus' cases for Problem #3.


#Note that heap = 7 default will not actually use 7 because all of the base cases
#increment the heap before using them. In my homework3 I changed the incrementing
#to happen after something was put on the heap for an attempt at slightly more efficient
#memory usage. For the midterm I did not worry about this as much. I just made sure everything
#worked to the best of my knowledge, not to the most efficient manner.
	
def compileProgram(env, p, heap = 7): # Set initial heap default address.
	if type(p) == Leaf:
		if p == 'End':
			return (env, [], heap)

	if type(p) == Node:
		for label in p:
			children = p[label]
			if label == 'Print':
				[e, p] = children
				(instsE, addr, heap2) = compileExpression(env, e, heap)
				(env, instsP, heap3) = compileProgram(env, p, heap2)
				return (env, instsE + copy(addr, 5) + instsP + ["label endPrint"], heap3)

			elif label == 'Assign':
	#['assign', variable, ':=', '[', expression, ',', expression, ',', expression, ']', ';', program]
				x = children[0]['Variable'][0]
				e1 = children[1]
				e2 = children[2]
				e3 = children[3]
				p = children[4]
				(instsE1, addr1, heap2) = compileExpression(env, e1, heap)
				(instsE2, addr2, heap3) = compileExpression(env, e2, heap2)
				(instsE3, addr3, heap4) = compileExpression(env, e3, heap3)
				heap5 = heap4 + 1
				heap6 = heap5 + 1
				heap7 = heap6 + 1
			
				#The heaps above I used specifically for the cases where I am reassigning arrays.
				#as in the cases of "assign x := [2,3,4]" followed by another case of assign x
				#in which the array machine code is used to reassign each expression in the new
				#x as some extension of the old x. As in the new x could contain @x[0] in one spot
				#with the intention of duplicating the old x[0] (2 in this case) into the x[0] location.
				#It also/more specifically helped when doing something along the lines of that but
				#when assigning a new location as an addition of an array location and another 'Number'
				#such as an actual integer or another array location (or any multiple of them).
				#Ex: reassigning one of the new x spots to @x[0] + 1 + @x[2] + @x[2] +...
				instsAssign =\
					["set " + str(heap5) + " 0 "]\
					+ ["set " + str(heap6) + " 0 "]\
					+ ["set " + str(heap7) + " 0 "]\
					+ copy(heap2, heap5)\
					+ copy(heap3,heap6)\
					+ copy(heap4,heap7)\
				
				env[x] = heap5
				#heap5 6 and 7 now point to the 3 @x[0-2] values (it puts them in mem in consecutive order)
				(env, instsP, heap8) = compileProgram(env, p, heap7)
				return (env, instsE1 + instsE2 + instsE3 + instsAssign + instsP, heap8)		
			
	#pass # Complete 'Assign' case for Problem #3.

	
def compile(s):
	p = tokenizeAndParse(s)
	# Add call to type checking algorithm for Problem #4.
	if typeProgram({},p) != 'Void':
		print('\nType Error: Will Not Compile')
		return None
	# Add calls to optimization algorithms for Problem #3.
	p = foldConstants(unrollLoops(p))
	(env, insts, heap) = compileProgram({}, p)
	return insts

def compileAndSimulate(s):
	x = compile(s)
	if x is not None:
		return simulate(x)
	return None

	
	

####TESTS####
#test = compileProgram({},tokenizeAndParse("print 4 + 2 + 1 + 0 + 3 + 6 +11 + -27;"))
#test = compileProgram({},tokenizeAndParse("print true + true;"))
#test = compileProgram({x : 8},tokenizeAndParse("print @x[0];"))
#test = compileProgram({},tokenizeAndParse("assign x:= [12,25,36]; print @x[0];"))
#test = compileProgram({},tokenizeAndParse("assign x:= [true,25,36]; print @x[0];"))
#test = compileProgram({},tokenizeAndParse("assign x:= [2,25,36]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0],@x[1],@x[2]]; print @x[0];print @x[1];print @x[2];"))
#if test is not None:
#	(env, insts, heap) = test
#	print(simulate(insts))	
#else:
#	print('INVALID SYNTAX')
#(env, insts, heap) = test
#print(env)
#print(simulate(insts))
	
#print(compileAndSimulate("print 2; for a {}")) #for only works when run through compile/compileAndSimulate because of loop unrolling
#print(compileAndSimulate("assign x:= [true,25,36]; print @x[1];"))	
#print(compileAndSimulate("assign x:= [1,25,36];print @x[0];print @x[1];print @x[2];assign x:= [@x[20],@x[1],@x[0]];"))	
#print(compileAndSimulate("assign x:= [1,25,36];print @x[0];print @x[1];print @x[2];assign x:= [@x[2],@x[1],@x[3]];print @x[1];print @x[1];print @x[2];"))	#this case tests invalid k's for reassigning
#print(compileAndSimulate("print 2; for a {} "))	
#print(compileProgram({},{'Print': [{'Number': [2]}, {'For': [{'Variable': ['a']}, 'End', 'End']}]},8))
#print(compileAndSimulate("assign x:= [2,25,36]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0],@x[1],@x[2]]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0],@x[1],@x[2]]; print @x[0];print @x[1];print @x[2];"))	
#print(compileAndSimulate("assign x:= [2,25,36]; print @x[0] + 1;"))	
#print(compileAndSimulate("assign x:= [true,25,36]; print @x[0] + @x[1];"))	
#print(compileAndSimulate("assign x:= [10,5,36]; print @x[0] + @100[1];"))	
#print(compileAndSimulate("assign x:= [10,5,36]; print @x[4];"))	
#print(compileAndSimulate("assign x:= [10,5,3]; print x;"))	
#print(compileAndSimulate("print 101 + -102;"))	
#print(compileAndSimulate("assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[1] + @x[0] + -10 + @x[2]]; print @x[0];print @x[1];print @x[2];"))	
#print(compileAndSimulate("assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0];print @x[1];print @x[2];assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0] + 15;print @x[1] + 6 + -50;print @x[2];"))	
#print(compileAndSimulate("print 3 + true;"))
#print(compileAndSimulate("assign x:= [2,7,10]; print @x[0] + @x[0] + @x[1];print @x[1] + @x[1];print @x[2];"))	
#print(compileAndSimulate("for x {print 11 + 2; } print 3;"))	
#print(compileAndSimulate("for 1 {print 11 + 2; } print 3;"))	
#print(compileAndSimulate("for x { } "))	
#print(compileAndSimulate("for x { for x {}} for x {} "))	
#print(compileAndSimulate("print@x[0];"))
#print(compileAndSimulate("assign x:= [1 + 5 + 123, 11 + 2, 3 + 5]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0],@x[1] + @x[1],@x[2]]; print @x[0];print @x[1];print @x[2];"))


#eof