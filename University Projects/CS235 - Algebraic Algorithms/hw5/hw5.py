'''
Created by Ben Blau - collaboration with Tyler Butler, and Alex Casella
April 18th 2014
Professor Lapets CS235
Homework 5
Filename: hw5.py
exec(open("hw5.py").read())
'''

from math import floor
from fractions import gcd
from random import randint
from urllib.request import urlopen



'''
1a.
[1,2,3,0] o [3,0,1,2]
= [0, 1, 2, 3]


1b.
[46,47,...,99,0,1,2,3,4,...,45] o [11,12,...,99,0,1,2,3,4,...,10]
= [57, 58, ..., 99, 0, 1, 2, 3, 4, ... 56]


1c.
p o q o p^(-1) o q^(-1)
= [0, ... , n-1]


1d.
p o p o p o p
= [0, ... , n-1]


1e.                      
[1,3] o [1,3] = [1,1]	1 * 1 = 1
[1,3] o [3,1] = [3,3]	1 * 3 = 3
[3,1] o [3,1] = [1,1]	3 * 3 = 1
[3,1] o [1,3] = [3,3]	3 * 1 = 3


1f.
closure({3 + 9Z}, +)              
[0,3,6] o [0,3,6] = [0,6,3]	0 + 0 = 0
[0,3,6] o [3,6,0] = [3,0,6]	0 + 3 = 3
[0,3,6] o [6,0,3] = [6,3,0]	0 + 6 = 6
[3,6,0] o [0,3,6] = [3,0,6]	3 + 0 = 3
[3,6,0] o [3,6,0] = [6,3,0]	3 + 3 = 6
[3,6,0] o [6,0,3] = [0,6,3]	3 + 6 = 0
[6,0,3] o [0,3,6] = [6,3,0]	6 + 0 = 6
[6,0,3] o [3,6,0] = [0,6,3]	6 + 3 = 0
[6,0,3] o [6,0,3] = [3,0,6]	6 + 6 = 3


1g.
closure({2 + 15z}, *) = [2, 2*2, 2*2*2, 2*2*2*2, ...] = [2, 4, 8, 1]
Z/4Z = [0, 1, 2, 3]

closure({2 + 15z}, *)      Z/4Z
2                           0
4                           1
8                           2
1                           3


1h.
No isomorphism can exist between (S4, o) and (Z/5Z, +) because they are of difference size

'''

##BELOW FROM PREVIOUS HW

def probablePrime(m):
    a = randint(2, m-1)
    if ((pow(a, (m-1), m) != 1) or (m/a == 0) or (gcd(a, m) != 1)):
        return False
    return True
    
def isCoprime(x, y):
    return gcd(x,y) == 1 

def closest(t, ks): 
    L = [] 
    for k in ks: 
        L.append(abs(t-k)) 
    return ks[L.index(min(L))]


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
##ABOVE FROM PREVIOUS HW



#permute([2,1,0], ['a','b','c'])
#returns ['c','b','a']

def permute(p, l):
	L = []
	duplicate = []
	for a in l:
		duplicate.append(a)
	for i in p:
		a = duplicate.pop(i)
		duplicate.insert(i, 'z')
		L.append(a)
	return L
	
print("\n 2a: permute([2,0,1,4,3], ['a','b','c','d','e']) \n")
print(permute([2,0,1,4,3], ['a','b','c','d','e']))

#C(1, 4)
#[1, 2, 3, 0] --> shifts the cyclic permutation C_m up by k

def C(k, m):
	L = []
	for i in range(0,m):
		if (i+k >= m):
			L.insert(i,i + k - m)
		else:
			L.insert(i,i+k)
	return L	

print("\n 2b: C(4,6) \n")	
print(C(4,6))

#M(2, 5)
#[0, 2, 4, 1, 3]		
def M(a, m):
	J = C(0,m) #construct the permutation
	L = [] 
	for i in J:
		L.append((a * i) % m) #perform the multiplication & mod and then append into L
	return L	

