'''
Created by Ben Blau: bblau94@bu.edu
September 18th 2014
Professor Lapets CS320
Homework 2 parse
Filename: parse.py
Collab with Tyler Butler
Note* BOTH Completed Extra Credit (To my own knowledge both work in full - subject to be wrong \
if I missed specific test cases)
'''
#exec(open("hw2/parse.py").read())


import re
def tokenize(T, css):
	tokenString = '('
	T = (re.escape(t) for t in T)
	for t in T:
		tokenString = tokenString + t + '|'
	tokenString = tokenString + '\s+)'

	newTokens = [t for t in re.split(tokenString,css)]

	return [b for b in newTokens if not b.isspace() and not b == ""]

	
#helper methods to add in top below
def number(tokens):
	return numberParse(tokens, True)
	
def numberParse(tokens, top):
	if re.match(r"^([1-9][0-9]*)", tokens[0]):
		return (int(tokens[0]), tokens[1:])
#next if accounts for negatives		
	if re.match(r"^(-[1-9][0-9]*)$", tokens[0]): 
		return (int(tokens[0]), tokens[1:])
#next for taking into account 0, could have (or maybe not, didn't try) used re.match, this was simpler...	
	if tokens[0] == '0':
		return (int(tokens[0]), tokens[1:])
	

def variable(tokens):
	return variableParse(tokens, True)
	
def variableParse(tokens, top):
	if isToken(tokens[0]) != 0:
		return None
	if re.match(r"^([a-z]+[a-zA-Z0-9]*)$", tokens[0]):
		return (str(tokens[0]), tokens[1:])

def variableAssignParse(tokens, top):
	if isToken(tokens[0]) != 0:
		return None
	if re.match(r"^([a-z]+[a-zA-Z0-9]*)$", tokens[0]):
		return ({'Variable':[str(tokens[0])]}, tokens[1:])
		
def formula(tokens):
	return formulaParse(tokens, True)

def term(tokens):
	return termParse(tokens,True)

def factor(tokens):
	return factorParse(tokens, True)

def program(tokens):
	return programParse(tokens, True)
	
'''
def complete(string):
	grammar = [':=','print', ';', 'assign','@','end','true',\
'false','not','and','or','(',')','equal','less than',\
'greater than','&&','||','==','<','>','plus',',','mult',\
'log','#','+','*', 'xor', 'parens', 'while', 'if', 'end', 'variable', \
'number']
	return programParse(tokenize(grammar, string), True)
'''
#isToken is just used to see if the variable attempting to be assigned is already taken by the language
def isToken(tokens):
	grammar = [':=','print', ';', 'assign','@','end','true',\
'false','not','and','or','(',')','equal','less than',\
'greater than','&&','||','==','<','>','plus',',','mult',\
'log','#','+','*', 'xor', 'parens', 'while', 'if', 'end', 'variable', \
'number']
	return grammar.count(tokens)

def formulaParse(tmp, top):
	seqs = [\
		('Xor', [leftFormula, 'xor', formulaParse]), \
		('Equal', [leftFormula, '==', formulaParse]), \
		#('Equal', [leftFormula, '==', formulaParse]), \
		('Left', [leftFormula]), \
		]

	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if len(tokens) == 0: #this covers returning None if this list is empty
					break
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
	
		if len(ss) + len(es) == len(seq):
			if label == 'Left':
				return (es[0], tokens)
			else:
				return ({label:es} if len(es) > 0 else label, tokens)

				
def leftFormula(tmp, top):
	seqs = [\
		('True', ['true']), \
		('False', ['false']), \
		('Not', ['not', '(', formulaParse, ')']), \
		('Parens', ['(', formulaParse, ')']), \
		('Equal', [termParse, '==', termParse]), \
		('LessThan', [termParse, '<', termParse]), \
		('Variable', [variableParse]) \
		]

	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if len(tokens) == 0:
				break
			if type(x) == type(""):
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			return ({label:es} if len(es) > 0 else label, tokens)

				
'''
def formula(tokens):

	(e1, tokens) = leftFormula(tokens)
	if tokens[0] == 'xor':
		(e2, tokens) = formula(tokens[1:])
		return ({'Xor':[e1,e2]}, tokens[1:])
	
	return (e1, tokens) #if a lone program (in this case true, false, variable) was fed in
	#return None
		# Final return None if nothing works
'''
'''	
def leftFormula(tokens, top):

	(e1, tokens) = leftFormula(tokens, top)
	if tokens[0] == 'xor':
		(e2, tokens) = formula(tokens[1:])
		return ({'Xor':[e1,e2]}, tokens[1:])
	else:	
		r = variable(tokens, True)
		if not r is None:
			(e, tokens) = r
			return ({'Variable':[e]}, tokens[0:])
		

	if tokens[0] == 'true':
		return ('True', tokens[1:])

	if tokens[0] == 'false':
		return ('False', tokens[1:])

	if tokens[0] == 'not' and tokens[1] == '(':
		(e1, tokens) = formula(tokens[2:])
		if tokens[0] == ')':
			return ({'Not':[e1]}, tokens[1:])
	
	if tokens[0] == '(':
		(e1, tokens) = formula(tokens[1:])
		if tokens[0] == ')':
			return ({'Parens':[e1]}, tokens[1:])

		
	#return (None, tokens[0:])
'''
'''	
def term(tokens):
	(e1, tokens) = factor(tokens)
	if tokens[0] == '+':
		(e2,tokens) = term(tokens[1:])
		return ({'Plus':[e1,e2]}, tokens[0:])
		
	return (e1, tokens) #if a lone factor was fed in

def factor(tokens):
	(e1, tokens) = leftFactor(tokens)
	if tokens[0] == '*':
		(e2, tokens) = leftFactor(tokens[1:])
		return ({'Mult':[e1,e2]}, tokens[0:])
	
	return (e1, tokens) #if a lone factor was fed in

def leftFactor(tokens):
	if tokens[0] == 'log' and tokens[1] == '(':
		(e1, tokens) = term(tokens[2:])
		if tokens[0] == ')':
			return ({'Log':[e1]}, tokens[1:])	
		
	if tokens[0] == '(':
		(e1, tokens) = term(tokens[1:])
		if tokens[0] == ')':
			return ({'Parens':[e1]}, tokens[1:])
	
	r = variable(tokens)
	if not r is None:
		(e, tokens) = r
		return ({'Variable':[e]}, tokens[0:])

	s = number(tokens)
	if not s is None:
		(e, tokens) = s
		return ({'Number':[e]}, tokens[0:])		
	
'''
def termParse(tmp, top):
	seqs = [\
		('Plus', [factorParse, '+', termParse]), \
		#('Equal', [factorParse, '==', termParse]), \ TOOK CARE OF IN EXPRESSION
		#('LessThan', [factorParse, '<', termParse]), \
		('Factor', [factorParse]) \
		]

	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if len(tokens) == 0: #returns None
					break
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
	
		if len(ss) + len(es) == len(seq):
			if label == 'Factor':
				return (es[0], tokens)
			else:
				return ({label:es} if len(es) > 0 else label, tokens)


				
				
