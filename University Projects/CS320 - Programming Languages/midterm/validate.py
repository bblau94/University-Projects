#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# validate.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
# Ben Blau U94434268
# Due: October 29th 2014


exec(open('interpret.py').read())
exec(open('compile.py').read())
exec(open('optimize.py').read())


#exec(open('analyze.py').read())
Node = dict
Leaf = str
#uncomment analyze.py or run prior to validate.py to include type checking

#############################
#		INSTRUCTIONS		#
#							#
#	Run testAllDefaults(n)	#
# this will add the default	#
# as you did and will also	#
# take care of illegal		#
#	cases by type checking	#
#							#
#############################

#Note - For was commented out since we cannot test for in compileProgram since we did not write
#a for compile. It can be turned on and added in for intentions of testing in compileAndSimulate


######################File Start######################
def expressions(n):
	if n <= 0:
		[]
	#elif n == 1:
	else:
		bc = [{'Number':[2]}] + ['True', 'False'] + [{'Array':[{'Variable':['a']}, {'Number':[2]}]}]
		return bc # Add base case(s) for Problem #5.
	#else:
	#	es = expressions(n-1)
	#	esN = []
	#	esN += [{'Array':[{'Variable':['a']}, {'Number':[2]}]}]
	#	return es + esN
		#	pass # Add recursive case(s) for Problem #5.

	
def metric(f):
	if type(f) == Leaf:
		return 1
	if type(f) == Node:
		for label in f:
			return 1 + max([metric(child) for child in f[label]])	


#Used only for testing. Returns the size of a list of programs psN
def pCount(psN):
	i = 0
	for p in psN:
		i = i + 1
	print(i)	

#Used only for testing. Generates a type-checked list of programs of size n	
def pList(n):
	for i in programs(n):
		typeP = typeProgram({}, i)
		if typeP == 'Void':
			print(i)

#Used only for testing. Prints appropriately type-checked programs in program list p			
def progList(p):
	for i in p:
		typeP = typeProgram({}, i)
		if typeP == 'Void':
			print(i)
			
def programs(n):
	if n <= 0:
		[]
	elif n == 1:
		return ['End']
	else:
		ps = programs(n-1)
		es = expressions(n-1)
		psN = []
		psN += [{'Print':[e, p]} for e in es for p in ps]
		psN += [{'Assign':[{'Variable':['a']}, e, e, e, p]} for p in ps for e in es]		
		psN += [{'For':[{'Variable':['i']}, p, p]} for p in ps]		
	
		
		return ps + psN

# We always add a default assignment to the program in case
# there are variables in the parse tree returned from programs().

def defaultAssigns(p):
	return \
		{'Assign':[\
		{'Variable':['a']}, {'Number':[2]}, {'Number':[2]}, {'Number':[2]}, p\
		]}

# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most 4.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.


#Used for testing only. Tests program list of size n in compileProgram within compile.py
def testCompile(n):
	count = 0
	ps = programs(n)
	for p in ps:
		if typeProgram({}, p) == 'Void':
			#print(p)
			test = compileProgram({}, unrollLoops(p), 7)
			if not test is None:
				
				(env, insts, heap) = test
				count += 1
				simulate(insts)
				#print(simulate(insts))
			#print(test)	
	print("Total compiled programs: " + str(count))

#Used for testing only. Tests program list of size n in execute within interpret.py		
def testInterpret(n):
	for p in programs(n):
		#print(p)
		test = execute({}, p)
		#print(test)
		#print()	

#TestAll does the same thing as testAllDefaults without adding the default assign in front of the programs.		
def testAll(n):
	ps = programs(n)
	passCounter = 0
	failCounter = 0
	for p in ps:
		typeP = typeProgram({}, p)
		if typeP == 'Void':
			compile = simulate(compileProgram({}, p)[1])
			interpret = execute({}, p)[1]
			if compile == interpret:
				passCounter += 1
				#print('PASS!')
				#print(p)
				#print(interpret)
			else:
				print('Failed on:\n')
				print(p)
				failCounter += 1
				#break
	print(str(failCounter) + " tests failed and " + str(passCounter) + " tests passed")
	
	
