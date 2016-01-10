#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# analyze.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
# Ben Blau U94434268
# Due: October 29th 2014

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
	if type(e) == Leaf:
		if e == 'True' or e == 'False':
			return 'Boolean'
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == 'Number':
				return 'Number'

			elif label == 'Variable':
				x = children[0]
				if x in env:
					return env[x]
				else:
					print("Variable '" + x + "' not in Environment")
					return None 
					
			elif label == 'Array':
				[x, e] = children
				x = x['Variable'][0]
				if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
					return 'Number'
				else: return None
					
			elif label == 'Plus':
				[e1, e2] = children
				e1T = typeExpression(env, e1)
				e2T = typeExpression(env,e2)
				if e1T != 'Number' or e2T != 'Number':
					return None
				return 'Number'
				
				
def typeProgram(env, s):
	if type(s) == Leaf:
		if s == 'End':
			return 'Void'
	elif type(s) == Node:
		for label in s:
			if label == 'Print':
				[e, p] = s[label]
				eT = typeExpression(env, e)
				eP = typeProgram(env, p)
				if (eT == 'Boolean' or eT == 'Number') and\
					eP == 'Void':
					return 'Void'
				else: return None
				
			elif label == 'Assign':
				[x, e0, e1, e2, p] = s[label]
				x = x['Variable'][0]
				e0T = typeExpression(env, e0)
				e1T = typeExpression(env, e1)
				e2T = typeExpression(env, e2)

				if e0T == 'Number' and e1T == 'Number' and e2T == 'Number':
					env[x] = 'Array'
					eP = typeProgram(env, p)			
					if eP == 'Void':
						return 'Void'
					else: return None
				else: return None
												
			elif label == 'For':
				[x, p1, p2] = s[label]
				x = x['Variable'][0]
				eP1 = typeProgram(env, p1)
				eP2 = typeProgram(env, p2)
				if eP1 == 'Void':
					env[x] = 'Number'
					if eP2 == 'Void':
						env[x] = 'Number'
						return 'Void'
					else: return None
				else : return None
	
#eof