print("\n 2c: M(2, 5) \n")	
print(M(2, 5))

def sortHelper(S):
	for j in range(0, len(S) - 1): #checks if S is ordered through comparisons
		if S[j] < S[j+1]: #check if S is ordered
			if j == len(S) - 2:
				return True
		else:
			return False
			
def sort(l):	
	n = len(l)
	R = []
	S = []
	#CYCLIC CHECK
	for i in range(0, n):
		R = C(i,n) #generates cyclical permutations of size n
		S = permute(R, l) #applies C_n to original permutation --> denoted S
		if sortHelper(S) == True:
			return R
	#MULT CHECK
	#go through list of M's (Z = M's)
	#use X = permute(Z, l)
	#if X == l
	#return Z
	for a in range(1, n):
		if gcd(a, n) == 1:
			Z = M(a,n)
			X = permute(Z, l)
			if sortHelper(X) == True:
				return Z
			
	
print("\n 2d: \n")	
print("\n  sort([38,16,27]) --> [1,2,0]\n")
print(sort([38,16,27]))	
print("\n  sort([38,16,27,35,36]) --> [1,2,3,4,0]\n")
print(sort([38,16,27,35,36]))	
print("\n permute(sort([38,49,16,27]), [38,49,16,27]) \n")	
print(permute(sort([38,49,16,27]), [38,49,16,27]))
print("\n sort([1, 13, 4, 17, 6, 23, 9]) \n")
print(sort([1, 13, 4, 17, 6, 23, 9]))	
#print("\n sort([0, 17, 4, 21, 8, 25, 12, 29, 16, 3, 20, 7, 24, 11, 28,\
#          15, 2, 19, 6, 23, 10, 27, 14, 1, 18, 5, 22, 9, 26, 13]) \n")
#print(sort([0, 17, 4, 21, 8, 25, 12, 29, 16, 3, 20, 7, 24, 11, 28,\
#          15, 2, 19, 6, 23, 10, 27, 14, 1, 18, 5, 22, 9, 26, 13]))
		  
		  
def unreliableUntrustedProduct(xs, n):
    url = 'http://cs-people.bu.edu/lapets/235/unreliable.php'
    return int(urlopen(url+"?n="+str(n)+"&data="+",".join([str(x) for x in xs])).read().decode())

def privateProduct(xs, p, q):
	D = []
	(a1,a2,a3) = generate(q)
	
	for x in xs:
		c1 = encrypt(x, (a1, a2))
		D.append(c1)
	
	eresult = unreliableUntrustedProduct(D, a1) 
	dresult = pow(eresult, a3, a1)
	
	return dresult % p
    
def validPrivateProduct(xs, p, q):
	D = []
	
	(n,e,d) = generate(q)    
	r = randint(0, q-1)
	
	qinv = inv(q,p)
	pinv = inv(p,q)
	while True:
		for x in xs:
			crtiso = (x*q*qinv + r*p*pinv)%(n)   #Implement CRT Isomorphism with each number in x paired with r (x,r) 
			c1 = encrypt(crtiso, (n, e))            #c1 = y^e(mod n) 
			D.append(c1)
		
		encryptresult = unreliableUntrustedProduct(D, n) #encrypt
	
		decryptresult = pow(encryptresult, d, n)  #decrypt   #((c1*...*ck)^e)^d) (mod n)
	
		result = decryptresult % p #result to be returned
		result1 = decryptresult % q #result for comparison with check
		check = pow(r, len(xs),q)
	#print(result%q)
	#print(check)
		
		if check == result1:
			return result  		  
	


a = [2, 3, 5]

print("\n 3b: \n")
#print(privateProduct(a, 89, 71))
print(validPrivateProduct(a, 87, 91))
print(validPrivateProduct(a, 87, 91))
print(validPrivateProduct(a, 87, 91))
print(validPrivateProduct(a, 87, 91))




		  
		  
