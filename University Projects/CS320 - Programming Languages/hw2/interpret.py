'''
Created by Ben Blau: bblau94@bu.edu
September 18th 2014
Professor Lapets CS320
Homework 2 interpret
Filename: interpret.py
Collab with Tyler Butler
Note* BOTH Completed Extra Credit (To my own knowledge both work in full - subject to be wrong \
if I missed specific test cases)
'''
#exec(open("hw2/interpret.py").read())

from math import log2,floor
import parse

Node = dict
Leaf = str

def evalTerm(env, t):
	if type(t) == Node:
		for label in t:
			children = t[label]
			if label == 'Number':
				t = children[0]
				return t
			elif label == 'Variable':
				t = children[0]
				v = env[t]
				return v
			elif label == 'Parens':
				t = children[0]
				v = evalTerm(env, t)
				return v
			elif label == 'Log':
				t = children[0]
				v = evalTerm(env, t)
				return floor(log2(v))
			elif label == 'Plus':
				t2 = children[1]
				v2 = evalTerm(env, t2)
				t1 = children[0]
				v1 = evalTerm(env, t1)
				return v1 + v2
			elif label == 'Mult':
				t2 = children[1]
				v2 = evalTerm(env, t2)
				t1 = children[0]
				v1 = evalTerm(env, t1)
				return v1 * v2
			elif label == 'LessThan':
				t2 = children[1]
				v2 = evalTerm(env, t2)
				t1 = children[0]
				v1 = evalTerm(env, t1)
				return v1 < v2
				
def evalFormula(env, t):
	if type(t) == Node:
		for label in t:
			children = t[label]
			if label == 'Variable':
				x = children[0]
				if x in env:
					return env[x]
				else:
					print(x + " is unbound.")
					exit()
			elif label == 'Parens':
				f = children[0]
				v = evalFormula(env, f)
				return v
			elif label == 'Not':
				f = children[0]
				v = evalFormula(env, f)
				return not v
			elif label == 'Xor':
				f2 = children[1]
				v2 = evalFormula(env, f2)
				f1 = children[0]
				v1 = evalFormula(env, f1)
				return v1 != v2
			elif label == 'Equal': #equal evaluates as formula then term if formula returns None (doesn't evaluate)
				f2 = children[1]
				v2 = evalFormula(env, f2)
				if v2 is None:
					v2 = evalTerm(env, f2)
				f1 = children[0]
				v1 = evalFormula(env, f1)
				if v1 is None:
					v1 = evalTerm(env, f1)
				return v1 == v2		
	elif type(t) == Leaf:
		if t == 'True':
			return True # Use the Python True constant.
		if t == 'False':
			return False # Use the Python False constant.

			
def execProgram(env, s):
	if type(s) == Node:
		for label in s:
			if label == 'Print':
				children = s[label]
				e = children[0]
				p = children[1]
				v = evalTerm(env, e)
				if v is None:
					v = evalFormula(env, e)
				(env, o) = execProgram(env, p)
				return (env,[v] + o) 
			elif label == 'Assign':
				children = s[label]
				x = children[0]['Variable'][0]
				e = children[1]
				p = children[2]
				if assignCheck(x, p) == True:
					#This checks to see if a variable is in the rest of the program when assigned.
					#If a variable is assigned/reassigned at the end of the program it has a check within to cover this.
					v = evalFormula(env, e)
					if v is None:
						v = evalTerm(env, e)
					env[x] = v
					(env, o) = execProgram(env, p)

					return (env, o)
				else:
					#print('Variable \'' + x + '\' does not appear in the rest of the program. \"Assign ' + x + ' := \" was not executed.')
					(env, o) = execProgram(env, p)
					return (env, o)
			elif label == 'If':
				children = s[label]
				e = children[0]
				p1 = children[1]
				p2 = children[2]
				v = evalTerm(env, e)
				if v is None:
					v = evalFormula(env, e)
				if v == False: #if false
					(env2, o1) = execProgram(env, p2)	
					return (env2 , o1)
				if v == True: #if true
					(env2, o1) = execProgram(env, p1)
					(env3, o2) = execProgram(env2, p2)
					return (env3, o1 + o2)
			elif label == 'While':
				children = s[label]
				e = children[0]
				p1 = children[1]
				p2 = children[2]
				v = evalTerm(env, e)
				if v is None:
					v = evalFormula(env, e)
				if v == False: #while false
					(env2, o) = execProgram(env, p2)	
					return (env2 , o)
				o = []
				while v == True: #while true
					(env2, o1) = execProgram(env, p1)
					v = evalTerm(env2, e)
					if v is not None:
						o = o + o1
					else:
						v = evalFormula(env2, e)
						o = o1
				(env3, o2) = execProgram(env2, p2)
				return (env3, o + o2)
	elif type(s) == Leaf:
		if s == 'End':
			return (env, [])


