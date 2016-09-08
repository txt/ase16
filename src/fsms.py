#!/usr/bin/python
from __future__ import division, print_function
import sys, random, os

sys.dont_write_bytecode = True


# usage:
#   python fsm.py 21083 # for a long-ish run
#   python fsm.py 1     # for a short run

# ----------------------------------------------
def fsm0(agent):
  m = Machine(agent)
  entry = m.state("entry")  # first names state is "start"
  foo = m.state("foo")
  bar = m.state("bar")
  stop = m.state("stop.")  # anything with a "." is a "stop"
  m.here = entry
  m.trans(T(entry, walk, foo),
          T(foo, walk, foo),
          T(foo, sit, stop),
          )
  return m


# ----------------------------------------------
def maybe():    return random.random() > 0.5

def walk(w, a): return maybe()

def sit(w, a): return maybe()

def ok(w, a):   return True


def fail(w, a):  return maybe()


def again(w, a): return maybe()


# ---------------------------------------------
def kv(d):
  return '(' + ', '.join(['%s: %s' % (k, d[k])
                          for k in sorted(d.keys())
                          if k[0] != "_"]) + ')'


def shuffle(lst):
  random.shuffle(lst)
  return lst

def move(): return random.randint(-10, 10)


class Pretty(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)


class o(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)


# ----------------------------------------------
class State(Pretty):
  def __init__(i, name):
    i.name, i.out, i.visits = name, [], 0

  def stop(i):
    return i.name[-1] == "."

  def looper(i):
    return i.name[0] == "#"

  def arrive(i):
    if not i.looper():
      i.visits += 1
      assert i.visits <= 5, 'loop detected'

  def next(i, w):
    for tran in shuffle(i.out):
      if tran.gaurd(w, tran):
        return tran.there
    return i


class Trans(Pretty):
  def __init__(i, here, gaurd, there):
    i.here, i.gaurd, i.there = here, gaurd, there


T = Trans


class Machine:
  Factory = []  # considered making it a class but it only has one method

  def __init__(i,k):
    i.states = {}
    i.first = i.here = None  # i.here now an instance var
    i.name = k
    i.pos = 0
    Machine.Factory.append(i)

  def trans(i, *trans):
    for tran in trans:
      tran.here.out += [tran]

  def state(i, txt):
    tmp = State(txt)
    i.states[txt] = tmp
    i.first = i.first or tmp
    return tmp

  @staticmethod
  def run(seed=1, ticks=100):
    print('#', seed)
    random.seed(seed)
    w = o(now=0)
    while w.now < ticks:
      alive = False
      for machine in shuffle(Machine.Factory):
        if not machine.here.stop():
          alive = True
          w.now += 1
          machine.step(w)
          Machine.report(machine.name)
          break
      if not alive: break

    return w

  @staticmethod
  def report(name):
    max_len = 50
    lst = [0]*(max_len+1)
    for machine in Machine.Factory:
      lst[machine.pos] += machine.name
    show = lambda x : str(x if x else ".")
    print(name," | ", " ".join(map(show, lst)))

  def step(i, w):
    if not i.here:
      i.here = i.start
      i.here.arrive()
    elif not i.here.stop():
      i.here = i.here.next(w)
      i.here.arrive()
      i.pos += move()



any = random.choice


if __name__ == '__main__':
  fsm0(1)
  fsm0(2)
  fsm0(4)
  if len(sys.argv) > 1:
    Machine.run(int(sys.argv[1]))
  else:
    Machine.run()
