'''
Created by Ben Blau: bblau94@bu.edu
October 14th 2014
Professor Lapets CS320
Homework 3 interpret
Filename: interpret.py
Collab with Tyler Butler
'''

#exec(open("hw2/interpret.py").read())

exec(open("parse.py").read())

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
				x = children[0]
				if x in env:
					t = env[x]
					v = evalTerm(env, t)
					if v is None:
						v = evalFormula(env, t)
					env[x] = t
					return v
			#elif label == 'Parens':
			#	t = children[0]
			#	v = evalTerm(env, t)
			#	return v
			#elif label == 'Log':
			#	t = children[0]
			#	v = evalTerm(env, t)
			#	return floor(log2(v))
			elif label == 'Plus':
				t2 = children[1]
				v2 = evalTerm(env, t2)
				t1 = children[0]
				v1 = evalTerm(env, t1)
				return v1 + v2
			#elif label == 'Mult':
			#	t2 = children[1]
			#	v2 = evalTerm(env, t2)
			#	t1 = children[0]
			#	v1 = evalTerm(env, t1)
			#	return v1 * v2
			#elif label == 'LessThan':
			#	t2 = children[1]
			#	v2 = evalTerm(env, t2)
			#	t1 = children[0]
			#	v1 = evalTerm(env, t1)
			#	return v1 < v2
				
def evalFormula(env, f):
	if type(f) == Node:
		for label in f:
			children = f[label]
			if label == 'Variable':
				x = children[0]
				if x in env:
					f = env[x]
					v = evalFormula(env, f)
					if v is None:
						v = evalTerm(env, f)
					env[x] = f
					return v
				else:
					print(x + " is unbound.")
					exit()
			#elif label == 'Parens':
			#	f = children[0]
			#	v = evalFormula(env, f)
			#	return v
			elif label == 'Not':
				f = children[0]
				v = evalFormula(env, f)
				return not v
			elif label == 'Or':
				f1 = children[0]
				v1 = evalFormula(env, f1)
				if v1 == True: #or-short
					return True
				f2 = children[1]
				v2 = evalFormula(env, f2)
				return v1 or v2	
			elif label == 'And':
				f1 = children[0]
				v1 = evalFormula(env, f1)
				if v1 == False: #and-short
					return False
				f2 = children[1]
				v2 = evalFormula(env, f2)
				return v1 and v2					
			#elif label == 'Xor':
			#	f2 = children[1]
			#	v2 = evalFormula(env, f2)
			#	f1 = children[0]
			#	v1 = evalFormula(env, f1)
			#	return v1 != v2
			#elif label == 'Equal': #equal evaluates as formula then term if formula returns None (doesn't evaluate)
			#	f2 = children[1]
			#	v2 = evalFormula(env, f2)
			#	if v2 is None:
			#		v2 = evalTerm(env, f2)
			#	f1 = children[0]
			#	v1 = evalFormula(env, f1)
			#	if v1 is None:
			#		v1 = evalTerm(env, f1)
			#	return v1 == v2		
	elif type(f) == Leaf:
		if f == 'True':
			return True # Use the Python True constant.
		if f == 'False':
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
				p = children[2] #changed 2 to 1 for hw3
				env[x] = e
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
			elif label == 'Procedure':
				children = s[label]
				x = children[0]['Variable'][0]
				p1 = children[1]
				p2 = children[2]
				env[x] = p1
				(env, o) = execProgram(env, p2)
				return (env, o)
			elif label == 'Call':
				children = s[label]
				x = children[0]['Variable'][0]
				p2 = children[1]
				if x in env:
					p1 = env[x]
					(env2, o1) = execProgram(env, p1)
					(env3, o2) = execProgram(env2, p2)		
					return (env3, o1 + o2)
				else:
					print(x + " is unbound.")
					exit()
	elif type(s) == Leaf:
		if s == 'End':
			return (env, [])


		
def interpret(string):
	#empty check
	if string == '':
		return []
	
	#program check. Should cover everything now?
	tree = tokenizeAndParse(string)
	if not tree is None:
		(env1, o) = execProgram({}, tree)
		return o
'''	
	#formula check
	tree = formulaParse(tokenize(grammar,string), True)
	#print(tree)
	if not tree is None:
		(parsed, extra) = tree
		(env, o) = execProgram({}, parsed)
		return o

	#term check
	tree = termParse(tokenize(grammar,string), True)
	(parsed, extra) = tree
	(env, o) = execProgram({}, parsed)
	return o
'''
