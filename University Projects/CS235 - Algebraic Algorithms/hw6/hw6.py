'''
Created by Ben Blau - collaboration with Tyler Butler, and Alex Casella
May 2nd 2014
Professor Lapets CS235
Homework 6
Filename: hw6.py
exec(open("hw6.py").read())
'''

from math import floor
from fractions import gcd
from random import randint

'''
1a. 
12x ≡ 16 (mod 32)
Check: 12 and 32 are not coprime
gcd(12, 32) = 4

12x/4 = 16/4 (mod 32/4)
3x = 4 (mod 8)
3 * 3^-1 * x = 4 * 3^-1
Note: 3^-1 = 3^(8-2) = 729
x = 2916 (mod 8)
x = 4 (mod 8)


1b.
x ≡ 7 (mod 21)
x ≡ 21 (mod 49)
Check: 21 and 49 are not coprime
gcd(21, 49) = 7
r = a % g = 7 % 7 = 0

x/7 (- 0) = 1 (mod 3)
x/7 (- 0) = 3 (mod 7)

x = 1 * 7 * 7^-1 + 3 *3 * 3^-1 
Note: 7^-1 = 7^(3-2) = 7, 3^-1 = 3^(7-2) = 243
x = 2236 (mod 21*49/7)
x = 15652 (mod 147)
x = 70 (mod 147) 


1c. 
2x ≡ 12 (mod 26)
Check: 2 and 26 are not coprime
gcd(2, 26) = 2

x/2 = 12/2 (mod 13)
x = 6 (mod 13)


1d.
x ≡ 11 (mod 14)
x ≡ 18 (mod 21)
r = a % g = 4
Check: 14 and 21 are not coprime
gcd(14, 21) = 7
Subtract r from both sides
x-4/7 = 7 (mod 2)
x-4/7 = 14 (mod 3)

z = 7 (mod 2)
z = 14 (mod 3)

inverse 3 = 1
inverse 2 = 2
		21	+	56 = 77 mod 6 = 5 mod 6
z = 7*3*3^-1 + 14*2*2^-1 (mod 6)
z = 5 (mod 6)

x = 5 * 7 + 4 = 39 (mod 14*21/7)
x = 39 (mod 42) 


1e.
x ≡ 10 (mod 12)
x ≡ 2 (mod 16)
Check: 12 and 16 are not coprime
gcd (12, 16) = 4

r = a % g = 10 % 4 = 2

x-2/4 = 8 (mod 3)
x-2/4 = 0 (mod 4)

inverse 3 = 3
inverse 4 = 1

z = 8 (mod 3)
z = 0 (mod 4)

		32		+		0 = 32
z = 8 * 4 * 4^-1 + 0 * 3 * 3^-1 

x = 32 * 4 + 2 = 130 (mod 12 * 16 / 4) = 130 (mod 48)
x = 34 (mod 48)

1f.
x^2 = 4 (mod 35)
3 * x = 15 (mod 21)

x = 2 (mod 35)
x = 15 (mod 21)
g = gcd(35,21) = 7
a % g must = b % g --> 2 % 7 = 15 % 7 --> 2 = 1 is false, 2 != 1
CLOSURE TEST FAILED
No answer


2a.

x = 6 (mod 12)
x = 14 (mod 16)
g = gcd(12, 16) = 4
r = a % g = 6 % 4 = 2

x-2 = 4 (mod 12)
x-2 = 12 (mod 16)

(x-2)/4 = 4 (mod 3)
(x-2)/4 = 12 (mod 4)

z = 1 (mod 3)
z = 3 (mod 4)

inverse 3 = 3
inverse 4 = 1
		4		+		27	= 31  mod(3 * 4) = 31 mod 12
z = 1 * 4 * 4^-1 + 3 * 3 * 3^-1 

(x-2)/4 = 7

x = 7 * 4 + 2 (mod 12 * 16 / 4) = 30 (mod 48)
x = 30

30 Hours have passed since the alarm rang at midnight and it is 6AM.

2b.
x mod 256
x mod 16
256 * 16 = 4096
gcd(16,256) = 16
4096/16 = 256
Z/256Z

2c.
60/12 = 5 --> 4 12 machines, 1 machine doing 1 --> 49 total --> 11 to bob
60/15 = 4 --> 3 15 machines, 1 machine doing 7 --? 52 total --> 8 left to bob

8 problems for Bob

Part 2

x mod (0-19)
If Bob has x problems to solve, he can do x% any number between 1 and 19 to look for one
that results in no problems left over, that way he can have a certain number of machines 
all doing the same amount of work with no problems left over. This wouldn't work for prime numbers
of equations however.
'''


# Problem 3

def egcd(a, b):
	(x, s, y, t) = (0, 1, 1, 0)
	while b != 0:
		k = a // b
		(a, b) = (b, a % b)
		(x, s, y, t) = (s - k*x, x, t - k*y, y)
	return (s, t)

