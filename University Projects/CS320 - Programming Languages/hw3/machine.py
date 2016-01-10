'''
Created by Ben Blau: bblau94@bu.edu
October 14th 2014
Professor Lapets CS320
Homework 3 machine
Filename: machine.py
Collab with Tyler Butler
'''

from random import randint

def freshStr():
	return str(randint(0,100000))


def simulate(s):
	instructions = s if type(s) == list else s.split("\n")
	instructions = [l.strip().split(" ") for l in instructions]
	mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
	control = 0
	outputs = []
	while control < len(instructions):
		# Update the memory address for control.
		mem[6] = control 
		
		# Retrieve the current instruction.
		inst = instructions[control]
		
		#print(inst)
		
		# Handle the instruction.
		if inst[0] == 'label':
			pass
		if inst[0] == 'goto':
			control = instructions.index(['label', inst[1]])
			continue
		if inst[0] == 'branch' and mem[int(inst[2])]:
			control = instructions.index(['label', inst[1]])
			continue
		if inst[0] == 'jump':
			control = mem[int(inst[1])]
			continue
		if inst[0] == 'set':
			mem[int(inst[1])] = int(inst[2])
		if inst[0] == 'copy':
			mem[mem[4]] = mem[mem[3]]
		if inst[0] == 'add':
			mem[0] = mem[1] + mem[2]
	
		# Push the output address's content to the output.
		if mem[5] > -1:
			outputs.append(mem[5])
			mem[5] = -1

		# Move control to the next instruction.
		control = control + 1

	print("memory: "+str(mem))
	return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to): #whatever is in address frm will be moved into the addr location of to
	return [\
		'set 3 ' + str(frm),\
		'set 4 ' + str(to),\
		'copy'\
	]
	
def resetAdd():
	return [\
		'set 0 0',\
		'set 1 0',\
		'set 2 0'\
	]


def resetCopy():
	return [\
		'set 3 0',\
		'set 4 0'\
	]
	
def resetAll():	
	return resetAdd()\
	+resetCopy()\

#incrementing/decrementing multiple times	
def incrementMult(addr, num):
	return copy(addr, 1) \
	+[\
	'set 2 ' + str(num), \
	'add' \
	] \
	+copy(0, addr) \
	+resetAll()\
	
	
def incrementAddressWithinBy(inFrm , num):
	return[\
	'set 3 ' + str(inFrm),\
	'set 4 3',\
	'copy',\
	'set 4 1',\
	'copy',\
	'set 2 ' + str(num),\
	'add',\
	]\
	+copyTo(0, 7)\
	+resetAll()\
	
	
def decrementMult(addr, num):
	return copy(addr, 1) \
	+[\
	'set 2 ' + str(num), \
	'add' \
	] \
	+copy(0, addr) \
	+resetAll()\

#copy from a the address contained in a (inFrom) - as in within from to b - to
#if inFrm contains address 31 but address 31 contains address 77, then this moves 77 into the 'to'	
#if a = 31 and mem[31] = 77 and we want b = 77
def copyAddressWithinTo(inFrm , to):
	return[\
	'set 3 ' + str(inFrm),\
	'set 4 3',\
	'copy',\
	'set 4 ' + str(to),\
	'copy'\
	]

	#copy address 15 within frm 
	#mem[a] = 77 mem[b] = 31, make mem[31] = 77
	#copy(a,b) makes mem[b] = mem[mem[a]]
	#set 3 a    set 4 b     it takes what is within 3 and puts it into mem[4]
	#mem[mem[4]] = mem[mem[3]]
def copyTo(a, b):
	return [\
	'set 3 ' + str(b),\
	'set 4 4',\
	'copy',\
	'set 3 ' + str(a),\
	'copy'\
	]
'''	
#this test shows copyTo works, mem[10] = 77, mem[15] = 31, product is mem[31] = 77
y = [\
'set 10 77',\
'set 15 31',\
'set 3 15',\
'set 4 4',\
'copy',\
'set 3 10',\
'copy'\
]\	

print(simulate(y))	
#this is for copyAddressWithinTo. mem[10] = 31, mem[31] = 77, mem[15] = 0 intially, prodcut is mem[15] = 77 
z = [\
'set 10 31',\
'set 31 77',\
'set 15 0',\
'set 3 10',\
'set 4 3',\
'copy',\
'set 4 15',\
'copy'\
]\

print(simulate(z))
'''	
	
def increment(addr):
	return copy(addr, 1) \
	+[\
	'set 2 ' + str(1), \
	'add' \
	] \
	+copy(0, addr) \
	+resetAll()\

def decrement(addr):
	return copy(addr, 1)\
	+[\
	'set 2 ' + str(-1),\
	'add'\
	]\
	+copy(0, addr)\
	+resetAll()\
	
	
#set 7 to 0
#decrement 5 so it now points to -2 (the next spot on the stack below the first location)
#copy(6,-1) so the current program location is now in mem[-1] (top of the stack)
#increment(5) increments the value at the tpo of the stack
#copy(6,7) puts the current location of the program, before the name call, into 7 for later use in procedure
#goto name
#increment(5) to update the integer stored at the top of the stack
#copy(-1,5) to move whatever is at the top of the stack into 5 so it will be added to outputs
# SHOULD I REMOVE INCREMENT(5)? DOES ^ DO WHAT I NEED? IT PRINTS THE OUTPUT BY ITSLEF, SEEMS RIGHT?
#I DELETED INCREMENT(5) that was after copy(-1,5)

'''
return [\
	'set 7 -1'\
	]\
	+decrement(7)\
	+copyTo(6, 7)\
	#takes what is in 6 and has what is in 7 point to it
	#7 points to -2, now -2 points to program
	#increment program (what is in -2)
	#7 -> -2 -> program . Move program to top of the call stack
	+copyAddressWithinTo(7, -1)\
	#now mem[-1] = current program location
	#increment the value at the top of the call stack (program) to point to after name
	+increment(-1)
	+[\
	'goto ' + name\
	]\
	+increment(7)\

	return decrement(7)\
	+copyTo(6, 7)\
	+incrementMult(-1, 15)\
	+[\
	'goto ' + name\
	]\
	+increment(7)\
	
	
	
	+incrementAddressWithinBy(7, 9)\
'''

def call(name):
	return decrement(7)\
	+copyTo(6, 7)\
	+[\
	'goto ' + name\
	]\
	+increment(7)\
	

def jumpWithin(n):
	return copyAddressWithinTo(n,0)\
	+['jump 0'\
	]
	
	
#increment 7 here since 7 records the location before the call to name was made
#increment it to point to after the call. If I increment 3-5 times it prints 1 but that's not what I want..
#does it work for 3 4 and 5 because 7 is set to 6 but copy increments 6 3 times (3 commands) afterwards?
#now I added copy(10,5) to move my 15 from set 10 15 to 5 so it will be put into the output
#how can I make this universal...
def procedure(name, body):
	fresh = freshStr()
	return [\
	'goto bodyEnd' + fresh + name,\
	'label ' + name\
	]\
	+body\
	+incrementAddressWithinBy(7, 2)\
	+jumpWithin(7)\
	+[\
	'label bodyEnd' + fresh + name\
	]

	

	
#r = call('test')
#print(r)

#v = [\
#'set 10 15',\
#'set 11 15',\
#'set 12 17'\
#]
#p = procedure('test', v)
#print(p)
#print(r + p)
#print(simulate(p + r))

	
	
