import random
r=random.random
n=2048

print "x1"
for _ in range(n): print r()**0.5 * 100

print "x2"
for _ in range(n): print r()**2 * 100

print "x3"
for _ in range(n): print r() * 100
