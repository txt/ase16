#!/usr/bin/python
# knights tour with warnsdorf's ruke
# copyright (c) 2016 Tim Menzies tim@menzies.us, MIT (2 clause)

# usage python knightstour.py [BOARDSIZE] [seed] [x0] [y0]

# suggested usage:
# for((i=1;i<30;i++)); do python knightstour.py 30 $RANDOM; done

# On failure, it retries up to 20 times, picking new x0,y0 each tie.
# Usually gets it right first time, very rarely needs than 5 retries.
# Works fine up to boards of size 50. Starts to crawl a bit at size 100

from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode=True

def kt(most=8, seed=1, x=1, y=1):
  print('\n#',seed)
  random.seed(seed)
  size = len(str(most**2)) + 1
  kt1(most,'%%%ss' % size, 20, x-1,y-1)
  
def kt1(most,show,retries,x0=None,y0=None): 
  if retries <= 0: return
  if not x0: x0 = random.randint(1,most-1)
  if not y0: y0 = random.randint(1,most-1)
  n,x,y,b = 1,x0,y0, [ [ '.' for _ in range(most)] for _ in range(most) ]
  print(x+1,y+1)
  while n <  most**2:
    b[x][y] = n
    x1,y1   = warnsdorf(x,y,most,b)
    if (x1,y1) == (x,y):
      return kt1(most,  show, retries-1)
    x,y = x1,y1
    n += 1
  b[x][y] = n
  for row in b:
    print(''.join([(show % cell) for cell in row]))

def warnsdorf(x0,y0,most, b):
  def jump(x0,y0):
    for x1,y1 in shuffle([(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]):
      x,y = x0+x1, y0+y1
      if 0 <= x < most:
        if 0 <= y < most:
          if b[x][y] == '.':
            yield x,y
  # ------------------------------------------------
  # step1: all moves that could follow this move
  all = [ ([_ for _ in jump(x,y)], (x,y))
          for x,y in jump(x0,y0) ]
  # step2: sort the moves according to their future options
  all = sorted(all,
               key = lambda z: len(z[0]))
  # step3: return the most constraining move
  #        (the one with least future options)
  return all[0][1] if all else (x0,y0)

def shuffle(lst):
  random.shuffle(lst)
  return lst

kt( *map(int,sys.argv[1:]) )
