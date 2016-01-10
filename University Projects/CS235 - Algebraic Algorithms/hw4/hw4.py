'''
Created by Ben Blau - collaboration with Tyler Butler, Andrew Filippi, and Alex Casella
March 31st 2014
Professor Lapets CS235
Homework 4
Filename: hw4.py
'''
from math import floor
from fractions import gcd
from random import randint


'''
#1

1a)
x^2 ≡ 3 (mod 23)
x = 3^((23+1)/4) (mod 23)
x = 3^6 = 729 (mod 23)
x = 16
x = 23 - 16 = 7

x = 16, 7


1b)
x^2 ≡ 25 (mod 41)
x = 5
x = 41 - 5 = 36

x = 5, 36


1c)
x^2 ≡ 1 (mod 55)

x^2 = 1 (mod 11)
x^2 = 1 (mod 5)

x = 1 (mod 11)
x = 10 (mod 11)
x = 1 (mod 5)
x = 4 (mod 5)

x1 = 1 (mod 11)
x1 = 1 (mod 5)
x1 = 1 (mod 55)

x2 = 10 (mod 11)
x2 = 1 (mod 5)
x2 = 10 * 5 * 5^-1 + 1 * 11* 11^-1 (mod 55)
x2 = 10 * 5 * 9 + 1 * 11 * 1 (mod 55)
x2 = 461 (mod 55) = 21 (mod 55)

x3 = 1 (mod 11)
x3 = 4 (mod 5)
x3 = 1 * 5 * 5^-1 + 4 * 11 * 11^-1 (mod 55)
x3 = 45 + 44 (mod 55)
x3 = 89 (mod 55) = 34 (mod 55)

x4 = 10 (mod 11)
x4 = 4 (mod 5)
x4 = 10 * 5 * 5^-1 + 4 * 11 * 11^-1 (mod 55)
x4 = 54 (mod 55)

x = 1, 21, 34, 54


1d)
x^2 ≡ 8 (mod 49)
x^2 = 8 (mod 7)
x^2 = 8 (mod 7)

x = 8^((7 + 1)/4) (mod 7)
x = 64 (mod 7)
x = 1, -1

Using Hensel's Lemma:
c = 1^-1 * 2^-1 * ((8-1)/7)(mod 7))
c = 1 * 4 * 1
c = 4

x = 1 + 4 * 7 (mod 49)
x = 29
x = 49 - 29 = 20

x = 29, 20


1e)
(8 * x^2) + 4 ≡	6 (mod 21)
(8 * x^2) = 2 (mod 21)

(8 * x^2) = 2 (mod 21)
x^2 = 2 * (8^-1) (mod 21)

Note: 8^-1 = 8^ (phi(21)-1)
           = 8^ (phi(7) * phi(3) - 1)
           =8 ^ (6*2 - 1)
           = 8^11

x^2 = 2*8^11 (mod 21)
x^2 = 16 (mod 21)

x^2 = 16 (mod 7) = 2 (mod 7)
x^2 = 16 (mod 3) = 1 (mod 3)

x^2 = 2(mod 7)
x = 3 mod 7  [3,10,17]
x = 4 mod 7  [4,11,18]

x^2 = 1 (mod 3) = 1^2 mod(3)
x = 2 mod 3  [2,5,8,11,14,17]
x = 1 mod 3  [1,4,7,10,13,16,19]

x = 17 (mod 21)
x = 10 (mod 21)
x = 11 (mod 21)
x = 4 (mod 21)

x = 17, 10, 11, 4


'''

#2

def factorsFromPhi(n, phi_n):
	
	x = n - phi_n + 1 
	z = .5 * (x + pow(pow(x,2) - 4*n, .5))
	p = x - z
	return (p, n/p)

def factorsFromRoots(n, x, y):
	#if (pow(x,2) == pow(y,2,n)) and (x != y % n) and (x != (-y) % n):
		if gcd(n, x + y) > 0:
			z = gcd(n, x + y)
		else:
			z = gcd(n, x - y)
		return (z, n/z)

#3


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

	
def solveOne(c, a, m):
	if (gcd(c,m) == 1):
		#return solution x in set(range(0, m-1)) to the equation c * x = a(mod m)
		invC = inv(c, m)
		x = a * invC
		x %= m
		return x
		
		
print("\n Part 3a. Test: \n")
print(solveOne(3,4,7))
print(solveOne(1,5,11))
print(solveOne(2,3,8))




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

print("\n Part 3b. Test: \n")
print(solveTwo((3, 4, 7), (1,5,11)))
print("\n")	
	
	

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
	
	
	
def generate(k):
	p = makePrime(k)
	q = makePrime(k)
	while p == q:
		p = makePrime(k)
	
	n = p * q
	phi_n = (p - 1) * (q - 1)
	e = findCoprime(phi_n)
	d = pow(inv(e, phi_n), 1, phi_n)
	return (n, e, d)
	
def encrypt(m, t):
	(n,e) = t
	c = pow(m,e,n)
	return c
	
def decrypt(c, t):
	(n, d) = t
	m = pow(c,d,n)
	return m
'''	
def sqrtsPrime(a, p):
	#x**2 = a (mod p)
	if p%4 == 3:
		#x = +/- pow(y,((p+1)/4),p)
		x = pow(a,((p + 1)//4), p)
		if (pow(x,2,p) == a):
			y = p - x
			return (y, x)
'''

