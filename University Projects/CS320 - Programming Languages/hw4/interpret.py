#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#
#Ben Blau (bblau94@bu.edu)
#November -- 2014


exec(open("parse.py").read())


def subst(s, a):
	if type(a) == Node:
		for label in a:
			children = a[label]
			if label == 'Variable':
				if children[0] in s:
					return s[children[0]]							
			elif label != 'Variable':
				for i in range(len(children)):
					children[i] = subst(s, children[i])					
	return a


	

#print(subst({"x":{"Number":[5]}}, {"Variable":['x']}))
#print(subst([], {"Variable":['x']}))
#print(subst({"y":{"Number":[2]}}, {"Plus":[{"Variable":['y']}, {"Variable":['y']}]}))
#print(subst({"a":{"Number":[1]}, "b":{"Number":[2]}}, {"Mult":[{"Variable":['y']}, {"Variable":['y']}]}))
#print(subst({"a":{"Number":[1]}, "b":{"Number":[2]}}, {"Mult":[{"Plus":[{"Variable":['y']}, {"Variable":['y']}]}, {"Variable":['b']}]}))
#print(subst({"z":{"Number":[2]}}, {"Plus":[{"Variable":['y']}, {"Variable":['z']}]}))
#print(subst({"z":{"Variable":['y']}, "y":{"Number":[3]}, "b":{"Variable":['a']}, "a":{"Variable":['z']}}, {"Plus":[{"Variable":['y']}, {"Variable":['b']}]}))
#^ That test case is apparently not something that needs to be done**
def unify(a, b):
	substitution = {}
	if a == None or b == None:
		return None
	
	if type(a) == Leaf and type(b) == Leaf:
		if a == b:
		#	print('CASE 1')
			return {}
		else: return None
	
	for labelA in a:
		for labelB in b:
			childrenA = a[labelA]
			childrenB = b[labelB]
			if labelA == 'Variable':
			#	print("CASE 2")
				x = a['Variable'][0]
				#if the variables are the same, return None. Only need this in the first check because
				#in the next case for labelB == 'Variable' if they were both variable it would have
				#been picked up here.
				if labelB == 'Variable' and childrenB[0] == x:
					return None
				substitution[x] = b
				return substitution
			elif labelB == 'Variable':
			#	print("CASE 3")
				x = b['Variable'][0]
				substitution[x] = a
				return substitution	
			elif labelA == labelB and len(childrenA) == len(childrenB):
				for i in range(len(childrenA)):
				#	print('Case 4 Test: ' + str(i))			
					#Integer Case
					#If A is an integer and B is an integer
					if type(childrenA[i]) == int and type(childrenB[i]) == int:
						#print("Test Case: A and B are ints")
						#A and B must equal each other if both are ints otherwise return None
						if childrenA[i] == childrenB[i]:
							return substitution	
						else: return None
					#if not dealing with integers, continue unification process
					uni = unify(childrenA[i], childrenB[i])
					if not uni is None:
						substitution.update(uni)
					else: return None
				return substitution
			
		

#If we have f(0) = 0 and f(n) = f(n-1) + 1. We will build M as: M = {‘f’ : [(0,0), (n, (n-1) + 1)} 
#FOR FUNCTION MORE:
#F is already in the domain of M1 (it is already a key in the dictionary) then 
#I will take M1 and add to it a new definition for f where f maps to all of the
#old stuff under key f plus the new pair of stuff (p,e). In python we just append,
#or add to the dictionary, etc, this is doing the same thing, extend with the additional pair (p,e).
#Then what we get back is a new data structure M2 from this entire process.

def build(m, d):
	#d --> f(p) = e;d
	#('Function', ['variable', '(', 'pattern' , ')', '=', 'expression', ';', 'declaration']),\
	if type(d) == Leaf:
		if d == 'End':
			return m
			
	if type(d) == Node:
		for label in d:
			if label == 'Function':
				[v, p, e, d1] = d[label]
				f = v['Variable'][0]
				#Function-First
				if f not in m:
					m[f] = [(p,e)]
					M2 = build(m, d1)
					return M2
				#Function-More
				else:
					m[f] += [(p,e)]
					M2 = build(m, d1)
					return M2

					
def interact(s):
	# Build the module definition.
	m = build({}, parser(grammar, 'declaration')(s))

	# Interactive loop.
	while True:
		# Prompt the user for a query.
		s = input('> ') 
		if s == ':quit':
			break
        
		# Parse and evaluate the query.
		e = parser(grammar, 'expression')(s)
		if not e is None:
			print(evaluate(m, {}, e))
		else:
			print("Unknown input.")


