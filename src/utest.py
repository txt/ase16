#!/usr/bin/python
"""
utest.py (c) 2016 tim@menzies.us, MIT licence

Part of http://tiny.cc/ase16: teaching tools for
(model-based) automated software enginering.

USAGE: 
(1) If you place '@ok' before a function, then
load that file, then that function will execute and
all assertion failures will add one to a FAIL
count.
(2) To get the final counts, add 'oks()' at the end
of the source code.

For more on this kind of tool, see
https://www.youtube.com/watch?v=nIonZ6-4nuU
"""
from __future__ import division,print_function
import sys,re,traceback,random
sys.dont_write_bytecode=True

PASS=FAIL=0
VERBOSE=True

def oks():
  global PASS, FAIL
  print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
          PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))

def ok(f):
  global PASS, FAIL
  try:
      print("\n-----| %s |-----------------------" % f.__name__)
      if f.__doc__:
        print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__))
      f()
      print("# pass")
      PASS += 1
  except Exception,e:
      FAIL += 1
      print(traceback.format_exc()) 
  return f


#################################################
  
def same(x):
  return x

def any(lst):
  return random.choice(lst)

def any3(lst,a=None,b=None,c=None,it = same,retries=10):
  assert retries > 0
  a = a or any(lst)
  b = b or any(lst)
  if it(a) == it(b):
    return any3(lst,a=a,b=None,it=it,retries=retries - 1)
  c = any(lst)
  if it(a) == it(c) or it(b) == it(c):
    return any3(lst,a=a,b=b,it=it,retries=retries - 1)
  return a,b,c

@ok
def _ok1():
  "Can at least one test fail?"
  assert 1==2, "equality failure"

@ok
def _ok2():
  "Can at least one test pass?"
  assert 1==1, "equality failure"

@ok
def _any3():
  """There are 2600 three letter alphanet combinations.
     So if we pick just 10, there should be no repeats."""
  random.seed(1)
  lst=list('abcdefghijklmnopqrstuvwxyz')
  seen = {}
  for x in sorted([''.join(any3(lst)) for _ in xrange(10)]):
    seen[x] = seen.get(x,0) + 1
  for k,v in seen.items():
    assert v < 2
  print("")
 
oks()
