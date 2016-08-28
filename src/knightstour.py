#!/usr/bin/python
from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode=True

any = random.choice

class KnightsTour:
  moves = ((1, 2), (1, -2), (-1, 2), (-1, -2),
           (2, 1), (2, -1), (-2, 1), (-2, -1))
  def __init__(i,x,seed=1):
    i.x = x
    random.seed(seed)
    i.goto( random.randint(0,x-1),
            random.randint(0,x-1),
            [ [ None for _ in range(x)]  for _ in range(x) ])
  def jump(i,x0,y0,b):
    for x1,y1 in KnightsTour.moves:
      x,y = x0+x1, y0+y1
      if 0 < x < i.x:
        if 0 < y < i.x:
          if not b[x][y]:
            yield x,y
  def jump2(i,x0,y0,b):
    all = [ (len([_ for _ in i.jump(x,y,b)]),(x,y))
            for x,y in i.jump(x0,y0,b)]
    print(sorted(all[1]))
    return sorted(all)[0][1]
  def goto(i,x,y,b):
    n = 0
    while n < i.x**2:
      b[x][y] = n
      n += 1
      x,y = i.jump2(x,y,b)
      
      
KnightsTour(8,1)
