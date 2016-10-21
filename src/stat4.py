import random
r=random.random
n=256

print "x1"
for _ in range(n): print r()**0.5 * 100

print "x2"
for _ in range(n): print r()**0.49 * 100

print "x3"
for _ in range(n): print r()**2 * 100

print "x4"
for _ in range(n): print r()**2.1 * 100

print "x5"
for _ in range(n): print r()**1.0 * 100

print "x6"
for _ in range(n): print r()**1.01 * 100

