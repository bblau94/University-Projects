#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# parse.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
# exec(open("parse.py").read())
# Benjamin Blau U94434268
# Due: October 29th 2014

import re

def number(tokens, top = True):
	try:
		if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
			return ({"Number": [int(tokens[0])]}, tokens[1:])
	except:
		return None
	
def variable(tokens, top = True):
	if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
		return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tmp, top = True):
	tokens = tmp[0:]
	r = leftExpression(tokens, False)
	if not r is None:
		(e1, tokens) = r
		if len(tokens) > 0 and tokens[0] == '+':
			r = expression(tokens[1:], False)
			if not r is None:
				(e2, tokens) = r
				return ({'Plus':[e1,e2]}, tokens)
			else:
				return None
		else:
			return (e1, tokens)



def leftExpression(tmp, top = True):
	r = parse([\
		('True', ['true']),\
		('False', ['false']),\
		('Array',  ['@', variable, '[', expression, ']']),\
		], tmp, top)
	if not r is None:
		return r
		
	tokens = tmp[0:]
	r = variable(tokens, False)
	if not r is None:
		return r
		
	tokens = tmp[0:]
	r = number(tokens, False)
	if not r is None:
		return r
	
	

def program(tmp, top = True):
	if len(tmp) == 0:
		return ('End', [])
	r = parse([\
		('Assign',  ['assign', variable, ':=', '[', expression, ',', expression, ',', expression, ']', ';', program]),\
		('Print', ['print', expression, ';', program]),\
		('For',  ['for', variable, '{', program, '}', program]),\
		('End', [])
		], tmp, top)
		
	if not r is None:
		return r	
	if r is None:
		return None

def parse(seqs, tmp, top = True):
	for (label, seq) in seqs:
		tokens = tmp[0:]
		(ss, es) = ([], [])
		for x in seq:
			if type(x) == type(""):
				if tokens[0] == x:
					tokens = tokens[1:]
					ss = ss + [x]
				else: break
			else:
				
				r = x(tokens, False)
				if not r is None:
					(e, tokens) = r
					es = es + [e]
		if len(ss) + len(es) == len(seq) and (not top or len(tokens) == 0):
			return ({label:es} if len(es) > 0 else label, tokens)		

			
			
#NOTE!!! ****************************************
#I have structured my program so that if we are not allowed to catch exceptions
#please just delete the try and catch and everything should still run fine!	
#but also note that the print() and return None past except should be left in
#after the if statement in the case that it fails. For this homework I returned None
#instead of using break. This was just to help me have everything in interpret catch the None
#and respond accordingly.
def tokenizeAndParse(s):
	try:
		tokens = re.split(r"(\s+|assign|:=|for|@|\[|\]|,|print|\+|{|}|;|true|false|)", s)
		tokens = [t for t in tokens if not t.isspace() and not t == ""]
		if program(tokens) is not None:
			(p, tokens) = program(tokens)
			return p
	except:
		print('Given string does not conform to language. Returning None:')
		return None

	
####TESTS####	
#L = []
#L.append("print x ;")
#L.append("print 3 + 3 ;")
#L.append("print x + x ;")
#L.append("print x + z ;")
#L.append("print x + 3 ;")
#L.append("print 3 + x ;")
#L.append("print 3 + x ; print true;")
#L.append("print false ; print true;")
#L.append("for x { print true ; }")
#L.append("for x { print -15 + 0 ; }")
#L.append("for x { print true ; } print false;")
#L.append("for x { print @ x [ 3 + 3 ] ; } print false;")
#L.append("for x { print @ x [ true ] ; } print false;")
#L.append("print @ x [ true ] ;  ")
#L.append("assign a := [1+2,4,6];")
#L.append("assign 5 := [1+2,4,6];")
#L.append("print 3;")

#for i in L:
#	print(tokenizeAndParse(i))	

#eof