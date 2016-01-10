#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
# Benjamin Blau U94434268
# Due: October 29th 2014

exec(open("parse.py").read())

Node = dict
Leaf = str


#value :: = true | false | number
#value is the result(s) of an evaluation algorithm. It is either a boolean or number
def evaluate(env, e):
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == 'Number':
				e = children[0]
				return e
			elif label == 'Variable':
				x = children[0]
				if x in env:
					return env[x] #n
				else:
					print(x + " is unbound.")			
					
			elif label == 'Array':
				x = children[0]['Variable'][0]
				if x in env:
					e = children[1] #e is the number we are looking for - @ x [ e ] - can't be true or false 
					k = evaluate(env, e)
					if k >= 0 and k <= 2 and k is not True and k is not False:
						nk = env[x] #nk = array variable we are looking at. nk[k] is the specific child
						return nk[k]							
			elif label == 'Plus':
				e2 = children[1]
				n2 = evaluate(env, e2)
				if type(n2) == bool:
					break
				e1 = children[0]
				n1 = evaluate(env, e1)
				if type(n1) == bool:
					break
				return n1 + n2
	
	elif type(e) == Leaf:
		if e == 'True':
			return True
		if e == 'False':
			return False
			

			
def execute(env, s):
	if type(s) == Node:
		for label in s:
			children = s[label]
			if label == 'Print':
				e = children[0]
				p = children[1]
				v = evaluate(env, e)
				(env, o) = execute(env, p)
				return (env,[v] + o)
			elif label == 'Assign':
				array = []
				x = children[0]['Variable'][0]
				e0 = children[1]
				e1 = children[2]
				e2 = children[3]
				p = children[4]
				array.append(evaluate(env, e0)) #n0 - Putting into array
				array.append(evaluate(env, e1)) #n1
				array.append(evaluate(env, e2)) #n2
				env[x] = array
				(env, o) = execute(env, p)
				return (env, o)
			elif label == 'For': #('For',  ['for', variable, '{', program, '}', program]),\
				x = children[0]['Variable'][0]
				#if x in env:
					#print("Cannot use variable " + x + " as your For loop variable since it is already assigned in the environment.")
				#	return None
				#else:
				p1 = children[1]
				p2 = children[2]
				env1 = env.copy()
				env1[x] = 0
				(env2, o1) = execute(env1, p1)
				env2[x] = 1
				(env3, o2) = execute(env2, p1)
				env3[x] = 2
				(env4, o3) = execute(env3, p1)
				(env5, o4) = execute(env1, p2)
				return env5, o1 + o2 + o3 + o4

			
	elif type(s) == Leaf:
		if s == 'End':
			return (env, [])

			
#NOTE!!! ****************************************
#I have structured my program so that if we are not allowed to catch exceptions
#please just delete the try and catch and everything should still run fine!	
def interpret(s):
	#empty check
	if s == '':
		return []
	tree = tokenizeAndParse(s)
	if not tree is None:
		try:
			(env, o) = execute({}, tree)
			return o
		except:
			return None
			
####TESTS####			
#test = interpret("assign x := [1+2,4,6]; print @x[-1]; print @x[0];print @x[1];print @x[2];print @x[false];print @x[true];print @x[10];")	
#test = interpret("assign x := [true,false,1 + 2 + 3 + 4 + 10]; print @x[-1]; print @x[0];print @x[1];print @x[2];print @x[false];print @x[true];print @x[10];")	
#test = interpret("assign x := [1+2,4,6]; print @x[0] + @x[2];")	
#test = interpret("print 3;")	
#test = interpret("print x; print 3;")	
#test = interpret("assign x := [1+2,4,6]; for y { print 7;} print @x[0];")#if both variables were x this wouldn't work?
#test = interpret("assign x := [1+2,4,6]; for y { print 7;} print x;")
#test = interpret("for x { print 7;} assign x := [1+2,4,6]; print @x[2];") #this works because assigning x after using x in for
#test = interpret("assign x := [1+2,4,6]; assign x := [@x[0] + 5,@x[1] + @x[0],@x[2] + -6]; print @x[0];print @x[1];print @x[2];")
#test = interpret("assign x := [1+2,4,6]; print x;")
#test = interpret("print false + 3;")
#test = interpret("print true + 3;")
#test = interpret("print 3 + false;")
#test = interpret("print 3 + false;")
#test = interpret("print true + false;")
#test = interpret("assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2];")
#test = interpret("assign a := [2,2,2]; for x {print @a[2];} print @a[2];")
#test = interpret("assign a := [2,2,2]; for x {print @a[2];} print @a[2];")
#test = interpret("assign a := [2,2,2]; for a {print @a[2];} print @a[2];")
#print(test)
			
#print(execute({},{'Assign': [{'Variable': ['a']}, {'Number': [2]}, {'Number': [2]}, {'Number': [2]}, {'For': [{'Variable': ['a']}, {'Print': [{'Array': [{'Variable': ['a']}, {'Number': [2]}]}, 'End']}, {'Print': [{'Array': [{'Variable': ['a']}, {'Number': [2]}]}, 'End']}]}]}))
#eof