def assignCheck(variable, program):
	if type(program) == Node:
		for label in program:
			children = program[label]
			if label == 'Variable':	#if we are currently unpacking a variable
				check = children[0]	#pull out the variable
				if variable == check: #compare the variable we are looking for with the one we pulled
					return True
				else: #break out of recursive call if it's not
					break			
			elif label == 'Assign':	#if we hit the assign case we need to skip over the assign
				#this case skips over the assign and variable label
				return assignCheck(variable, children[2])
			else:
				if assignCheck(variable, children[0]) == True: #we pulled out a program ; program
					#this checks the first program, if true returns true, if false--
					return True
				else:#this will check if the second program is true now
					if assignCheck(variable, children[1]) == True:
						return True
					else:#and if it is not it will return false. No variable match was found at this point
						return False
	if type(program) == Leaf: #covers leafs - end, true, false, etc
		return True
	#if program == 'End': 
	#	print(type(program))
		#this test case covers when values are reassigned at the end of a program
	#	return True
	#if program == 'True' or program == 'False':
	#	return True

		
def interpret(string):
	grammar = [':=','print', ';', 'assign','end', 'true',\
'false','not','and','or','(',')','equal','less than',\
'greater than','&&','||','==','<','>','plus',',','mult',\
'log','+','*', 'xor', 'parens', 'while', 'if', 'variable', \
'number', 'log']
	
	#empty check
	if string == '':
		return []
	
	#formula check
	tree = formulaParse(tokenize(grammar,string), True)
	if not tree is None:
		(parsed, extra) = tree
		(env, o) = execProgram({}, parsed)
		return o

	#term check
	tree = termParse(tokenize(grammar,string), True)
	if not tree is None:
		(parsed, extra) = tree
		(env, o) = execProgram({}, parsed)
		return o
		
	#program check
	tree = programParse(tokenize(grammar,string), True)
	(parsed, extra) = tree
	(env1, o) = execProgram({}, parsed)
	return o
	

	
#print(interpret("print ( ( not ( (true ))) == true ) ;"))	
#print(interpret("print  (log ( 8 ) < 3)  ;"))	
#print(interpret("print(  ( log(8) ) < 4  ) ;"))
#print(interpret("print 3 * 4 + 5;"))
#print(interpret("print 5 + (3 + 4) * 5 + 2;"))
#print(interpret("print not ( true ) == false ;"))
#print(interpret("print 3 + 2 < 6;"))
#print(interpret("assign x := true; if x { while x xor false { print 123; assign x := x xor true; } } print x;"))	
#print(interpret("assign x := 5; assign y := true; while x < 10 { print x; print y; assign x := x + 1; assign y := not ( y );} print x; print y;"))	
#print(interpret("assign x := 5 ; print x; while x < 54 { assign x := x + 3; } print x;"))
#print(interpret("print ( true ) ;"))		
#print(interpret("print not (true);"))	
#print(interpret("assign x := true; print x; print not ( x );"))
#print(interpret("assign x := 10; print x * 7;"))
#print(interpret("assign x := 5; assign y := 6; print x*y; assign x := 15; print ( false );"))	
#print(interpret("assign x := 5 ; while x < 10 { print x; assign x := x + 1; } print x; "))
#print(interpret("assign x := true; while x { print x; assign x := false; } print x;"))
#print(interpret("assign x := true; while x { print x; assign x := false; } print x; assign z := 23 ; print x;"))	
#print(evalTerm([], {'LessThan': [{'Number': [-1]}, {'Number': [0]}]}))
#print(interpret("print false == true ;"))	
#print(evalFormula({}, {'Parens': [{'Xor': ['True', 'False']}]}))
#print(interpret("assign x := 2 ; while x < 10 { assign x := x + 1 ; print x ;}"))
#print(execProgram({}, {'Print': ['True', 'End']}))
#print(interpret("print true ;"))
#print(interpret("assign x := 3+4 ; assign y := 5 ; assign z := 90; print x*y;"))			
#print(execProgram({}, {'Print': ['Plus': [{'Number': [0]}, {'Number': [1]}]]}))			
#print(execProgram({'z': 32},{'Print': [{'Mult': [{'Variable': ['z']}, {'Number': [3]}]}, 'End']}))