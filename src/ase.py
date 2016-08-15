#!/usr/bin/python
from __future__ import division,print_function
import sys,re,random,argparse,traceback,time,math,copy,pprint
from functools import wraps
from collections import defaultdict
sys.dont_write_bytecode=True
pp = pprint.PrettyPrinter(indent=4)

###############################################################################
# Copyright (c) 2016 tim@menzies.us
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
###############################################################################

### GLOBALS ###################################################################
PASS=FAIL=0

#TODO: normalize back in cdom
#    : add "k" to knn

help = lambda : [
"""
(C) 2016, tim@menzies.us MIT, v2
Useful routines for building simple data miners and optimizers
""","""
"And He shall have sway and dominion over all the world." 
-- Wolf (a.k.a. Eddie Izzard) 

Most of the complexity here is the enable a generic, say, SA that can have 
different  models passed to it as  argument.

Can implements incremental sway (O(N), not O(3N)).

For simplicity's sake, there is no normalization on objectives.  Hence, the eval
functions need to be well-behaved i.e. ideally 0..1 or, more realistically, (a)
all goals are to be minimized; (b) the eval function does not deliver numbers
that are orders of magnitude different.
""",
  # sway
  elp("SWAY's target population = pop^swayCull", swayCull  = 0.5),
  elp("SWAY's smallest size, leaf clusters",     swayStop  = 2),
  elp("SWAY projections bigger",                 swayBigger= 0.2),
  # -----------------------------------------------------------------
  # div
  elp("verbose mode for DIV",                    divVerbose= False),
  elp("DIV's cohen measure",                     divCohen  = 0.2),
  elp("DIV's trivally small delta",              divTrivial= 1.05),
  elp("""DIV's enough items in a cluster (if 0,
         computed from pop size)""",             divEnough = 0),
  elp("""when DIV's are tiny (if 0,
         computed using divCohen)""",            divTiny   = 0),
  # -----------------------------------------------------------------
  # naive Bayes
  elp("NaiveBayes m",                            nbm       = 2),
  elp("NaiveBayes k",                            nbk       = 1),
  # -----------------------------------------------------------------
  # distance
  elp("power constant for distance",             edist     = 2.0),
  elp("what to use to compute distance",         dist      = ["decs", "objs"]),
  # -----------------------------------------------------------------
  # optimization (general)
  
  elp("model number",                            model= [0,1,2,3,4,5,6]),
  elp("continuous domination bigger",            cdomBigger= 0.005),
  elp("evalautions before pausing to reflect",   era       = 100),
  elp("lives before quiting" ,                   lives     = 5),
  elp("population size",                         pop       = 100),
  elp("evaluation budget",                       budget    = 10000),
  elp("mutation retries limit",                  retries   = 100),
  elp("probability of mutating a field",         cf        = 0.3),
  elp("size of smear",                           f         = 0.7),
  elp("splay size for the 'around1' mutatio",    splay     = 0.5),
  elp("trial size",                              trials    = 20),
  elp("pop0 size ",                              pop0      = 100),
  elp("verbose optimization",                    verbose=False),

  
  # -----------------------------------------------------------------
  # optimization (sa)
  elp("SA's cooling schedule",                   cooling= 2),

  # -----------------------------------------------------------------
  # optimization (max walk sat)
  elp("probablity of local search",              localSearch= 0.5),
  elp("local search steps",              localSteps= 10),
  
  # misc
  elp("Disable distance normalization",          raw       = False),
  elp("run unit tests",                          tests     = False),
  elp("tiles display width",                     tiles     = 40),
  elp("small effect size (Cliff's dela)",        cliff     = [0.147, 0.33, 0.474]),
  elp("keep at most, say, 256 samples",          samples   = [256,128,512,1024]),
  elp("in pretty print, round numbers",          round     = 3),
  elp("use quintiles if this==5 else quartiles", ntiles    = [5,4]),
  elp("probability of reading a row",            some      = 1.00),
  elp("random number seed",                      seed      = 61409389),
  elp("training data (arff format",              train     = "train.csv"),
  elp("testing data (csv format)",               test      = "test.csv"),
  # --------------------------------------------------------------------
  # System
  elp("Run some test function, then quit",       run       = "")
]
def elp(h, **d):
  def elp1():
    if val is False :
      return dict(help=h, action="store_true")
    if isinstance(val,list):
      return dict(help=h, choices=val,default=default, metavar=m ,type=t)
    else:
      return dict(help=h + ("; e.g. %s" % val), default=default, metavar=m, type=t)
  key,val = d.items()[0]
  default = val[0] if isinstance(val,list) else val
  m,t = "S",str
  if isinstance(default,int)  : m,t= "I",int
  if isinstance(default,float): m,t= "F",float
  return "--" + key, elp1()

def options(before, after, *lst):
  parser = argparse.ArgumentParser(epilog=after, description = before,
              formatter_class = argparse.RawDescriptionHelpFormatter)
  for key, rest in lst:
    parser.add_argument(key,**rest)
  return parser.parse_args()

THE = options(*help())

### LIB ########################################################################

def same(x)  : return x
def less(x,y): return x < y
def more(x,y): return x > y
def square(x): return x*x
def exp(x)   : return math.exp(x)
def dinc(d,x): d[x] = d.get(x,0) + 1
def max(x,y) : return x if x>y else y
def min(x,y) : return x if x<y else y
def ro(x)    : return round(x,THE.round)
def ros(lst) : return map(ro,lst)
def zos(lst) : return ', '.join(map(unZero,map(ro,lst)))
def unZero(f):
  return ('%.15f' % f).rstrip('0').rstrip('.')

def isa(x,y) : return isinstance(x,y)
def copied(x): return copy.deepcopy(x)

def rseed(s=None): random.seed(s or THE.seed)
def r()          : return random.random()
def any(lst)     : return random.choice(lst)
def shuffle(lst) : random.shuffle(lst); return lst
def dot(x='.',show=THE.verbose)   :
  if show: sys.stdout.write(str(x)); sys.stdout.flush()

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
  