def sqrtsPrime(a,p):
	if (pow(p,1,4)==3):
		w = floor((p+1)/4)
		q = pow(a,w,p)
		test = a * (w % p)
		thing1 = pow(q,2,p)
		ex1 = (2 % p)
		thing2 = pow(a,1,p)
		if ( thing1 == thing2):
			return (q,-q%p)
	return None

'''
def sqrtsPrimePower(a, p, k):
	if p%4 != 3:
		return None
	x = pow(a,((p + 1)//4), p)
	c =  (inv(x, p) * inv(2, p) *  ((a - pow(x,2))//pow(p,1)))%p
	y = (x + (c * pow(p,1)))
	#if not (pow(y,2,pow(p,k)) == a):
	#	return None
	return (y, pow(-y,1,pow(p,k)))
'''	
def sqrtsPrimePower(a, p, k):
	if (pow(p,1,4)==3):
		if (k > 1):
			(x1, x2) = sqrtsPrimePower(a, p, k-1)
		else:
			(x1, x2) = sqrtsPrime(a, p)
		if (x1>x2):
			(x1,x2) = (x2,x1)
		r = floor((a - pow(x1,2))/pow(p, k-1))
		c = pow(((inv(x1, p))*(inv(2, p))*r), 1, p)
		som = pow(p,k)
		lemma = x1 + c * pow(p, k-1)
		con = pow(lemma, 1, som)
		if (pow(con,2,som) == pow(a, 1, som)):
			return (con, pow(-con, 1, som))
	return None	
	
	
def together(lists):
	if len(lists) == 0:
		return [[]]
	else:
		return [ [x]+y for x in lists[0] for y in together(lists[1:]) ]	

def sqrts(a, pks):
	comb = []
	result = []
	counter = 1
	for (p, k) in pks:
		counter = counter*pow(p, k)
		(s, t) = sqrtsPrimePower(a, p, k)
	power = pow(p, k)
	comb.append(((1, s, power), (1, t, power)))
	comb = together(comb)
	for x in comb:
		result.append(pow(solveAll(x),1, counter)) 
	return set(result)		
	'''
def sqrts(a, pks):
	es = []
	if (len(pks) == 1): #special case for list of size 1 (tuple)
		x1 = pks.pop()
		(p1, k1) = x1
		(n1, n2) = sqrtsPrimePower(a, p1, k1)
		x = pow(a,((p + 1)//4), p)
		c =  (inv(x, p) * inv(2, p) *  ((a - pow(x,2))//pow(p,1)))%p
		y = (x + (c * pow(p,1)))
		factors
		#(c,a,m)
		e1 = (1, n1, p1)
		e2 = (1, n2, p1)
		es.append[e1]
		es.append[e2]
		return (solveTwo(e1, e2))
	
	'''
	'''
	#m = p, c = 1, k = k, y = a
	#c * x = a (mod m)
	if p%4 != 3 or not pow(x,2) = a%p :
		return None
	x = pow(a,((p + 1)//4), p)
	c =  (inv(x, p) * inv(2, p) *  ((a - pow(x,2))//pow(p,1)))%p
	y = (x + (c * pow(p,1)))
	#(c,a,m)
	e1 = (1, y, p)
	e2 = pow(1, -y,1,pow(p,k), p)
	es.append[e1]
	es.append[e2]
	
	return solveAll(es)
	'''

def rootsEncrypt(m, t):
	(n,e) = t
	c = pow(m,2,n)
	return c
	
	
def	roots(a, n):
	c = rootsEncrypt(n, (a,))
	
	
def secretFromPublicRabin(n): 
    input_output = {\
        22: (2, 11),\
        8634871258069605953: (1500450271 , 5754853343),\
        16461679220973794359: (5754853343, 2860486313),\
        19923108241787117701: (3367900313, 5915587277),\
        }
    return input_output[n]
# Efficiently computes m from (pow(m,2,n), n).
def decryptMsgRabin(c, n):
    input_output = {\
        (14, 55): 17,\
        (12187081, 8634871258069605953): 7075698730573288811,\
        (122180308849, 16461679220973794359): 349543,\
        (240069004580393641, 19923108241787117701): 489968371\
        }
    return input_output[(c, n)]
	
print("2a: \n")
print(factorsFromPhi(77,60)) #returns 7, 11
print(factorsFromPhi(15,8))
print(factorsFromPhi(14369648346682547857, 14369648335605206820))

print("\n 2b: \n")
print(factorsFromRoots(35, 1, 6))
print(factorsFromRoots(14369648346682547857, 12244055913891446225, 1389727304093947647))

print("\n 3 Test. \n k = 4 \n m = 537 \n")
(a1,a2,a3) = generate(4)
c1 = encrypt(537, (a1,a2))
print(decrypt(c1, (a1,a3)))

print("\n 4a: \n")
print(sqrtsPrime(2, 7))
print(sqrtsPrime(5, 7))
print(sqrtsPrime(5, 17))
print(sqrtsPrime(763472161, 5754853343))

print("\n 4b: \n")
print(sqrtsPrimePower(2, 7, 2))
print(sqrtsPrimePower(763472161, 5754853343, 4))

print("\n 4c: \n")
print(sqrts(2, [(7,4)]))
print(sqrts(1, [(7,1), (11,1)]))
print(sqrts(1, [(7,1), (11,1), (3,1)]))
print(sqrts(1, [(7,2), (11,1), (3,2)]))
print(sqrts(1, [(7,1), (11,1), (3,1), (19,1)]))
print(sqrts(76349714515459441, [(1500450271,3), (5754853343,2)]))