#This tests a program list of size n in both compile and interpret and then compares the two
#If the test passes it will increment the passCounter and vice versa with failCounter.
#It is defaulted to also print out the case which fails. It can be changed to print('PASS')
#at every event of a pass and it can also be changed (break) to stop upon encountering a
# failure. At the end it will print out the number of failed and passed tests.
def testAllDefaults(n):
	ps = programs(n)
	passCounter = 0
	failCounter = 0
	for p in [defaultAssigns(p) for p in ps]:
		typeP = typeProgram({}, p)
		if typeP == 'Void':
			#print(p)
			compile = simulate(compileProgram({}, unrollLoops(p))[1])
			#compile = simulate(compileProgram({}, foldConstants(unrollLoops(p)))[1]) #can use this if you want to optimize even more
			interpret = execute({}, p)[1]
			if compile == interpret:
				passCounter += 1
				#print('PASS!')
				#print(p)
			else:
				print('Failed on:\n')
				print(p)
				failCounter += 1
				#break
	print(str(failCounter) + " tests failed and " + str(passCounter) + " tests passed")


	
#Used for testing only. 
#I used this to test specific cases that I made in both interpret and compile
#NOTE this function only works for proper syntax because I only wanted to test cases that should work with this one.
#Interpret does not type check!
def testTop(s):
	i = interpret(s)
	c = compileAndSimulate(s)
	#print(i)
	#print(c)
	if i == c:
		print("Pass")
	elif not i is None:
		print("Improper Grammar or Type Error")
	else:
		print("Fail")
		print(i)
		print(c)

#Used for testing only. Used to feed in a list of test cases into testTop
def testTopList(L):
	for s in L:
		testTop(s)

'''
L = []
L += ["print 3 + 3;"]
L += ["print 3 + -1000;"]
L += ["print -1000;"]
L += ["print 0;"]
L += ["print -1;"]
L += ["print 1;"]
L += ["print 3 + 3 + 10 + 100 + -50;"]
L += ["for x { print -10000;} print -10000 + 1000;"]
L += ["for x { print 10000;} print 10000 + 1000;"]
L += ["for x { assign x:= [7,11,35];} print @x[0];print @x[1];print @x[2];print @x[0] + @x[0];"]
#L += ["print true + 3;"] #returns appropriate error
L += ["assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2];"]
L += ["assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2]; for x {print 30;}print20; "]
L += ["assign x:= [7,11,35];assign y:= [71,121,355]; print @x[0];print @x[1];print @x[2]; for x {print @y[2];}print20; "]
L += ["assign x:= [7,11,35]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0];print @x[1];print @x[2];assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0] + 15;print @x[1] + 6 + -50;print @x[2];"]
L += ["assign x:= [1 + 5 + 123,11 + -100,3  + 5]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0];print @x[1];print @x[2];assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0] + 15;print @x[1] + 6 + -50;print @x[2];"]
L += ["assign x:= [1 + 5 + 123,11 + 100,3  + 5]; print @x[0];print @x[1];print @x[2]; assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0];print @x[1];print @x[2];assign x:= [@x[0] + @x[0], @x[1] + @x[1], @x[2] + @x[2]]; print @x[0] + 15;print @x[1] + 6 + -5;print @x[2] + @x[1]; for y { print @x[0] + -5 + 10 + @x[1]; } print @x[1];"]

testTopList(L)	
'''

#Running the default code below gave me an error that acted as if the actual "type()" function itself
#was being changed. The first time I would run it I would get through the first test before encountering
#some error that resulted from type() not longer working. The second time I would run it I would not even
#get through that first case as if the code I wrote had been altered between the first and second time
#I ran validate.py which it was not. This could have been an error resulting from an incomplete validate
#because I had not implemented array as a base case at the time; however, this doesn't seem like it would
#effect the program in such a way. I have not tested since the issue, it is possible it works correctly now
#but I wrote my own testing function that works pretty much exactly the same so I just left this out.	

#EDIT: This now works. I am aware of the problem. Type was being renamed in the type check below. (type =...)
#Dumb mistake. This will work if you want to run it to check too.
#Default value is set to 4. Works for higher numbers. Counter added to keep track of correct cases.
'''
totalProgramsHere = 0
for p in [defaultAssigns(p) for p in programs(5)]:
	typeP = typeProgram({}, p)
	if typeP == 'Void':
		try:
			if simulate(compileProgram({}, p)[1]) != execute({}, p)[1]:
				print('\nIncorrect behavior on: ' + str(p))
			else:
				totalProgramsHere += 1
		except:
			print('\nError on: ' + str(p))
print(totalProgramsHere)
'''
#eof