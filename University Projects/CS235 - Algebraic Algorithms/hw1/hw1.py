'''
Created by Ben Blau with minor collaboration with Tyler Butler
January 29th 2014
Professor Lapets CS235
Homework 1
Filename: hw1.py
'''
def quotient(X, R):
    return {frozenset({y for y in X if (x,y) in R}) for x in X}

def divides(x,y):
    return y % x == 0   # The remainder of y/x is 0.

def prime(y):
    for x in range(2,y):
        if divides(x,y):
            return False
    return True
	
def forall(X, P):
  S = {x for x in X if P(x)}
  return len(S) == len(X)

def exists(X, P):
  S = {x for x in X if P(x)}
  return len(S) > 0

def subset(X,Y):
  return forall(X, lambda x: x in Y)
  
def atLeastOne(X, P):
  return exists(X, P)
 
def atMostOne(X, P):
  S = {x for x in X if P(x)}
  return len(S) <= 1
  
def none(X, P):
    return  forall(X, lambda x: not P(x))    

def all(X, P):
    return  forall(X, P)
    
def product(X):
	return {(x, y) for x in X for y in X }
	
def isReflexive(X, R):
	return (subset(R, product(X)) and forall(X, lambda x: (x,x) in R))

def isTransitive(X,R):
	return (subset(R, product(X)) and forall(X, lambda x: forall(X, lambda y: forall(X, lambda z: ((x,y) in R and (y,z) in R) <= ((x,z) in R)))))

	
def isSymmetric(X, R):	
	return (subset(R, product(X)) and forall(X, lambda x: forall(X, lambda y: ((x,y) in R) <= ((y,x) in R)))) 

print("isSymmetric test: \n")
print(isSymmetric({1,2}, {(1,1), (2,2), (2,1), (1,2)}))
print(isSymmetric({1,2,3}, {(1,2), (2,1), (3,3)}))
print(isSymmetric({'a','b','c'}, {('a','a'), ('b','b'), ('a','c')}))
print("\n")

print("isEquivalence test: \n")
def isEquivalence(X, R):
	return  isSymmetric(X,R) and isTransitive(X,R) and isReflexive(X,R) 

	
print(isEquivalence({1,2,3}, {(1,1), (2,2), (3,3)}))
print(isEquivalence({1,2,3}, {(1,2), (2,1), (3,3)}))
print(isEquivalence({1,2}, {(1,1), (2,2), (1,2), (2,1)}))
print(isEquivalence({0,3,6}, {(0,3), (3,6), (0,6), (3,0), (6,3), (6,0)}))
print("\n")

print("Part 2a. \n")
X1 = {"a","b","c","d"}
R1 = {("a", "b"), ("b", "a"), ("a", "a"), ("b", "b"), ("c", "d"), ("d", "c"), ("c", "c"), ("d", "d")}
print(isEquivalence(X1,R1))
print(quotient(X1,R1) == {frozenset({"a", "b"}), frozenset({"c", "d"})})
print("\n")

print("Part 2b. \n")
X2 = {0,1,2,3,4,5}
R2 = {(0,3),(3,0),(1,4),(4,1),(2,5),(5,2),(0,0),(3,3),(1,1),(4,4),(2,2),(5,5)}
print(isEquivalence(X2,R2))
print(quotient(X2,R2) == {frozenset({0,3}), frozenset({1,4}), frozenset({2,5})})
print("\n")

'''
print("Part 2c. \n")
X3 = set(range(-1000,1001))

R3 = {(range(-1000,0)).union({range(0,-1000)}),(range(1,1001)).union({range(1001,1)}),(0)}
'''
'''
R3 = { ((x,y) for x in range(-1000,0) and range(0,-1000) for y in range(-1000,0) and range(0,-1000)),((a,b) for a in range(1,1001) and range(1001,1) for b in range(1,1001) and range(1001,1)),(0)}
'''
'''
print(isEquivalence(X3,R3))
print(quotient(X3,R3) == {frozenset(range(-1000,0)), frozenset({0}), frozenset(range(1,1001))})
print("\n")
'''

def properPrimeFactors(n):
	return { x for x in set(range(2,n)) if prime(x) and divides(x,n) }
print("properPrimeFactors test: \n")
print(properPrimeFactors(9))
print(properPrimeFactors(14))
print("\n")	

def disjointHelper(x,y) :
	S = properPrimeFactors(x).intersection(properPrimeFactors(y))
	return len(S) >= 1

def disjoint(S) :
	return { (x,y) for x in S for y in S if not disjointHelper(x,y) }

print("disjoint test: \n")
print(disjoint({2,3,4,5,6}))
print(disjoint({2,4,8}))
print("\n")

'''
Part 3c below
'''
symmetric = None
reflexive = {2,3,4,5,6}
transitive = {2,3,4,5,6}

print("Part 3c: \n")
print(isReflexive(reflexive, disjoint(reflexive)))
print(isTransitive(transitive, disjoint(transitive)))
print("\n")
'''
Part 3c above
'''

def square(n):
	return exists(range(0,n), lambda x: x*x == n)

print("square test: \n")	
print(square(9))
print(square(12))
print("\n")

def pythagoreanSetConstructor(S):
	for x in range(0, 1000):
		if exists(S, not pythagorean(S)):
			S.add(x)
	return {S}
	
def pythagorean(S):
	return { (x,y) for x in S for y in S if ((square(y * y + x * x)) or (square( x * x  -  y * y )) or (square( y * y  -  x * x )) and (not x == y))}

print("\n")
print("pythagorean test: \n")
print(pythagorean({3,4}))
print(pythagorean({3,4,5,12}))
print("Part 2 of 4b: \n")



print("len(S): " + len(pythagoreanSetConstructor({})))
print("len(pythagorean(S): " + len(pythagorean(pythagoreanSetConstructor({}))))

'''
def anotherPrimeSquare(ps):
    for x in ps:
		if isPrime(square((x+y) * (x+y))):
			return square((x+y) * (x+y))
		else:
			y+=1;
			anotherPrimeSquare(x)
'''		
		
		
		
print(anotherPrimeSquare({11}))