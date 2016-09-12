
[home](http://tiny.cc/ase2016) |
[copyright](https://github.com/txt/ase16/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://raw.githubusercontent.com/txt/ase16/master/img/mase16.png">](http://tiny.cc/ase2016)<br>
[overview](https://github.com/txt/ase16/blob/master/doc/overview.md) |
[syllabus](https://github.com/txt/ase16/blob/master/doc/syllabus.md) |
[src](https://github.com/txt/ase16/tree/master/src) |
[submit](http://tiny.cc/ase16give) |
[chat](https://ase16.slack.com/) 


______




# Homework5: Your Second Optimizer (Basic Max Walk Sat)

Read the [lecture](mws.md) on Max Walk Sat.

Code  MaxWalkSat  for the
[Osyczka2](pdf/moeaProblems.pdf) model.

Do not be clever. This is throw away code. As quick
and as dirty as you like.


Use the same energy calcs as for SA.

Try and make a report that looks like the output from SA.

## Tips

### Not everything is "ok".


Note that this model has constraints-- so after you
_mutate_ a solution, you must check if it is _ok_
(I.e. does not violate the constraints-- otherwise,
mutate again until ok).


### Local Search

Not sure that this is useful to you but, for what its worth,
here is my local search code. First, for each column,
it knows how to spin over min to max of each col:

```python
import random
def r(): return random.random()

class Column:
  "This code is in a class that knows min,max for each decision"
  ...
  def any(i):
    return i.min + r()*(i.max - i.min)
  def localSearch(i):
    for j in xrange(0,10):
      yield i.min + j/10*(i.max - i.min)

def mwsfiddle(old):
  new = old[:]  # copy
  col = random.choice(cols) # pick any column
  i   = col.pos # we will change things in this column
  if r() > 0.5: # just do anything
    new[i] = col.any()
    return new
  best = None
  for x in col.localSearch():
    new[i] = x
    if better(new,best): # insert your scoring function here
      best = new[:]
  return best
```

#### When

Use p=0.5

### Watch those evals

Note that now, when you report evals, then you are reporting _steps * evals_. So when you report how long it takes to reach a
solution, remember to reports _steps * evals_.