def rows(file,prep=same):
  with open(file) as fs:
    for line in fs:
      line = re.sub(r'([\n\r\t]|#.*)', "", line)
      row = map(lambda z:z.strip(), line.split(","))
      if len(row)> 0:
         yield prep(row) if prep else row

def atoms(lst):
  return map(atom,lst)

def atom(x)  :
  try: return int(x)
  except:
    try: return float(x)
    except ValueError:
      return Sym

def timeit(f,repeats=1):
  start = time.time()
  for _ in xrange(repeats):
    f()
  stop = time.time()
  return (stop - start)/repeats
  
def atom2(x)  :
  try: return float(x),Num
  except ValueError: return x,Sym

def kv(d, private="_"):
  "Print dicts, keys sorted (ignoring 'private' keys)"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,THE.round) if isa(x,float) else x
  return '('+', '.join(['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]) + ')'

class Pretty(object):
  def __repr__(i):
    return i.__class__.__name__ + kv(i.__dict__)
    
class o(Pretty):
  def __init__(i, **adds): i.__dict__.update(adds)
  
### LIB.test suite ##################################################

def oks():
  global PASS, FAIL
  if THE.tests:
    print("\n# PASS= %s FAIL= %s %%PASS = %s%%"  % (
          PASS, FAIL, int(round(PASS*100/(PASS+FAIL+0.001)))))

def ok(f):
  global PASS, FAIL
  if THE.tests:
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



### LIB.tiles ##################################################
def xtiles(pairs):
  pairs = [(name,sorted(lst)) for name,lst in pairs]
  lo   = sorted(map(lambda z:z[1][ 0], pairs))[0]
  up   = sorted(map(lambda z:z[1][-1], pairs))[-1]
  mid  = 2 if  THE.ntiles==5 else 1
  pairs= [ (xtile(pair[1],lo=lo,up=up),pair[0]) for pair in pairs]
  return sorted(pairs,
                key = lambda z:z[0][1][mid])
  
  
def xtile(lst,lo=None, up=None):
  lo   = lo or lst[0]
  up   = up or lst[-1]
  r    = lambda n: int(n)         # round
  ok   = lambda z: max(0, min(len(lst) - 1, z))
  yth  = lambda y: lst[ ok(r(len(lst)*y)) ]  # yth percentile item
  pos  = lambda y: r((yth(y) - lo) / (up - lo + 0.00001) * THE.tiles) # xth place   
  tiles= [" "] * THE.tiles
  seen = []
  if THE.ntiles==5:
    for z in xrange(pos(0.1), pos(0.3)): tiles[z] = "-"
    for z in xrange(pos(0.7), pos(0.9)): tiles[z] = "-"
    seen = [yth(z) for z in [0.1,0.3,0.5,0.7,0.9]]
  else:
    for z in xrange(pos(0.25), pos(0.75)): tiles[z] = "-"
    seen = [pos(z) for z in [0.25,0.5,0.75]]
  tiles[ pos(0) ] = "|"
  tiles[ pos(1) ] = "|"
  
  tiles[ pos(0.5) ] = "*"
  return ''.join(tiles), ros(seen)




### Sample  ###################################################################
def cache(f):
  @wraps(f)
  def memo(i):
    if i.cache is None:  i.cache = f(i)
    return i.cache
  return memo
  
class Sample(Pretty):
  def __init__(i, init=[],max=None):
    i.n, i._some  = 0, []
    i.max = max or THE.samples
    i.cache = None
    map(i.add,init)
  def sample(i):
    return any(i._some)
  def add(i,x):
    i.n += 1
    now  = len(i._some)
    if now < i.max:
      i.cache = None
      i._some += [x]
    elif r() <= now/i.n:
      i.cache = None
      i._some[ int(r() * now) ]= x
  def __ne__(i, j): # assumes all samples are nums
    "Cliff's delta"
    lt = gt = 0
    for x in i._some:
      for y in j._some:
        if x > y: gt += 1
        if x < y: lt += 1
    z = (lt + gt) / (len(i._some) * len(j._some))
    return z >= THE.cliff
  @cache
  def stats(i): # assumes all samples are nums
    i._some = sorted(i._some)
    z= lambda z: int(max(0, min(len(i._some) - 1, z)))
    x= lambda y: i._some[ok(int(len(i._some)*y))]
    return o(median= x(0.5),
             lo    = i._some[0],
             hi    = i._some[-1],
             some  = i._some,
             iqr   = x(0.75) - x(0.25),
             bars  = [x(p) for p in [0.1,0.3,0.5,0.7,0.9]])


### Columns  ###################################################################
class Summary(Pretty):
  def __init__(i,init=[]):
    i.reset()
    map(i.add,init)

class Thing(Summary):
  "some thing that can handle  Nums or Syms"
  UNKNOWN = "?"
  def __init__(i,pos,txt=None):
    txt = txt or pos
    i.txt, i.pos, i.my, i.samples = str(txt), pos, None, Sample()
  def sample(i):
    return i.samples.sample()
  def add(i,x):
    if x != Thing.UNKNOWN:
      if i.my is None:
        x,what  = atom2(x)
        i.my = what()
      x = i.my.add(x)
      i.samples.add(x)
    return x

class Num(Summary):
  def reset(i):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
  def add(i,x):
    i.n += 1
    x = float(x)
    if x > i.up: i.up=x
    if x < i.lo: i.lo=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    return x 
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def sd(i):
    return 0 if i.n <= 2 else (i.m2/(i.n - 1))**0.5
  def norm(i,x):
    if not THE.raw:
      tmp= (x - i.lo) / (i.up - i.lo + 10**-32)
      if tmp > 1: return 1
      elif tmp < 0: return 0
      else: return tmp
    return x
  def dist(i,x,y):
    return i.norm(x) - i.norm(y)
  def furthest(i,x) :
    return i.up if x <(i.up-i.lo)/2 else i.lo
  def like(i,x,*_):
    var   = i.sd()**2
    denom = (2*math.pi*var)**.5
    num   = math.exp(-(x-i.mu)**2/(2*var))
    return num/denom
 
   
class Sym(Summary):
  def reset(i):
     i.counts, i.most, i.mode, i.n = {},0,None,0
  def add(i,x):
    i.n += 1
    new = i.counts[x] = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new,x
    return x
  def sub(i,x):
    i.n -= 1
    i.counts[x] -= 1
    if x == i.mode:
      i.most, i.mode = None,None
  def norm(i,x)   : return x
  def dist(i,x,y) : return 0 if x==y else 1
  def furthest(i,x): return "SoMEcrazyTHing"
  def like(i,x,prior):
    return (i.counts.get(x,0) + THE.nbm*prior)/(i.n + THE.nbm)
  def k(i):
    return len(i.counts.keys())
  def ent(i):
    """Measures how many symbols are mixed up together.  If only one symbol, then
       ent=0 (nothing mixed up)."""
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp
  
#XXX??/ dump Function

### Rows  ######################################################################
class Row(Pretty):
  rid = 0
  def __init__(i,lst):
    i.rid = Row.rid = Row.rid+1
    i.contents=lst
    i.labelled=False
  def __repr__(i)       : return '#%s,%s' % (i.rid,i.contents)
  def __getitem__(i,k)  : return i.contents[k]
  def __setitem__(i,k,v): i.contents[k] = v
  def __len__(i)        : return len(i.contents)
  def __hash__(i)       : return i.rid #hash(set(i.contents))
  def __eq__(i,j)       : return i.rid == j.rid
  def __ne__(i,j)       : return not i.__eq__(j)

### About ####################
# ways to generate decisions and objectoves

class About1number(Pretty):
  def __init__(i,txt,lo=0, up=1,get=None):
    i.txt, i.lo, i.up,i.want,i.get = txt,lo,up,None,get
    if i.txt[0] == Table.MORE: i.want=more
    if i.txt[0] == Table.LESS: i.want=less
  def __call__(i,*lst):
    return i.get(*lst) if i.get else i.lo + r()*(i.up - i.lo)
  def norm(i,x):
    if x < i.lo:
      i.lo = x
      return 0
    if x > i.up:
      i.hi = x
      return 1
    return (x - i.lo)/(i.up - i.lo + 1E-16)
  def wrap(i,x):
    lo,up = i.lo, i.up
    return lo if lo==up else lo + ((x - lo) % (up - lo))
  def cap(i,x):
    return max(i.lo, min(i.up, x))
  def around1(i,x, splay=THE.splay):
    gap = (i.up - i.lo)* splay
    return x - gap*(0.5 + r())
  def localSearch(i):
    for j in xrange(0,THE.localSteps):
      yield i.lo + j/10*(i.up - i.lo)
  def smear(i,a,b,c):
    return a if r() > THE.cf else a + THE.f * (b - c)
  def better(i,x,y):
    return i.want(x,y) if i.want else False
  def worse(i,x,y):
    if not i.want   : return False
    if x == y       : return False
    if i.better(x,y): return False
    return True

class About1symbol(Pretty):
  def __init__(txt,*lst,**d):
    i.txt = txt
    for x in lst:
      d[x] = 1
    i.n, i.bias=0,[]
    for x in d: 
      n    += d[x]
      i.bias += [(d[x],x)]
    i.bias  = sorted(i.bias, reverse=True)
  def __call__(i):
    z = r()
    for feq,thing in bias:
      z -= freq/n
      if z <= 0:
        return thing
    return bias[-1][0]
  def norm(i,x)  : return x
  def wrap(i,x)  : return x
  def cap(i,x)   : return x
  def better(i,x,y): return False
  def worse(i,x,y):  return False
  def around(i,_): return i.__call__()
  def localSearch(i):
    for _,x in i.bias:
      yield x
  def smear(i,a,b,c):
    return a if r() > THE.rc else (b if r() > THE.f else c)
  

N,S = About1number,About1symbol

def summaries(pop,abouts):
  summary = [Thing(pos) for pos,_ in enumerate(abouts._objs)]
  for one in pop:
    for col,thing in zip(abouts._objs,summary):
      thing.add(one[col.pos])
  return map(lambda x: x.samples.stats().median, summary)
  
class Abouts(Pretty):
  def __init__(i):
    i.evals = 0
    i.abouts()
  def ok(i,row): return True
  def fresh(i) : return Row(["?"] * i.cols)
  def copyDecs(i,old):
    tmp = i.fresh()
    for dec in i._decs:
      tmp[dec.pos] = old[dec.pos]
    return tmp
  def decsObjs(i):
    row0 = i.decs()
    return i.objs(row0)
  def decs(i,retries = THE.retries)  :
    assert retries > 0, 'too hard to generate valid decisions'
    row = i.fresh()
    for dec in i._decs:
      row[dec.pos] = dec()
    return row if i.ok(row) else i.decs(retries - 1)
  def objs(i,row): 
    if not row.labelled:
      row = i.objs1(row)
      i.evals += 1
      row.labelled=True
    return row
  def objs1(i,row):
    for obj in i._objs: row[obj.pos] = obj(row)
    return row
  def scores(i,row):
    return [row[col.pos] for col in i._objs]
  def normObjs(i,row):
    row = i.objs(row)
    norms  = [ col.norm( row[col.pos] ) for col in i._objs]
    return sum( map(square, norms) ) ** 0.5  / len(i._objs)**0.5
  def ready(i,**d):
    i._decs    = d["decs"]
    i._objs    = d["objs"]
    for pos,about1 in enumerate(i._decs + i._objs):
      about1.pos = pos
    i.cols = len(i._decs) + len(i._objs)
    return i
  def table(i, rows):
    names = [col.txt for col in i._decs + i._objs ]
    tbl = Table()
    tbl(names)
    for row in rows:
      tbl(row.contents)
    return tbl
  
class Fonseca(Abouts):
  n=3
  def abouts(i):
    def f1(row):
      z = sum([( row[col.pos] - 1/math.sqrt(Fonseca.n))**2
               for col in i._decs])
      return 1 - math.e**(-1*z)
    def f2(row):
      
      z = sum([( row[col.pos] + 1/math.sqrt(Fonseca.n))**2
               for col in i._decs])
      return 1 - math.e**(-1*z)
    return i.ready(decs= [N(str(n), lo= -4, up=4)
                          for n in xrange(Fonseca.n)],
                   objs= [N("<f1", get= f1),
                          N("<f2", get= f2)])

class Viennet4(Abouts):
  n=2
  def ok(i,row):
     one,two = row[0],row[1]
     g1 = -1*two - 4*one + 4
     g2 = one + 1            
     g3 = two - one + 2
     return g1 >= 0 and g2 >= 0 and g3 >= 0
  def abouts(i):
    def f1(row):
      one,two = row[0], row[1]
      return (one - 2)**2 /2 + (two + 1)**2 /13 + 3
    def f2(row):
      one,two = row[0], row[1]
      return (one + two - 3)**2 /175 + (2*two - one)**2 /17 - 13
    def f3(row):
      one,two= row[0], row[1]
      return (3*one - 2*two + 4)**2 /8 + (one - two + 1)**2 /27 + 15
    return i.ready(decs= [N(str(n),lo=-4,up=4)   for n in range(Viennet4.n)],
                   objs= [N("<f1",lo=  0, up= 10, get=f1),
                          N("<f2",lo=  -15, up= -5, get=f2),
                          N("<f3",lo= 12, up= 27, get=f3)])     

def DTLZ6_10(): return DTLZ6(10)
def DTLZ6_20(): return DTLZ6(20)
def DTLZ6_40(): return DTLZ6(40)

class DTLZ6(Abouts):
  """
  This is called DTLZ6 in the original paper but listed at DTLZ7 in jmetal
  Taken from some Java code at the jMetal site: https://goo.gl/rDLC8f
  """
  def __init__(i, nobjs = 3):
    i.ndecs, i.nobjs = nobjs-1,nobjs
    Abouts.__init__(i)
  def objs1(i,row):
    k  = i.nobjs
    g  = sum([row[ col.pos ] for col in i._decs])
    g  = 1 + 9*g/k
    f  = [ row[col.pos] for col in i._decs ]
    h1 = lambda j: f[j]/(1+g) *(1+math.sin(3*math.pi*f[j]))
    h  = sum([h1(j) for j in xrange(i.nobjs-1)])
    h  = i.nobjs - h
    f += [(1+g)*h]
    for pos,x in enumerate(f):
      row[i.ndecs + pos] = f[pos]
    return row
  def defObj(i,j):
    return lambda row: i.objs(row)[i.ndecs + n ]
  def abouts(i):
    return i.ready(decs = [N(str(n)) for n in xrange(i.ndecs)],
                    objs = [N("<f%s" % n, lo=0,up=25, get=i.defObj(n))
                           for n in xrange(i.nobjs)])

def wrap(x,col): return col.wrap(x)
def cap(x,col):  return col.cap(x)
  
def around1(x,col)  : return col.around1(x)
def any1thing(_,col): return col()

def deFiddles(old,new,abouts,pop,_):
  a,b,c = any3(pop, it = lambda z: z.rid)
  for col in abouts._decs:
    i     = col.pos
    new[i]= col.smear(a[i], b[i], c[i])
  col = any(abouts._decs)
  new[col.pos] = old[col.pos]
  return new

def maxWalkSatFiddles(_old,new,abouts,_,better):
  "cut down version, assumes only one goal"
  col  = any(abouts._decs)
  if r() > THE.localSearch: # just do anything
    new[col.pos] = any1thing(_,col)
    return new
  else:
    best = copied(new)
    for x in col.localSearch():
      new[col.pos] = x
      if  better(new,best,abouts): # multi-obj domination
        best  = copied(new)
    return best

# de's eval counts increased by THE.localSteps
# this mutate is also the creation thing. need to unify.
# susp[ect that 'create' will be simpler

def mutate(old, abouts, pop=[], better= lambda x,y,z: cdom(x,y,z),
           fiddles= None,      # e.g. de. maxWalkSat
           fiddle = any1thing, # e.g. around1 or any1thing
           after  = wrap,      # e.g. wrap or cap
           retries= THE.retries):
  assert retries > 0, 'too hard to satisfy model'
  new = abouts.copyDecs(old)
  if fiddle:
    for col in abouts._decs:
      if r() < THE.cf:
        new[col.pos] = fiddle(old[col.pos], col)  # eg around1, any1thing
  if fiddles:
    new = fiddles(old,new,abouts,pop, better) # eg deFiddles maxWalkSatFiddles
  if after:  # e.g. wrap cap
    for col in abouts._decs:
      new[col.pos] = after(new[col.pos], col)
  return new if abouts.ok(new) else mutate(old, abouts, pop,better,
                                          fiddles,fiddle, after,
                                          retries=retries-1)

### Tables #####################################################################      
class Table(Pretty):
  
  DIST  = {'decs' : lambda tbl:tbl.decs,
           'objs' : lambda tbl:tbl.objs}[THE.dist]
  MORE  = ">"
  LESS  = "<"
  KLASS = "="
  SYM   = "!" 
  SKIP  = "-"
  def __init__(i,inits=[]):
    i._rows = []
    i.cost = 0
    i.cols,  i.objs, i.decs = [], [], []
    i.klass, i.gets, i.dep  = [], [], []
    map(i.__call__, inits)
  def isa(i,row):
    return row[ i.klass[0].pos ]
  def clone(i,inits=[]):
    tbl = Table()
    tbl([col.txt for col in i.cols])
    map(tbl.__call__,inits)
    return tbl
  def __call__(i,row):
    if i.cols:
      row     = [i.cols[put].add(row[get])
                 for put,get in enumerate(i.gets)]
      row     = Row(row)
      i._rows += [ row ]
    else:
      for get,cell in enumerate(row):
        if cell[-1] != Table.SKIP:
          i.gets += [get]
          col     = Thing(len(i.cols) , cell)
          i.cols += [col]
          if   cell[0] == Table.MORE  : i.objs  += [(col,more)]
          elif cell[0] == Table.LESS  : i.objs  += [(col,less)]
          elif cell[0] == Table.KLASS : i.klass += [col]
          else                        : i.decs  += [col]
          #---------------------------------------
          for col,_ in i.objs  : i.dep   += [col]
          for col   in i.klass : i.dep   += [col]
          if cell[-1] == Table.SYM:
            col.my = Sym()
    return row
  def furthest(i,r1,cols=None,f=None, better=more,init= -1,ignore=set()):
    out,d = r1,init
    for r2 in i._rows:
      if r1.rid != r2.rid:
        if not r2 in ignore:
          tmp = i.distance(r1,r2,cols,f)
          if better(tmp, d):
            out,d = r2,tmp
    return out
  def closest(i,r1,cols=None,f=None,ignore=set()):
    return i.furthest(r1,cols=cols,f=f,better=less, init=10**32,ignore=ignore)
  def distance(i,r1,r2,cols=None,f=None):
    cols = cols or Table.DIST(i)
    f    = f    or THE.edist
    d,n = 0, 10**-32
    for col in cols:
      x, y  = r1[col.pos], r2[col.pos]
      if x is Thing.UNKNOWN and y is Thing.UNKNOWN:
        continue
      if x is Thing.UNKNOWN: x=col.my.furthest(y)
      if y is Thing.UNKNOWN: y=col.my.furthest(x)
      n    += 1
      inc   = col.my.dist(x,y)**f
      d    += inc
    return d**(1/f)/n**(1/f)
  def distances(i,r1,cols=None,f=None):
    return sorted([(i.distance(r1,r2,cols,f),r2)
                   for r2 in i._rows
                   if r2.rid != r1.rid
                 ])
  def label1(data,row):
    return row # usually rewritten by subclass


### Table filters #################################################################


def csv2table(file):
  tbl= Table()
  for row in rows(file):
    tbl(row)
  return tbl

def arff2rows(file): 
  tbl   = Table()
  seen  = lambda x,y: re.match('^[ \t]*'+x,y,re.IGNORECASE)
  data,div  = False," "
  words = []
  with open(file) as fs: # cant use 'rows' since i have to flip commans
    for line in fs:
      line = re.sub(r'([\n\r]|#.*)', "", line)
      row  = map(lambda z:z.strip(), line.split(div))
      if row != []:
        if   seen("@relation", row[0]) : tbl.relation = row[1]
        if   seen("@attribute", row[0]): words += [row[1]]
        elif data and len(row) > 1     :
          yield tbl,tbl(row)
        elif seen("@data", row[0])     :
          data,div=True,","
          words[-1] = "=" + words[-1]
          tbl(words)

def arff2table(file):
  for tbl,_ in arff2rows(file): pass
  return tbl

def table2arff(tbl):
  rel = tbl.relation if "relation" in tbl.__dict__ else "data"
  print("@relation", rel, "\n")
  for col in tbl.cols:
    vals="real"
    if isa(col.my,Sym):
      vals = set([row[col.pos] for row in tbl._rows
                if row[col.pos] != Thing.UNKNOWN])
      vals = '{' + ', '.join(vals) + '}'
    print("@attribute",col.txt,vals)
  print("\n@data")
  for row in tbl._rows:
    print(', '.join(map(str,row)))


def like(row,all,klasses):
  guess, best, nh, k = None, -1*10**32, len(klasses), THE.nbk
  for this,tbl in klasses.items():
    guess = guess or this
    like  = prior = (len(tbl._rows)  + k) / (all + k * nh)
    for col in tbl.decs:
      if col.my:
        x = row[col.pos]
        if x != Thing.UNKNOWN:
          like *= col.my.like( x, prior)
    if like > best:
      guess,best = this,like
  return guess
  
### Learners   ####################################################################
def knn(train=THE.train,test=THE.test): return learn(knn1,train,test)
def nb( train=THE.train,test=THE.test): return learn(nb1, train,test)

def learn(what, train, test):
  print(train,test)
  for actual, predicted in what(train, test):
    print(actual, predicted)

def nb1(train,test):
  klasses = {}
  for all,(tbl1,row) in enumerate(arff2rows(train)):
    k = tbl1.isa(row)
    if not k in klasses:
      klasses[k] = tbl1.clone()
    klasses[k](row)
  for tbl2,row in arff2rows(test):
    yield tbl2.isa(row), like(row,all,klasses)

def knn1(train,test):
  tbl = arff2table(train)
  k   = tbl.klass[0].pos
  for _,r1 in arff2rows(test):
    r2 = tbl.closest(r1)
    yield r1[k],r2[k]
  

  
### Discretize ####################################################################
class Range(Pretty):
  def __init__(i, label=None, n=None,  lo=None,  report=None,
                  id=None,   up=None, has=None, score=None):
    i.label, i.lo, i.up, i._has = label, lo, up, has
    i.score, i.n, i.id         = score, n, id
    i.report=report
  def pretty(i)  :
    if i.lo == i.up:
      return str(i.lo)
    else:
      return '[%s..%s]' % (i.lo,i.up)

def relevant(tbl, goal):
  "Only returns a range if it contains the goal."
  for pos,ranges in sharp(tbl):
    for range in ranges:
      if range.report.mode == goal:
        yield pos,range

def sharp(tbl):
  "Only returns something is discretization can split the column."
  for col in tbl.cols:
    if isa(col.my,Num):
      ranges = div(div, label=col.txt,
                   x= lambda z: z[col.pos],
                   y= lambda z: z[tbl.klass[0].pos])
      if len(ranges) > 1:
        yield col.pos, ranges
        
def div(lst,label=0, x= same, y= same, yKlass= Num):
  def divide(lst, out=[], lvl=0, cut=None):  
    xlhs, xrhs   = Num() , Num(map(x,lst))
    ylhs, yrhs   = yKlass(), yKlass(map(y,lst))
    score,score1 = value(yrhs),None
    n            = len(lst)
    report       = copied(yrhs)
    for i,new in enumerate(lst):
      x1= x(new)
      y1= y(new)
      if not x1 == Thing.UNKNOWN:
        xlhs.add(x1); xrhs.sub(x1)
        ylhs.add(y1); yrhs.sub(y1)
        if xrhs.n < enough:
          break
        else:
          if xlhs.n >= enough:
            start, here, stop = x(lst[0]), x1, x(lst[-1])
            if here - start > tiny:
              if stop - here > tiny:
                score1 = ylhs.n/n*value(ylhs) + yrhs.n/n*value(yrhs)
                if score1*THE.divTrivial < score:
                  if yKlass == Num:
                    cut,score= i,score1
                  else:
                    k0,e0,ke0 = yrhs.k(), yrhs.ent(), ke(yrhs)
                    gain   = k0 - score1
                    delta  = math.log(3**k0-2,2)-(ke0- ke(yrhs)-ke(ylhs))
                    border = (math.log(n-1,2) + delta)/n
                    if gain >= border:
                      cut,score = i,score1
    if THE.divVerbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if cut:
      divide(lst[:cut], out= out, lvl= lvl+1)
      divide(lst[cut:], out= out, lvl= lvl+1)
    else:
      out.append(Range(label=label, score=score, report=report,
                       n=len(lst), id=len(out),
                       lo=x(lst[0]), up=x(lst[-1]),
                       has=lst))
    return out
    # --- end function divide -----------------------------
  if not lst: return []
  ke     = lambda z: z.k()*z.ent()
  ent    = lambda z: z.ent()
  sd     = lambda z: z.sd()
  value  = sd if yKlass==Num else ent
  tiny   = THE.divTiny  or Num(map(x,lst)).sd() * THE.divCohen
  enough = THE.divEnough or len(lst)**0.5
  return divide( sorted(lst[:], key=x), out=[] ,lvl=0) # copied, sorted






### Optimizers #################################################################
def above(x,y,tbl,better=more):
  "single objective"
  klass=tbl.klass[0].pos
  return better(x[klass], y[klass])

def below(x,y,tbl):
  "single objective"
  return above(x,y,tbl, better=less)
  
def bdom(x, y, abouts):
  "multi objective"
  x=abouts.objs(x)
  y=abouts.objs(y)
  betters = 0
  for obj in abouts._objs:
    x1,y1 = x[obj.pos], y[obj.pos]
    if obj.better(x1,y1) : betters += 1
    elif x1 != y1: return False # must be worse, go quit
  return betters > 0

def cdom(x, y, abouts):
  "many objective"
  x= abouts.objs(x)
  y= abouts.objs(y)
  def w(better):
    return -1 if better == less else 1
  def expLoss(w,x1,y1,n):
    return -1*math.e**( w*(x1 - y1) / n )
  def loss(x, y):
    losses= []
    n = min(len(x),len(y))
    for obj in abouts._objs:
      x1, y1  = x[obj.pos]  , y[obj.pos]
      x1, y1  = obj.norm(x1), obj.norm(y1)
      losses += [expLoss( w(obj.want),x1,y1,n)]
    return sum(losses) / n
  l1= loss(x,y)
  l2= loss(y,x)
  return l1 < l2 

def reference(pop,abouts,better=bdom):
  alive = {row.rid:True for row in pop}
  for row1 in pop:
    if alive[row1.rid]:
      #dot("?")
      for row2 in pop:
        if alive[row2.rid]:
          #dot(".")
          if better(row1,row2,abouts):
            #dot("!")
            alive[row2.rid] = False
  return [row for row in pop if alive[row.rid]]

def sway( population, tbl, better= bdom) :
  def cluster(items, out):
    if len(items) < max(len(population)**THE.swayCull, THE.swayStop):
      out.append(tbl.clone(items))
    else:
      west, east, left, right = split(items, int(len(items)/2)) 
      if not better(east,west,tbl): cluster( left, out )
      if not better(west,east,tbl): cluster( right, out )  
    return out
  
  def split(items, mid,west=None, east=None,redo=20):
    assert redo>0
    cosine = lambda a,b,c: ( a*a + c*c - b*b )/( 2*c+ 0.0001 )
    #if west is None: west = any(items) 
    #if east is None: east = any(items)
    if west is None: west = tbl.furthest(any(items))
    #if east is None: east = tbl.furthest(west)
    if east is None: east = any(items)
    while east.rid == west.rid:
      east = any(items)
    c      = tbl.distance(west, east)
    xs     = {}
    for n,item in enumerate(items):
       a = tbl.distance(item, west)
       b = tbl.distance(item, east)
       x = xs[ item.rid ] = cosine(a,b,c) # cosine rule
       if a > c and abs(a-c)  > THE.swayBigger:
         dot(">%s " % n)
         return split(items, mid, west=west, east=item, redo=redo-1)
       if b > c and abs(b-c) > THE.swayBigger:
         dot("<%s " % n)
         return split(items, mid, west=item, east=east, redo=redo-1)   
    items = sorted(items, key= lambda item: xs[ item.rid ]) # sorted by 'x'
    return west, east, items[:mid], items[mid:] 
  # --------
  return cluster(population, [])

              
def sa(abouts=Fonseca()):
  def score(row) : return abouts.normObjs(row)
  def inc(k)     : events[k] = events.get(k,0) + 1
  def improved() : return events.get('!',0) > 0
  abouts.evals = 0
  s0 = s  = sb = abouts.decsObjs()
  e  = eb = score(s)
  k, frontier, events = 1, [],{}
  lives = THE.lives + 1
  while abouts.evals < THE.budget:
    dot(" %s\n%5.3f |" % (kv(events),eb))
    lives = THE.lives if improved() else lives - 1
    if lives < 1:
      break
    events = {'!' : 0}
    for _ in xrange(THE.era):
      event= "."
      k += 1
      sn = mutate(s,abouts)
      en = score(sn)
      if en < eb:
        sb,eb    = s,e = sn,en
        inc("!")
        frontier = [sb]
      elif en < e:
        s,e = sn, en
        event = "<"
      else:
        frontier += [sn]
        t = k/THE.budget
        if exp((e - en)/t) < r()**THE.cooling:
          event = "?"
          s,e   = sn, en
      inc(event)
      dot(event)
  return o(s0=s0, sb=sb,
           frontier=frontier) # list of things not worse than best

def mws(abouts=Fonseca(), better=bdom, sb=None,s0=None):
  def inc(k)     : events[k] = events.get(k,0) + 1
  def improved() : return events.get('!',0) > 0
  maxTries  =  20
  maxChange = 100
  lives      =  5
  events     = {}
  abouts.evals=  0
  frontier    = []
  for _ in xrange(maxTries):
    eb = abouts.scores(sb) if sb else  []
    dot(" %s\n%s |" % (kv(events),ros(eb)))
    lives = THE.lives if improved() else lives - 1
    if lives < 1:
      break
    events = {'!' : 0, "=" : 0}
    s = abouts.decsObjs()
    sb = sb or s
    s0 = s0 or s
    for _ in xrange(maxChange):
      status="."
      s = mutate(s,abouts,better=bdom,fiddles=maxWalkSatFiddles)
      if better(s,sb,abouts):
        sb = copied(s)
        fronter = [sb]
        status = "!"
      else:
        frontier += [copied(s)]
        status = "."
      inc(status)
      dot(status)
  return o(sb=sb,s0=s0,frontier=frontier)

def de(abouts=Fonseca(), better=bdom, sb=None,s0=None):
  def inc(k)     : events[k] = events.get(k,0) + 1
  def improved() : return events.get('!',0) > 0
  def best(lst)  : return copied(reference(lst, abouts,cdom))
  frontier = [abouts.decs() for _ in xrange(10*len(abouts._decs))]
  events = {}
  s0 = best(frontier)
  lives = THE.lives + 1
  while abouts.evals < THE.budget:
    eb = summaries(frontier,abouts)
    dot(" %s\n%s |" % (kv(events),ros(eb)))
    lives = THE.lives if improved() else lives - 1
    if lives < 1:
      break
    events = {'!' : 0}
    for (i,parent) in enumerate(frontier):
      event="."
      kid = mutate(parent,abouts,frontier,
                   better=better,fiddles=deFiddles)
      if better(kid,parent,abouts):
        frontier[i]= kid
        event="!"
      dot(event)
      inc(event)
  return o(sb=best(frontier),
           s0=s0,
           frontier=frontier)

def igds(models,opts):
  subs=400
  def sampleFrontier0(abouts):
    tmp = abouts()
    return [tmp.decsObjs() for _ in xrange(THE.pop0)]
  def finalFrontier(abouts,opt):
    tmp = abouts()
    results = opt(tmp)
    return reference(results.frontier, tmp)
  for abouts in models:
    all,some = Sample(max=subs), defaultdict(lambda : [])
    some['baseline'] = sampleFrontier0(abouts)
    for opt in opts:
      rseed()
      print("\n",opt,": ",sep="",end="")
      for t in xrange(THE.trials):
        dot(t,True)
        tmp        = finalFrontier(abouts,opt)
        some[opt] += tmp
        for one in tmp: all.add(one)
    dot(">1",True)
    abouts1=abouts()
    all = all._some
    print(len(all))
    all = reference(all,abouts1)
    things= {}
    dot(">2",True)
    for opt in some:
      things[opt] = Thing(opt)
      tbl  = abouts1.table(all)
      mine = Sample([tbl(row) for row in some[opt]],max=subs)._some
      dot(">3[%s] " % len(mine),True)
      for row in mine:
        ref = tbl.closest(row,cols=tbl.decs,ignore=mine)
        igd = tbl.distance(row,ref, cols=tbl.decs)
        things[opt].add(igd)
    yield abouts, xtiles([(opt, things[opt].samples._some)
                           for opt in things])
    
      
                                                    
### Unittests #################################################################        

  
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
  lst=list('abcdefghijklmnopqrstuvwxyz')
  for x in sorted([''.join(any3(lst)) for _ in xrange(30)]):
    print(x)
  
  
@ok
def _atom2():
  x,t=atom2('23.1')
  assert isinstance(x,float), "coercion failure1"
  x,t= atom2('tim menzies')
  assert isinstance(x,str), "coercion failure2"

@ok
def _sample():
  rseed(1)
  s = Sample(list('i have gone to seek a great perhaps'),max=8)
  print(s)
  assert s._some == [' ', ' ', 'n', 'p', 'v', 'e', 'r', 'p']

@ok
def _sample1():
  rseed()
  n = 1000
  s1,s2,s3,s4 = Sample(), Sample(), Sample(), Sample()
  for _ in xrange(n): s1.add(r()**4/2)
  for _ in xrange(n): s2.add(r()**2)
  for _ in xrange(n): s3.add(r()**0.5* 1.5)
  for _ in xrange(n): s4.add(3*r()**0.33)
  lsts = [(str(i),s.stats().some) for i,s in enumerate([s1,s2,s3,s4])]
  for (a,b),c in xtiles(lsts):
    print(c,a,b)


@ok
def _sym():
 assert Sym(list('i have gone to seek a great perhaps')).counts['a'] == 4

@ok
def _col():
  rseed(1)
  n= Num( [ 600 , 470 , 170 , 430 , 300])
  assert 164.711 <= n.sd() <= 164.712
  assert n.lo == 170
  assert n.up == 600

@ok
def _table(file= "data/weather.csv",show=True): 
  tbl = csv2table(file)
  for col in tbl.cols:
    print(col.pos,col)
  print("===")
  for col,what in tbl.objs:
    print(col.txt,what.__name__)
  if show:
    table2arff(tbl)

@ok
def _arff(file= "data/weather.arff",show=True):
  tbl =  arff2table(file)
  for col in tbl.cols:
    print(col.pos,col)
  print("===")
  for col in tbl.klass:
    print(col)
  if show: 
    table2arff(tbl)

@ok
def _table1():
  _table("data/diabetes.csv",show=False)

@ok
def _table2():
  print("Loading 100,000 records takes",
        timeit(lambda:
               _table("data/diabetes100000.csv",False)),"seconds.")

@ok
def _distances(file= "data/diabetes.csv"):
  rseed()
  tbl= csv2table(file)
  for r1 in shuffle(tbl._rows)[:4]:
    tmp  = tbl.distances(r1)
    tmp1 = tbl.closest(r1)
    print("")
    print("it   :",r1)
    print("far  :",tmp[-1][1], tmp[-1][0])
    print("near1:",tmp[0][1], tmp[0][0])
    print("near2:",tmp1, tbl.distance(r1,tmp1))

@ok
def _sway(file="data/diabetes.csv"):
  rseed()
  tbl0 = csv2table(file)
  print(0,tbl0.klass[0].my.counts,
        tbl0.klass[0].my.ent())
  leafs = sway(tbl0._rows,tbl0,below)
  n=0
  for c,tbl in enumerate(leafs):
    n += len(tbl._rows)
    print(c,tbl.klass[0].my.counts,
          tbl.klass[0].my.ent())
  print(n)

#@ok
  def worker():
    rseed()
    tbl0 = csv2table(file)
    print(0,tbl0.klass[0].my.counts,
          tbl0.klass[0].my.ent())
    leafs = sway(tbl0._rows,tbl0,below)
    n=0
    for c,tbl in enumerate(leafs):
      n += len(tbl._rows)
      print(c,tbl.klass[0].my.counts,
            tbl.klass[0].my.ent())
    print(n)
  print(timeit(worker))
  
@ok
def _sdiv():
  rseed()
  n   = 10000
  lst = [r()**2 for x in xrange(n)]
  lst = lst + [r()**0.5 for x in xrange(n)]
  for range in  div([(i,n) for i,n in enumerate(lst)],
                    x=lambda z:z[0],
                    y=lambda z:z[1]):
    print(range)

@ok
def _sdiv1():
  rseed()

  lst = [63
         ,53
         ,52
         ,48
         ,45
         ,44
         ,41
         ,36
         ,34
         ,34
         ,34
         ,33
         ,32
         ,31
         ,31
         ,31
         ,29
         ,28
         ,28
         ,28]
  for range in  div(lst,
                    x=lambda z:z,
                    y=lambda z:z):
    print(range)

@ok
def _sdiv2():
    lst=[83
         ,67
         ,82
         ,65
         ,69
         ,76
         ,63
         ,49
         ,50
         ,46
         ,46
         ,49
         ,46
         ,46
         ,44
         ,39
         ,42
         ,46
         ,42
         ,40]
    for range in  div(lst,
                    x=lambda z:z,
                    y=lambda z:z):
      print(range)

@ok
def _ediv():
  rseed()
  lst0=list('abcd')
  lst = []
  for _ in xrange(2500):
    for i,x in enumerate(lst0):
      lst += [[i+0.5*r(), x]] # 'a' is around 0.5, 'd' is around 3.5
  for y in div( lst,yKlass=Sym,
                x=lambda z: z[0],
                y=lambda z: z[1]):
    print(y)

@ok          
def _knn():
  for actual, predicted in knn("data/soybean.arff","data/soybean.arff"):
    print(actual,predicted)

@ok
def _Fonseca():
  rseed()
  f= Fonseca()
  for _ in xrange(10):
    print(f.decsObjs())
@ok
def _Viennet4():
  rseed()
  f= Viennet4()
  s1,s2,s3 = Num(), Num(), Num()
  for _ in xrange(100000):
    row = f.decsObjs()
    s1.add(row[2]), s2.add(row[3]), s3.add(row[4])
  print(s1.lo,s1.up)
  print(s2.lo,s2.up)
  
  print(s3.lo,s3.up)

@ok
def _bdom():
  print(1)


def models(n=THE.model):
  return [Fonseca,Viennet4,DTLZ6,DTLZ6_10,DTLZ6_20,DTLZ6_40][n]

@ok
def _sa(abouts=Fonseca):
  rseed()
  out = sa(abouts())
  print("")
  print(ros(out.s0))
  print(ros(out.sb))
  print(len(out.frontier))

@ok
def _mws(abouts=models()):
  rseed()
  print("#",abouts,len(abouts()._objs))
  _sa(abouts)
  out = mws(abouts())
  print("")
  print(ros(out.s0))
  print(ros(out.sb))
  print(len(out.frontier))

@ok
def _de(abouts=models()):
  rseed()
  print("#",abouts,len(abouts()._objs))
  out1 = mws(abouts())
  print("")
  print(ros(out1.s0))
  print(ros(out1.sb))
  print(len(out1.frontier))
  out2 = de(abouts())
  print("")
  print(len(out2.frontier))

  
@ok
def _DTLZ6():
  rseed()
  f= Viennet4()
  s1,s2,s3 = Num(), Num(), Num()
  for _ in xrange(100000):
    row = f.decsObjs()
    s1.add(row[2]), s2.add(row[3]), s3.add(row[4])
  print(s1.lo,s1.up)
  print(s2.lo,s2.up)
  
  print(s3.lo,s3.up)

@ok
def _bdom(abouts=models(2)):
  rseed()
  f= abouts()
  rows = [f.decsObjs() for _ in xrange(1024)]
  c = reference(rows,f,cdom)
  for row in c[:10]: print("c",row)
  b = reference(rows,f,bdom)
  for row in b[:10]: print("b",row)
  print("b",len(b),"c",len(c))

@ok
def _igds():
  models= [Fonseca,Viennet4,DTLZ6,DTLZ6_10]
  opts  = [ sa, mws, de]
  for what, reports in igds(models,opts):
    print("\n",what)
    for report in reports:
      print(report)
      
if THE.run:
  f= eval("lambda : %s()" %THE.run)
  ok(f())
  sys.exit()
  

# check ignore works
# add in the stats
# why is distnace so slow.
