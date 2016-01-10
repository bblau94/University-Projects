'''
Created by Ben Blau
September 4th 2014
Professor Lapets CS320
Homework 1
Filename: hw1.py
Collab with Tyler Butler
'''
#exec(open("hw1.py").read())

#T = list of tokens, css = concrete syntax string

'''
build a regular expression, use that regular expression to convert the second string
into a token sequence (represented in Python as a list of strings), and then return that token sequence. 
tokenize(["red", "blue", "#"], "red#red blue# red#blue")
['red', '#', 'red', 'blue', '#', 'red' '#', 'blue']
'''
import re
def tokenize(T, css):
	#Use a regular expression to split the string into tokens or sequences of zero or more spaces.
	tokenString = '('
	#'\||\+|\-|\=|\"|\\|\}|\{|\[|\]|\?|\.|\<|\>|\/|\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\_|\;|\:|,|\(|\)' + ')'
	T = (re.escape(t) for t in T)
	for t in T:
		tokenString = tokenString + t + '|'
	tokenString = tokenString + '\s+)'
	#print("tokenString")
	#print(tokenString)
	newTokens = [t for t in re.split(tokenString,css)]

	#print("newTokens")
	#print(newTokens)
	return [b for b in newTokens if not b.isspace() and not b == ""]



#print(tokenize(["red", "blue", "#"], "red#red blue# red#blue"))
#print(tokenize(\
#               ["forward","reverse","left","right","turn","stop",";"],\
#               "forward; forward; forward; right turn; reverse; forward; stop;"\
#              ))

'''
 directions(tokenize(\
               ["forward","reverse","left","right","turn","stop",";"],\
               "forward; forward; forward; right turn; reverse; forward; stop;"\
              ))
{ "Forward": [
    { "Forward": [
        { "Forward": [
            { "RightTurn": [
                { "Reverse": [
                    { "Forward": ["Stop"]}
'''

def directions(tokens):

	if tokens[0] == 'forward' and tokens[1] == ';':
		(tokens) = directions(tokens[2:])
		return ({'Forward':[tokens]})
	
	if tokens[0] == 'reverse' and tokens[1] == ';':
		(tokens) = directions(tokens[2:])
		return ({'Reverse':[tokens]})
	
	if tokens[0] == 'left' and tokens[1] == 'turn' and tokens[2] == ';':
		(tokens) = directions(tokens[3:])
		return ({'LeftTurn':[tokens]})
	
	if tokens[0] == 'right' and tokens[1] == 'turn' and tokens[2] == ';':
		(tokens) = directions(tokens[3:])
		return ({'RightTurn':[tokens]})
		
	if tokens[0] == 'stop' and tokens[1] == ';':
		return ('Stop')
	
#print(directions(tokenize(\
#               ["forward","reverse","left","right","turn","stop",";"],\
#               "forward; forward; forward; right turn; reverse; forward; stop;"\
#              )))



'''
PROBLEM NUMBER 2 
VICTORY DANCE ONLY HOURS AWAY!
'''

def number(tokens, top):
	if re.match("^([1-9][0-9]*)", tokens[0]):
		#return ({"Number": [int(tokens[0])]}, tokens[1:])
		return (int(tokens[0]), tokens[1:])
#next if accounts for negatives		
	if re.match(r"^(-[1-9][0-9]*)$", tokens[0]): 
		return (int(tokens[0]), tokens[1:])

def numTest(e):
	if re.match("^([1-9][0-9]*)", e):
		e = int(e)
		return e
	return e
		
def variable(tokens, top):
	if re.match(r"^([a-zA-Z]+)$", tokens[0]):
		return ({'Variable':[str(tokens[0])]}, tokens[1:])

#print(variable(['123', 'foo', 'bar']))
#if it follows the language -> return tuple(abstract syntax, remaining unparsed suffix of input token sequence)
#a.s = the set of all data structure instances that correspond to a character string - LABELED "Variable"
		
def term(tokens):	
	return parse(tokens, True)	
