'''
Created by Ben Blau - collaboration with Tyler Butler and Alex Casella
February 26th 2014
Professor Lapets CS235
Homework 3
Filename: hw3.py
Note** Did the extra credit problem, it made the entire program take 2 or 3 seconds to initially run
'''

from math import floor
from fractions import gcd

'''
a**(p-1) = 1 (mod p) Fermat's little theorem
a * a**(p-1) = 1 (mod p)
a**(-1) = a**(p-2) (mod p)
a * a**(-1) = a * a**(p-2) (mod p) = a**(p-1) = 1

a***(phi(m)) mod m = 1 --> if gcd(m,a) = 1    Euler's Theorem

1.
a.

THIS STEP : http://cs-people.bu.edu/lapets/235/m.php#6eeacc649d97481883bdb5ac89749d74
8 * x = 2 (mod 5)
8**(5-1) = 1 (mod 5)
8**(5-1) * 8**(-1) = 1 * 8**(-1)
8**((5-1)-1) = 8**(-1)
8**(5-2) = 8**(-1)
8**(3) = 8**(-1)
512 = 8**(-1)
512 % 5 = 2
2 = 8**(-1)

THIS STEP: http://cs-people.bu.edu/lapets/235/m.php#a089f48b8d764402873ead43c6e65d34
8**(-1) * 8 * x = 2 * 8**(-1) (mod 5)
x = 2 * 2
x = 4


b.
solve for x e Z/35Z
x = 1 (mod 7)
x = 3 (mod 5)

1 + 7Z = {1, 8, 15, 22, 29, 36, 43, 50, 57...}
3 + 5Z = {3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58...}

(1 + 7Z).union(3 + 5Z) = {...8, 43...}
8 + 35Z
x = 8 (mod 35)
*** THE ABOVE PART was just a check to find the correct answer, below is the proper work
Inverse 7 in congruence class 5
7**(-1) mod 5
7**(5-2)
7**(3) (mod 5) = 3

Inverse 5 in congruence class 7
5**(-1) mod 7
5**(7-2)
5**(5) (mod 7) = 3

x = 1 * 5 * 5**(-1) + 3 * 7 * 7**(-1)
x = 1 * 5 * 3 + 3 * 7 * 3
x = 15 + 63 = 78 (mod 35)
x = 8 (mod 35)



c.
x = 2 (mod p)
x = 4 (mod q)
p^(-1) = 5 (mod q)
q^(-1) = 3 (mod p)

x = 2 * q * q^(-1) + 4 * p * p^(-1)
= 2 * q * (3 (mod p)) + 4 * p * (5 (mod q))
= (6q (mod p) + 20p(mod q)) (mod p*q)



d.
Using Fermat's Little Theorem to calculate 5^(-1)
5^(-1) (mod 14)
= 5^(14-2)
= 5^(12) (mod 14)
= 1

Using Fermat's Little Theorem to calculate 14^(-1)
14^(-1) (mod 5)
= 14^(5-2)
= 14^(3) (mod 5)
= 4

x = 3 * 14 * 14^(-1) + 6 * 5 * 5(-1)
= 3 * 14 * 4 + 6 * 5 * 1
= 198 (mod 5 * 14)
= 198 (mod 70)
= 48 (mod 70)



'''



def invPrime(a, p):
	if (a == 0):
		return None
	c = a**(p-2) % p
	return c
	
print("Part 2a. Test\n")
print([invPrime(i,7) for i in range(0,7)])
print([invPrime(i, 13) for i in range(1,13)])
print("\n")

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
	
print("Part 2b. Test\n")
print([inv(i, 13) for i in range(1,13)])
print([inv(i, 8) for i in range(1,8)])



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
	

	
print("Part 3c. Test: \n")
print(solveAll([(3,4,7), (1,5,11)]))
print(solveAll([(5,3,7), (3,5,11), (11,4,13)]))
print(solveAll([(1,2,3), (7,8,31), (3,5,7), (11,4,13)]))
print(solveAll([(3,2,4), (7,8,9), (2,8,25), (4,4,7)]))	




