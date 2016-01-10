'''
Created by Ben Blau - collaboration with Tyler Butler & Alex Casella
February 14th 2014
Professor Lapets CS235
Homework 2
Filename: hw2.py
'''

from fractions import gcd
'''
Problem 1:
a.
7 * x + 2 ≡ 6 (mod 31)
7 * x ≡ 4 (mod 31)
7 * x ≡ 35 (mod 31)
7 * x ≡ 7 * 5 (mod 31)
x ≡ 5 mod (31)
x ≡ 5 + 31Z        ---> Z being the congruence class

b.
40 * x ≡ 5 (mod 8)
No solution since 8 isn't prime and 40 IS a multiple of 8

c.
3 * x + 1 ≡ 1 (mod 3)
3 * x ≡ 0 (mod 3)
3 * x ≡ 3 * 0 (mod 3)
x ≡ 0 (mod 3)
x ≡ 0 + 3Z
x ≡ {0 + 3Z, 1 + 3Z, 2 + 3Z}

d.
1 + 2 * x ≡ 4 (mod 14)
14 is not prime
2 * x ≡ 3 (mod 14)
No solution

e.
17 * x + 11 ≡ 300 (mod 389)
17 * x ≡ 289 (mod 389)
x ≡ 17 (mod 389)
x ≡ 17 + 389Z

f.
718581210326212034673 * x ≡ 1 (mod 9843578223646740201)
^----this is a-----^               ^----this is b----^
gcd(a,b) = b
b * 73 = a
gcd = 73 != 1
No solution

g.
48822616 * x ≡ 14566081015752 (mod 3333333333333333333333333)
^---a--^	   ^-----b------^
b/a = 298347
x ≡ 298347 (mod 3333333333333333333333333)
x ≡ 298347 + 3333333333333333333333333Z

'''
	
def closest(t, ks):
	L = []
	for k in ks:
		L.append(abs(t-k))
	return ks[L.index(min(L))]
	
	
##print(closest(5, [1,3,4,9,10]))
  
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
	
print(gcd(findCoprime(100), 100))
print(findCoprime(330))
print(findCoprime(1000))
print(findCoprime(273))
print(gcd(findCoprime(2543423), 2543423))



def randByIndex(m, i):
##m is the upper bound of random numbers generated
##i represents an index specifying which random number in the sequence should be generated
##assume m > 4 and 1 <= i <= m - 1
##function returns the "i"th random number in the permutation {0...,m-1}
## something something generate a number < m since m is upper bound
	##for a in range(0, m-1):
		##if isCoprime(a,m):
		a = findCoprime(m)
		return (a * i) % m
		##uses findCoprime to generate relatively random numbers

'''		
for any a and m both in N, if isCoprime(a,m) then (i*a) mod m (0<=i<=m-1)
euclids lemma = a,b,c in N, if (b*c)/a and isCoprime(a,b) then c/a
since a and m are coprime, a*x = a*y mod m, x = y mod m
'''
#print([randByIndex(10,i) for i in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}])
#print([randByIndex(77, i) for i in range(0,76)])

#print(findCoprime(2**2000))

def probablePrime(m):
    for a in {randByIndex(123, 5), randByIndex(23, 6)}:
        if ((pow(a, (m-1), m) != 1) or (m/a == 0) or (gcd(a, m) != 1)):
            return False
    return True

#print(probablePrime(107))	
#print(probablePrime(230204771))	
#print(probablePrime(10738019798475862873464857984759825354679201872))	
	
	

def makePrime(d):


#d >=1, return a probable prime number that has exactly d digits
#d in N
#do -->  n = any number from {10^(d-1),..., (10^d)- 1}
#while is not probablePrime(n)
#return(n)
	#i+1 because if you put just i you get an error
	
	for i in range(10**(d-1), (10**d) - 2): 
		n = randByIndex((10**d) - 1, i)
		if probablePrime(n) and (len(str(n)) == d):
			return n

			
			
print(makePrime(2))
print(makePrime(5))
#print(makePrime(100))			