def inv(a, m):
	(s, t) = egcd(a, m)
	if (a * s + m * t == 1):
		return  s % m
	return None

def probablePrime(m):
	a = randint(2, m-1)
	if ((pow(a, (m-1), m) != 1) or (m/a == 0) or (gcd(a, m) != 1)):
		return False
	return True
	
def isCoprime(x, y):
	return gcd(x,y) == 1  

def findCoprime(m):

##This method uses the algorithm at "http://cs-people.bu.edu/lapets/235/m.php#e0ff1c992c6149df8a4c1f742bb55b00"

	L =[]
	for b in range(2, m-1):
		if isCoprime(b,m):
			for k in range(1, m.bit_length()):
				a = b**k
				L.append(a)
			c = closest(((4*m)//7), L)
			return c	
	
def makePrime(d):
	n = randint((10**(d-1)), (10**d) - 1)
	while not probablePrime(n):
		n = randint((10**(d-1)), (10**d) - 1)
	return n

'''	ORIGINAL
def solveOne(c, a, m):
	if (gcd(c,m) == 1):
		#return solution x in set(range(0, m-1)) to the equation c * x = a(mod m)
		invC = inv(c, m)
		x = a * invC
		x %= m
		return x
'''
#c * x = a (mod m)
def solveOne(c, a, m):	
	g = gcd(c,m)
	b = a
	a = c
	n = m
	#ALGORITHM VARIALBES, JUST REASSIGNING
	#closure check	
	if b % g != 0:
		return None
			
	nP = n//g	
	aP = a//g
	bP = b//g
	invAP = inv(aP, nP)
	
	x = invAP * bP
	x = x % nP
	
	return x
		


''' ORIGINAL
def solveTwo(e1, e2):
	#c * x = a (mod m)
	#d * x = b (mod n)
	(c, a, m) = e1
	(d, b, n) = e2
	if (gcd(n,m) != 1):
		return None
	if not (solveOne(c, a, m) != None and solveOne(d, b, n) != None):
		return None
	if (c != 1): #just a check to avoid doing this if unnecessary
		a = solveOne(c, a, m) #this turns the equation into x = (1, ?, m)
	if (d != 1):
		b = solveOne(d, b, n) #this step allows us to solve with the equation below
	invm = inv(m,n) #inv of m in congruence class n
	invn = inv(n,m) 
	x = ((a * n * invn) + (b * m * invm)) % (n * m)
	return x
'''

def solveTwo(e1, e2):
	#c * x = a (mod m)
	#d * x = b (mod n)
	(c, a, m) = e1
	(d, b, n) = e2

	G1 = gcd(c,m)
	G2 = gcd(d,n)
	NP = n//G2 #this NP and MP are the adjusted n and m each eq is solveOne 'd below
	MP = m//G1
	if solveOne(c, a, m) == None: #checking to see if both can be solved
		return None
	if solveOne(d, b, n) == None:
		return None
	if (c != 1): #just a check to avoid doing this if unnecessary
		a = solveOne(c, a, m) #this turns the equation into x = (1, ?, m)
	if (d != 1):
		b = solveOne(d, b, n) #this step allows us to solve with the equation below
	
	# x = a % MP
	# x = b % NP
	g = gcd(NP,MP)
	if (a % g == b % g): #another check to confirm that a solution exists

		nP = NP/g
		mP = MP/g
		r = a % g
		invNP = inv(nP, mP)
		invMP = inv(mP, nP)
		a = (a-r)/g
	
		b = (b-r)/g
	
		x = ((a * nP * invNP) + (b * mP * invMP)) % (nP * mP)

		x = (x * g + r) % ((n * m)/g)
		
		return x
		
		


	
''' ORIGINAL
def solveAll(es):
	if (len(es) == 1): #special case for list of size 1 (tuple)
		e1 = es[0]
		(c,a,m) = e1
		return solveOne(c, a, m)
	
	#c * x = a (mod m)
	
	while abs(len(es)) > 1:
		e1 = es.pop()
		e2 = es.pop()
		(c, a, m) = e1
		(d, b, n) = e2
		y = solveTwo(e1, e2)
		#we now have a new equation in form x = y (mod m*n)
		es.append((1, y, (m*n)))
	return y	
'''


def solveAll(es):
	if (len(es) == 1): #special case for list of size 1 (tuple)
		e1 = es[0]
		(c,a,m) = e1
		return solveOne(c, a, m)
	
	#c * x = a (mod m)
	
	while abs(len(es)) > 1:
		e1 = es.pop()
		e2 = es.pop()
		(c, a, m) = e1
		(d, b, n) = e2
		NP = n / gcd(d,n)
		MP = m / gcd(c,m)
		y = solveTwo(e1, e2)
		#we now have a new equation in form x = y (mod m*n)
		es.append((1, y, (MP*NP)/gcd(NP,MP)))
	return y	
	



	