def evaluate(m, env, e):
	if type(e) == Node:
		for label in e:
			children = e[label]
			if label == 'Number':
				return children[0]
			elif label == 'Variable':	
				x = children[0]
				if x in env:
					return env[x]
				else:
					print(x + " is unbound.")
					return None
					#exit() #can toggle for desired effect
			elif label == 'Plus':
				e2 = children[1]
				n2 = evaluate(m, env, e2)
				e1 = children[0]
				n1 = evaluate(m, env, e1)
				return n1 + n2
	
			elif label == 'ConInd':
				c = children[0]
				e1 = children[1]
				e2 = children[2]
				v1 = evaluate(m, env, e1)
				v2 = evaluate(m, env, e2)
				return {'ConInd': [c,v1,v2]}
			elif label == 'ConBase':
				return e
			elif label == 'Apply':
				[f, eArg] = children
				f = f['Variable'][0]
				if f in m:
					v1 = evaluate(m, env, eArg) #this is the x in f(x)
					for i in range(len(m[f])):
						[p, e2] = m[f][i]
						unified = unify(p, v1)
						if not unified is None:
							env.update(unified)
							v2 = evaluate(m, env, e2)
							return v2
				else:
					print(f + " is unbound.")
					return None
					#exit() #can toggle for desired effect
		
	print("Something in evaluate went wrong! (Or a variable is unbound)")

#small testing function aside from interact
def testEval():
	#This test: input "x(Leaf)" for the function(list): "x(Leaf) = y(False); y(True) = False; y(False) = True;"
	#run with evaluate
	#return evaluate(build({}, parser(grammar, 'declaration')("x(Leaf) = y(False); y(True) = False; y(False) = True;")), {}, parser(grammar, 'expression')("x(Leaf)"))
	#return evaluate(build({}, parser(grammar, 'declaration')("x(Leaf) = y(False); y(True) = False; y(False) = True;")), {}, parser(grammar, 'expression')("x(Leaf)"))
	#return evaluate(build({}, parser(grammar, 'declaration')(" y(True) = False;y(False) = True;")), {}, parser(grammar, 'expression')("y(False)"))
	#return evaluate(build({}, parser(grammar, 'declaration')("y(True) = False; y(False) = True; ")), {}, parser(grammar, 'expression')("y(False)"))
	#print(evaluate(build({}, parser(grammar, 'declaration')("new(Node t1 t2) = NewNode new(t1) new(t2); new(Leaf) = NewLeaf;")), {}, parser(grammar, 'expression')("new(Node Leaf Leaf)")))
	# y(True) = False;y(False) = True; FOR LAST LINE


#Excess code below- Not necessary for the assignment----------------------------------			
'''
#This version of build gets rid of labels: would just return something like "Node t1 t2" instead of ConBase t1, etc			
def build(m, d):
	M1 = {}
	#d --> f(p) = e;d
	#('Function', ['variable', '(', 'pattern' , ')', '=', 'expression', ';', 'declaration']),\
	if type(d) == Leaf:
		if d == 'End':
			return m
			
	if type(d) == Node:
		for label in d:
			if label == 'Function':
				[v, p, e, d1] = d[label]
				f = v['Variable'][0]
				newP = ""
				newE = ""
				#This for loop unpacks p so that things such as "Node, Var...t1, Var...t2"
				#come back as "Node, t1, t2"
				whiteSpaceCountP = 1
				whiteSpaceCountE = 1
				for labelP in p:
					for labelInterior in p[labelP]:
						if type(labelInterior) != Leaf and type(labelInterior) != int:
							for labelInLabel in labelInterior:
								newP += labelInterior[labelInLabel][0]
						else:
							newP += labelInterior
							
						#this adds a space between every object in the argument BUT not after the last one
						if whiteSpaceCountP < len(p[labelP]):
							newP += " "
							whiteSpaceCountP += 1
					
				for labelE in e:
					for labelInteriorE in e[labelE]:
						if type(labelInteriorE) != Leaf and type(labelInteriorE) != int:
							for labelInLabelE in labelInteriorE:
								newE += labelInteriorE[labelInLabelE][0]
						else:
							newE += labelInteriorE
						
						if whiteSpaceCountE < len(e[labelE]):
							newE += " "
							whiteSpaceCountE += 1					
				#Function-First
				if f not in m:
					m[f] = [(newP,newE)]
					M2 = build(m, d1)
					return M2
				#Function-More
				else:
					m[f] += [(newP,newE)]
					M2 = build(m, d1)
					return M2			
'''



	
#eof