'''	
#BLOCKING OFF OLD CODE TO USE THE PRIMARY PARSING METHOD FOR TERMS	
	if tokens[0] == 'log' and tokens[1] == '(':
		(e1, tokens) = term(tokens[2:]) #you use 2 here because your check analyses the first 2 tokens; therefore, we 'discard' the first 2
		if tokens[0] == ')':
			return ({'Log':[e1]}, tokens[1:])
			
	if tokens[0] == 'mult' and tokens[1] == '(':
		(e1, tokens) = term(tokens[2:])
		if tokens[0] == ',':
			(e2, tokens) = term(tokens[1:]) #the reason you use 1 here instead of 2 above is because the if statement checks for 1 token
			if tokens[0] == ')':
				return ({'Mult':[e1,e2]}, tokens[1:])
				
	if tokens[0] == 'plus' and tokens[1] == '(':
		(e1, tokens) = term(tokens[2:])
		if tokens[0] == ',':
			(e2, tokens) = term(tokens[1:]) #the reason you use 1 here instead of 2 above is because the if statement checks for 1 token
			if tokens[0] == ')':
				return ({'Plus':[e1,e2]}, tokens[1:])
	if tokens[0] == '@':
		return variable(tokens[1:])
	if tokens[0] == '#':
		return number(tokens[1:])
'''		
		
def formula(tokens): #true, false, not, and, or, equal, lessthan, greaterthan
	return parse(tokens, True)

''' BLOCK OUT THIS FOR OTHER METHOD, USE FORMULA AS HELPER METHOD TO CHAIN THINGS TO ACTUAL PARSE METHOD
	if tokens[0] == 'true':
		return ('True', tokens[1:])

	if tokens[0] == 'false':
		return ('False', tokens[1:])

	if tokens[0] == 'not' and tokens[1] == '(':
		(e1, tokens) = formula(tokens[2:])
		if tokens[0] == ')':
			return ({'Not':[e1]}, tokens[1:])

	if tokens[0] == 'or' and tokens[1] == '(':
		(e1, tokens) = formula(tokens[2:])
		if tokens[0] == ',':
			(e2, tokens) = formula(tokens[1:])
			if tokens[0] == ')':
				return ({'Or':[e1,e2]}, tokens[1:])

	if tokens[0] == 'and' and tokens[1] == '(':
		(e1, tokens) = formula(tokens[2:])
		if tokens[0] == ',':
			(e2, tokens) = formula(tokens[1:])
			if tokens[0] == ')':
				return ({'And':[e1,e2]}, tokens[1:])

	if tokens[0] == 'equal' and tokens[1] == '(':
		(e1, tokens) = term(tokens[2:])
		if tokens[0] == ',':
			(e2, tokens) = term(tokens[1:])
			if tokens[0] == ')':
				return ({'Equal':[e1,e2]}, tokens[1:])
				
	if tokens[0] == 'less' and tokens[1] == 'than' and tokens[2] == '(':
		(e1, tokens) = term(tokens[3:]) #use tokens 3 because the check knocks off first 3, see above for more detail
		if tokens[0] == ',':
			(e2, tokens) = term(tokens[1:]) #because we only took off the ',' token -> so we use 1
			if tokens[0] == ')':
				return ({'LessThan':[e1,e2]}, tokens[1:])	

	if tokens[0] == 'greater' and tokens[1] == 'than' and tokens[2] == '(':
		(e1, tokens) = term(tokens[3:]) 
		if tokens[0] == ',':
			(e2, tokens) = term(tokens[1:]) 
			if tokens[0] == ')':
				return ({'GreaterThan':[e1,e2]}, tokens[1:])	
'''

				
		
def program(tokens):	#print, assign, end
	return parse(tokens, True)

	#return leftFactor(tokens)
		
	'''
	if tokens[0] == 'end' and tokens[1] == ';':
		return 'End'			
		
	if tokens[0] == 'print':
		leftFactor(tokens[1], True)
		(e1, tokens) = formula(tokens[1:])
		if tokens[0] == ';':
			(e2, tokens) = program(tokens[1:])
			return ({'Print':[e1,e2]}, tokens[1:])
		#	redo this check for first case???
		#if term(tokens[1]) != None:
		#possibly do a program check here first, wait on piazza response
		#
		(e3, tokens) = term(tokens[1:])
		if tokens[0] == ';':
			(e4, tokens) = program(tokens[1:])
			return ({'Print':[e3,e4]}, tokens[1:])
		
	if tokens[0] == 'assign' and tokens[1] == '@':
		if term(tokens[3]) != None:
			tokens[2] = term(tokens[3])
			return ({'Assign':[tokens[2]] + '=' + term(tokens[3])}, tokens[4:])
		if program(tokens[3]) != None:
			tokens[2] = program(tokens[3])
			return ({'Assign':[tokens[2]] + '=' + program(tokens[3])}, tokens[4:])
	'''
	