def sumOfPowers(nes, ps):
	L1 = [] # list of the equations
	#nes[i] % ps[j] + nes[i+...] % ps[j] = c
	#d = (1,c,ps[j])
	
	for i in range(0, len(ps)):
		x = 0
		for j in range(0, len(nes)):
			x1 = nes[j]
			(a,m) = x1
			#adding in place of m, pow(m, 1, ps[i] - 1) changes to extra credit
			#this is instead of a**k, a**(k mod phi(m))
			c = pow(a, pow(m, 1, ps[i]-1), ps[i])
			x += c
		d = (1, x, ps[i])
		L1.append(d)
	return solveAll(L1)
	
	
	
	
	#a (mod m) + b (mod m) = (a + b) mod m, so add all the numbers with the
	#same p[i] mod to get one equation per p[i], then solve those
	
	#a**(k) % n == pow(a,k,n)
	#sum(list) returns the sum of all integers in the list
	
	
print("\n")
print("Part 4a. Test: \n")
print(sumOfPowers([(2,3), (5,6)], [3,5,7,11,13,17,19,23,29]))





primes =[\
         15481619,15481633,15481657,15481663,15481727,15481733,15481769,15481787 
        ,15481793,15481801,15481819,15481859,15481871,15481897,15481901,15481933 
        ,15481981,15481993,15481997,15482011,15482023,15482029,15482119,15482123 
        ,15482149,15482153,15482161,15482167,15482177,15482219,15482231,15482263 
        ,15482309,15482323,15482329,15482333,15482347,15482371,15482377,15482387 
        ,15482419,15482431,15482437,15482447,15482449,15482459,15482477,15482479 
        ,15482531,15482567,15482569,15482573,15482581,15482627,15482633,15482639 
        ,15482669,15482681,15482683,15482711,15482729,15482743,15482771,15482773 
        ,15482783,15482807,15482809,15482827,15482851,15482861,15482893,15482911 
        ,15482917,15482923,15482941,15482947,15482977,15482993,15483023,15483029 
        ,15483067,15483077,15483079,15483089,15483101,15483103,15483121,15483151 
        ,15483161,15483211,15483253,15483317,15483331,15483337,15483343,15483359 
        ,15483383,15483409,15483449,15483491,15483493,15483511,15483521,15483553 
        ,15483557,15483571,15483581,15483619,15483631,15483641,15483653,15483659 
        ,15483683,15483697,15483701,15483703,15483707,15483731,15483737,15483749 
        ,15483799,15483817,15483829,15483833,15483857,15483869,15483907,15483971 
        ,15483977,15483983,15483989,15483997,15484033,15484039,15484061,15484087 
        ,15484099,15484123,15484141,15484153,15484187,15484199,15484201,15484211 
        ,15484219,15484223,15484243,15484247,15484279,15484333,15484363,15484387 
        ,15484393,15484409,15484421,15484453,15484457,15484459,15484471,15484489 
        ,15484517,15484519,15484549,15484559,15484591,15484627,15484631,15484643 
        ,15484661,15484697,15484709,15484723,15484769,15484771,15484783,15484817 
        ,15484823,15484873,15484877,15484879,15484901,15484919,15484939,15484951 
        ,15484961,15484999,15485039,15485053,15485059,15485077,15485083,15485143 
        ,15485161,15485179,15485191,15485221,15485243,15485251,15485257,15485273 
        ,15485287,15485291,15485293,15485299,15485311,15485321,15485339,15485341 
        ,15485357,15485363,15485383,15485389,15485401,15485411,15485429,15485441 
        ,15485447,15485471,15485473,15485497,15485537,15485539,15485543,15485549 
        ,15485557,15485567,15485581,15485609,15485611,15485621,15485651,15485653 
        ,15485669,15485677,15485689,15485711,15485737,15485747,15485761,15485773 
        ,15485783,15485801,15485807,15485837,15485843,15485849,15485857,15485863]

		
print(
sumOfPowers(\
       [(2,29999999999999999999999999999999996)\
       ,(-8,9999999999999999999999999999999999)\
       ,(2,29999999999999999999999999999999996)\
       ,(7,7),(-13,3)], primes)
)

print("\n")
print("Extra Credit Test: \n")
print(sumOfPowers([(2,10**1000000 + 1), (-2,10**1000000 + 1), (3,3)], primes))
