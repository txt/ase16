#!/usr/bin/python
from __future__ import division,print_function
import sys,random,os
sys.dont_write_bytecode=True

# usage:
#   python fsm.py 21083 # for a long-ish run
#   python fsm.py 1     # for a short run

#----------------------------------------------
def fsm0():
  m     = Machine()
  entry = m.state("entry") # first names state is "start"
  foo   = m.state("foo")
  bar   = m.state("bar")
  stop  = m.state("stop.") # anything with a "." is a "stop"
  m.trans(T(entry,   ok, foo),
          T(entry, fail, stop),
          T(foo,     ok,  bar),
          T(foo,   fail, stop),
          T(foo,  again, entry),
          T(bar,     ok,  stop),
          T(bar,   fail,  stop),
          T(bar,   fail,   foo))
  return m

#----------------------------------------------
def maybe():    return random.random() > 0.5
def ok (w,a):   return maybe() 
def fail(w,a):  return maybe() 
def again(w,a): return maybe()

#---------------------------------------------
def kv(d):
  return '('+', '.join(['%s: %s' % (k,d[k])
          for k in sorted(d.keys())
          if k[0] != "_"]) + ')'

def shuffle(lst):
    random.shuffle(lst)
    return lst

class Pretty(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)
    
class o(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)

#----------------------------------------------
class State(Pretty):
  def __init__(i,name): i.name, i.out, i.visits = name,[],0
  def stop(i)         : return i.name[-1] == "."
  def looper(i)       : return i.name[0] == "#"
  def arrive(i):
    print(i.name)
    if not i.looper():
      i.visits += 1
      assert i.visits <= 5, 'loop detected'
  def next(i,w):
    for tran in shuffle(i.out):
        if tran.gaurd(w,tran):
          return tran.there
    return i
  
class Trans(Pretty):
  def __init__(i,here,gaurd,there):
    i.here,i.gaurd,i.there = here, gaurd, there

T= Trans    

class Machine(Pretty):
  def __init__(i):
    i.states={}
    i.first = None
  def state(i,txt):
    tmp = State(txt)
    i.states[txt] = tmp
    i.first = i.first or tmp
    return tmp
  def trans(i,*trans):
    for tran in trans:
      tran.here.out += [tran]
  def run(i,seed = 1):
   print('#', seed)
   random.seed(seed)
   w, here = o(), i.first 
   while True:
     here.arrive()
     if here.stop():
       return w
     else:
       here = here.next(w)

if __name__ == '__main__':
  if len(sys.argv)>1:
     fsm0().run(int(sys.argv[1]))
  else:
     fsm0().run()