'''
#left factor print
def leftFactor(tokens, top):
	r = parse(tokens[0:], top)
	
	if not r is None:
		(e1, tokens) = r
		if tokens[0] == ';':
			(e2, tokens) = parse(tokens[1:])
		return [e1,e2], tokens[2:]
'''
		
def complete(string):
	grammar = [':=','print', ';', 'assign','@','end','true',\
'false','not','and','or','(',')','equal','less than',\
'greater than','&&','||','==','<','>','plus',',','mult',\
'log','#','+','*', ' ', '']
	#print(tokenize(grammar, "print true ; end ;"))
	#print(tokenize(grammar, string))
	return parse(tokenize(grammar, string), True)
	
#I call the original program method rather than parseProgram just for my own personal coding convention
		
	

def parse(tmp, top):
	seqs = [\
		('True', ['true']), \
		#BNF NOTATION FOR EVERYTHING YOURE DOING - first entry is tuple, second is the list
		('False', ['false']), \
		#THESE TELL YOU WHAT TO RETURN
		('Not', ['not', '(', parse, ')']), \
		('And', ['and', '(', parse, ',', parse, ')']), \
		('And', ['(', parse, '&&', parse, ')']), \
		('Or', ['or', '(', parse, ',', parse, ')']), \
		('Or', ['(', parse, '||', parse, ')']), \
		('Equal', ['equal', '(', parse, ',', parse, ')']), \
		('Equal', ['(', parse, '==', parse, ')']), \
		('LessThan', ['less than', '(', parse, ',', parse, ')']), \
		('LessThan', ['(', parse, '<', parse, ')']), \
		('GreaterThan', ['greater than', '(', parse, ',', parse, ')']), \
		('GreaterThan', ['(', parse, '>', parse, ')']), 
		('Plus', ['plus', '(', parse, ',', parse, ')']), \
		('Plus', ['(', parse, '+', parse, ')']), \
		('Mult', ['mult', '(', parse, ',', parse, ')']), \
		('Mult', ['(', parse, '*', parse, ')']), \
		('Log', ['log', '(', parse, ')']), \
		('Number', ['#', number]), \
		('Variable', ['@', variable]), \
		('Print', ['print', parse, ';', parse]), \
		('Assign', ['assign', '@', variable, ':=', parse, ';', parse]), \
		('End', ['end', ';']) \
		]

	for (label, seq) in seqs:
	#ex: label = 'True' and seq = ['true']
		tokens = tmp[0:]
		#MAKE A COPY OF THE TOKENS BEFORE DOING ANYTHING - FOR BACKTRACKING
		ss = []
		#this keeps track of which tokens we are parsing
		es = []
		#this list keeps track of the subtrees we are parsing successfully
		for x in seq:
		#go through the sequence one by one - if the element x is a string
			#print('tokens[0] = ' + tokens[0])
			if type(x) == type(""):
				#print('x = ' + x)
				#print('tokens[0] = ' + tokens[0])
				if tokens[0] == x:
					tokens = tokens[1:]
					#print('tokens[0] = ' + tokens[0])
					#consume the first token
					ss = ss + [x]
					#just to keep track of it, put that consumed token into the ss list
				else:
					break
			else:
			#this else block says the current element x is a function (parse)
				#if tokens[0] == '#':
				#	tokens = tokens[1:]
				#print('tokens[0] == ' + tokens[0])
				r = x(tokens, False)
				#so this calls x on the rest of the token sequence, basically parses the rest
				if not r is None:
					(e, tokens) = r
					#this does the steps in my other code if the parse works (if it doesnt return none)				
					es = es + [e]
		if len(ss) + len(es) == len(seq):
		#this is a check to see if it worked in full by checking the length of the tokens by the length of the "children" collected up
			if not top or len(tokens) == 0:
			#does the normal 'am i at the top' check
				if label == 'Variable':
					return (es[0] if len(es) > 0 else label, tokens)
				else:
					return ({label:es} if len(es) > 0 else label, tokens)
				#return results as a dictionary with whatever the label was followed by results 
				#this checks if the number of children is > 0 and returns them if so otherwise it returns the other thing
				#the problem of checking something like program or program versus and, you have to cache to fix that, not required!
				#that problem being going through a big program to learn you had and instead of or, etc
	
#print(parse(['#', '-343'], True))			
#print(term(['log', '(', 'mult', '(', '#', '2', ',', '#', '3', ')', ')']))