def factorParse(tmp, top):
	seqs = [\
		('Mult', [leftFactor, '*', factorParse]), \
		('LeftFactor', [leftFactor]) \
		]

	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if len(tokens) == 0: #returns None
					break
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			if label == 'LeftFactor':
				return (es[0], tokens)
			else:
				return ({label:es} if len(es) > 0 else label, tokens)
	
def leftFactor(tmp, top):
	seqs = [\
		('Log', ['log', '(', termParse, ')']), \
		('Parens', ['(', termParse, ')']), \
		('Number', [numberParse]), \
		('Variable', [variableParse]) \
		]

	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if len(tokens) == 0: #returns None
					break
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			return ({label:es} if len(es) > 0 else label, tokens)


	
def programParse(tmp, top):
	seqs = [\
		('Print', ['print', expressionParse, ';', programParse]), \
		('Assign', ['assign', variableAssignParse, ':=', expressionParse, ';', programParse]), \
		('If', ['if', expressionParse, '{', programParse, '}', programParse]), \
		('While', ['while', expressionParse, '{', programParse, '}', programParse]), \
		('End', []) \
		]
	
	for (label, seq) in seqs:
		tokens = tmp[0:]
		ss = []
		es = []
		for x in seq:
			if type(x) == type(""):
				if len(tokens) == 0: #return None
					break
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else:
					break
			else:
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r				
					es = es + [e]
		if len(ss) + len(es) == len(seq):
			return ({label:es} if len(es) > 0 else label, tokens)

	

def expression(tokens):
	return expressionParse(tokens, True)



def expressionParse(tokens, top):
	#if statement to avoid feeding true/false return as a variable through term. Could have moved formula first, either would work
	tmp = tokens[0:]
	r = formulaParse(tmp, top)
	if not r is None:
		(e1, tokens) = r
		if (tokens[0] == ';' or tokens[0] == '{'):
			return r
		'''	
		if tokens[0] == '==':
			(e2,tokens) = formula(tokens[1:])
			return ({'Equal':[e1,e2]}, tokens[0:])
		'''	
	s = termParse(tmp, top)
	if not s is None:
		(e1, tokens) = s
		if (tokens[0] == ';' or tokens[0] == '{'):
			return s
		'''
		if tokens[0] == '<':
			(e2,tokens) = term(tokens[1:])
			return ({'LessThan':[e1,e2]}, tokens[0:])
		if tokens[0] == '==':
			(e2,tokens) = term(tokens[1:])
			return ({'Equal':[e1,e2]}, tokens[0:])
		'''
#print(program(['print', '3', '+', '2', '==', '5', ';']))
#print(program(['print', '3', '+', '2', '==', '5', ';']))			
#print(program(['print', '3', '==', '4', ';']))
#print(program(['print', 'true', '==', 'true', ';']))
#print(program(['print', 'x', '*', '3', ';']))
#print(formula(['x']))		
#print(formula(['x'], True))
#print(formula(['x', 'xor', 'y', 'a'], True))	
#print(complete("assign x := true; if x { while x xor false { print 123; assign x := x xor true; } } print x;"))
#print(program(['print', 'true', ';', 'end', ';']))
#print(formula(['not', '(', 'true', ')', 'a', 'b']))	
#print(program(['while', 'true', '{', 'print', 'true', ';', '}', 'print', 'false', ';', 'abc']))
#print(program(['print', 'aa', ';', 'print', 'ab', 'absc']))	
#print(expression(['false', 'true', 'b']))	
#print(expression(['a123A', 'b']))
#print(term(['sdasdss', '+', 'aA3521'], True))
#print(term(['a', '+', '3'], True))			
#print(term(['7', '+', '3'], True))	
#print(term(['4', '+', 'b'], True))	
#print(term(['a', '*', '3'], True))			
#print(term(['7', '*', '3'], True))	
#print(term(['4', '*', 'b'], True))	
				