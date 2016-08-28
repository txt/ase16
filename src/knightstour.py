#!/usr/bin/python
from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode=True

# suggested usage:
#     while read; do python knightstour.py 20 $RANDOM; done

# works for huge boards: python knightstour.py 20 
# fails, rarely; e.g for python 5 4288
#    (but so fast, just run it again)

class KnightsTour:
  def __init__(i,most,x=0,y=0,show='%3s'):
    i.most = most
    b = [ [ '.' for _ in range(i.most)]
               for _ in range(i.most) ]
    n = 1
    while n <  most**2 + 1:
      b[x][y]  = n
      n       += 1
      x,y      = i.warnsdorf(x,y,b)
    for row in b:
      print(''.join([(show % cell) for cell in row]))

  def moves(i):
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
             (1, 2), (1, -2), (-1, 2), (-1, -2)]
    random.shuffle(moves)
    return moves
  
  def jump(i,x0,y0,b):
    for x1,y1 in i.moves():
      x,y = x0+x1, y0+y1
      if 0 <= x < i.most:
        if 0 <= y < i.most:
          if b[x][y] == '.':
            yield x,y
              
  def warnsdorf(i,x0,y0,b):
    # step1: all moves that could follow this move
    all = [ ([_ for _ in i.jump(x,y,b)], (x,y))
            for x,y in i.jump(x0,y0,b) ]
    
    # step2: sort the moves according to their future options
    all = sorted(all,
                 key = lambda z: len(z[0]))

    # step3: return the most constraining move
    #        (the one with least future options)
    return all[0][1] if all else (x0,y0)
    
def main(most=8, seed=1, x=None, y=None):
  print('#',seed)
  random.seed(seed)
  size = len(str(most**2)) + 1
  if not x: x = random.randint(1,most)
  if not y: y = random.randint(1,most)
  KnightsTour(most, x-1, y-1, '%%%ss' % size)

main( *map(int,sys.argv[1:]) )
