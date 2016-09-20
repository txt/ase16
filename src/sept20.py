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


################################################

@staticmethod
  def neighbor(self,s):
      """
      Jump to neighbour +- Jump value
      :param s:   Current state
      :return:    New State
      """
      jump=20
      while True:
          s+=random.randint(-1*jump,jump)
          if  s < pow(10,5) and s > pow(10,-5):return s

################################################

def get_min_max(xmin, xmax):
    """Brute force function to find the min and max values possible for schaffer model"""
    min_ener = float('inf')
    max_ener = float('-inf')
    min_x = float('inf')
    max_x = float('-inf')
    for x in xrange(xmin, xmax):
        curr = schaffer(x)
        if curr < min_ener:
            min_ener = curr
            min_x = curr
        if curr > max_ener:
            max_ener = curr
            max_x = curr

    return (min_ener, max_ener, min_x, max_x)

################################################

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


N,S = About1number,About1symbol

###############################################
class Pom3(Abouts):
  import pom3
  def abouts(i):
    def f1(row):
      row[10:] = pom3().simulate(row[0:9])
      return row[10]
    def f2(row): return row[11]
    def f3(row): return row[12]
    def f4(row): return row[13]
    return i.ready(
      decs=[
            N('culture',              lo=0.1 ,up=0.9),
            N('criticality',          lo=0.82,up=1.26),
            N('criticality_modifier', lo=0.02,up=0.95),
            N('initial_known',        lo=0.2 ,up=0.7),
            N('interdependency',      lo=0   ,up=50),
            N('dynamism',             lo=1   ,up=50),
            N('size',                 lo=3   ,up=300),
            N('plan',                 lo=0   ,up=1),
            N('team_size',            lo=1   ,up=44)],
      objs= [
            N("<cost",       get= f1),
            N(">score",      get= f2),
            N(">completion", get= f3),
            N("<idle",       get= f4)])

