#!/usr/bin/python
from __future__ import division,print_function
import sys,random,os
sys.dont_write_bytecode=True

#----------------------------------------------
def fsm0():
  m     = Machine()
  entry = m.state("entry")
  foo   = m.state("foo")
  bar   = m.state("bar")
  stop  = m.state("stop")
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
  def __init__(i,name):
    i.name, i.out, i.visits = name,[],0
class Trans(Pretty):
  def __init__(i,here,gaurd,there):
    i.here,i.gaurd,i.there = here, gaurd, there

T= Trans    

class Machine(Pretty):
  def __init__(i):
    i.states={}
  def state(i,txt):
    tmp = State(txt)
    i.states[txt] = tmp
    return tmp
  def trans(i,*lst):
    for one in lst:
      arc.here.out += [one]
  def run(i,seed = 1):
   random.seed(seed)
   w,here=o(), i.states["entry"]
   while True:
     print(here.name)
     here.visits += 1
     if here.name == "stop": return w
     if here.visits > 5: return w
     for arc in shuffle(here.out):
        if arc.gaurd(w,arc):
          here = arc.there
          break

fsm0().run(sys.argv[1])
