[home](http://tiny.cc/ase2016) |
[copyright](https://github.com/txt/ase16/blob/master/LICENSE.md) &copy;2016, tim&commat;menzies.us
<br>
[<img width=900 src="https://raw.githubusercontent.com/txt/ase16/master/img/mase16.png">](http://tiny.cc/ase2016)<br>
[overview](https://github.com/txt/ase16/blob/master/doc/overview.md) |
[syllabus](https://github.com/txt/ase16/blob/master/doc/syllabus.md) |
[src](https://github.com/txt/ase16/tree/master/src) |
[submit](http://tiny.cc/ase16give) |
[chat](https://ase16.slack.com/) 

_______

# What Optimizer is Best?


Sooner or later, you are going to ask "is GA/DE/PSO better than GA/DE/PSO" etc.
The answer will be _model dependent_ so, for each new model you
look at, you are going to have to do some kind of analysis.

How?

Well, first you need:

1. Models to act as case studies;
2. Optimizers, to be compared;
3. A _performance measure_ collected on running an optimizer on a model.
4. Some way to _compare_ measures. Note that, to be defensible, this
  comaprison method has to be approved by the international community.
5. A rig that runs the models and optimizers multiple times (why?)
  which collects the performance measure.
  - Tools to run all the above.

This talk is about  1,2,3.

See [stats.md](stats.md) for notes on 4,5.

## Models

We have

## Optimizers

GA, SA,PSO, DE, etc etc.

## Performance Measures

### HyperVolume

In the following 2d optimization space, which optimizer do you like?

- Hint: we want to minimize dollars and maximize Q(W)

<img width=500 src="http://thermalscienceapplication.asmedigitalcollection.asme.org/data/Journals/JTSEBV/934703/tsea_008_02_021022_f005.png">

The volume inside the paretor frontiers is called the _hypervolume_ and the optimizer
we like has the greatest _hypervolume_ (in this case, the green). Note that there
many hypervolume calculators, some of which has problems when the number of objectives
get very large.

- In [Python](https://github.com/ai-se/Spread-HyperVolume).
- In ["R"](https://github.com/cran/hypervolume)

Note that the _more_ the hypervolume, the _better_.

### Spread

In the following 2d optimization space, which optimizer do you like?

- Hint: we want to minimize all objectives
- The left hand side plot _seems_ to have lower hypervolumes. But is there anything
we do not like about the middle and right-hand-side plots?

<img width=600 src="../img/spread.png">

The middle and right-hand side solutions are not very _spread_ (huge gaps in the frontier).

Calculating spread: 

<img width=300 src="http://mechanicaldesign.asmedigitalcollection.asme.org/data/Journals/JMDEDB/27927/022006jmd3.jpeg">

- Ignoring everything except the Pareto frontier.
- Find the distances to the last two most distance points to their
  nearest neighbor: _d<sub>f</sub>_ and
  _d<sub>l</sub>_
- Find the distance between all pints and their nearest neighbor _d<sub>i</sub>_ and
  their nearest neighbor
  - Then:
  
<img width=300 src="../img/spreadcalc.png">

- If all data is maximally spread, then all distances _d<sub>i</sub>_ are near mean d
which would make _&Delta;=0_ ish.

Note that _less_ the spread of each point to its neighbor, the _better_.

### IGD

Which is better? Spread or hypervolume? What if they conclude different things?
What if they are insanely slow to calculate? What if there was a better measure?

IGD = inter-generational distance; i.e. how good are you compared to the _best known_?

- Find a _reference set_ (the best possible solutions)
- For each optimizer
      - For each item in its final Pareto frontier
      - Find the nearest item in the reference set


Details:

- Problem1: Optimal reference set may be unobtainable (if the model is very nasty).
      - Solution1: Let every optimizer work on populations of size _"N"_
      - Let the combined Pareto frontier from _"a"_ optimizers, removing duplicates.
      - Down select those _"aN"_ items to the  the best _"N"_ best ones.
	  - Use the resulting space as the reference set
          
- Problem2: How to remove duplicates?
      - Solution2a: exact match on decisions (may not be v.useful for real-valued decisions)
      - Solution2b: from the business users, find the minimum value &epsilon;	that
	    they can control each decision. Declare two decisions _same_ if they are within
	    &epsilon;.
            
- Problem3: How to down select?
      - Solution3: count how many times each item in _"aN"_ dominates something else.
      - Keep just the _"N"_ items with highest domination count.
      
- Problem3a: with _binary domination_, many things may have the highest domination
	    count, especially when dealing with high dimensional objections.
      - Solution 3a1: Delete at random from most crowded
	    parts of the Pareto frontier. Why? Cause in crowded spaces, many decisions give
	    rise to the same objective scores.
	  - Solution 3a2: Don't use _binary domination_. Instead, use _continuous domination_
	    since, usually, cdom rejects one item in the comparison. So in this approach,
	    sort each item by the sum of how much it _losses_ to everyone else. They
		pick the _"N"_ that lose least.
                
- Problem 3a1a: How to compute "crowded"
      - Select all candidates that dominate the most number of other candidates.
      - For that set, sort each candidate separately on each objective.
      - On each objective _O<sub>i</sub>_, compute the distance left and right to
	    its nearest neighbor
	  - Let the cuboid around a candidate _V<sub>x</sub>_
	    be the product  _V<sub>x</sub> = &prod;<sub>i</sub>O<sub>i</sub>_
	  - Sort the candidates descending by _V<sub>x</sub>_.
	  - Return the left-most _"N"_ items in that sort.

<img src="../img/crowdcalc.png">

Summary: 
```
optimal known?
  yes: use it
  no:
    combine frontiers from all optimizers
    remove duplications
      epsilon known?
        yes: use near match
        no: use exact match
    downSelect to "N" items
      use binary domination
        yes:
          count how often each one dominates another
          select candidates that dominate the most
          selection > "N"
            no: use selection
            yes:
              sort descending by cubiod distance around them
              use first 1.."N"
        no:
          sort each, ascending, from the sum of its losses to all other
          use first "N"
```


### Binary Domination

Candidate one dominates candidate two:

- if at lease one objective score is _better_;
- and none are _worse_.

Note that in the following, each objective knows if it wants to be minimized or maximized.

```python
def more(x,y): return x > y
def less(x,y): return x < y
```

e.g. `objective1.better = more` or `objective2.better = less`  then call the following.


```python
def bdom(x, y, abouts):
  "multi objective"
  x = abouts.objs(x)
  y = abouts.objs(y)
  betters = 0
  for obj in abouts._objs:
    x1,y1 = x[obj.pos], y[obj.pos]
    if obj.better(x1,y1) : betters += 1
    elif x1 != y1: return False # must be worse, go quit
  return betters > 0
```

### Continuous Domination

Binary domination never reports that that one candidate is waaaaaay more
dominated that the other. It only says "true".  Not the most informative!

<img width=300 src="https://s3-eu-west-1.amazonaws.com/ppreviews-plos-725668748/2119733/preview.jpg">

So that as the number of objectives increase, _bdom_ losses to _cdom_.

<a href="../img/cbdom.png"><img width=700 src="../img/cbdom.png"></a>

What _cdom_ does is that it takes the differences between each objective, then
raises it to a exponential factor (so those differences _SHOUT_ louder). From this we compute the mean _loss_
as
travel from _this_ to _that_
versus _that_ to _this_ (and the one we prefer is the one
that _loss_es least).

Formally, this is a domination test across the Pareto frontier.

- First, we normalize _x,y_ to  0..1
- Then we adjust the direction of the comparison depending on
  whether or not we are _minimizing_ that objective.
- Third, we raise the differences _x - y_ to some exponential (i.e.
  the larger the difference, the louder we shout!)
- Lastly, we return the mean loss over all objectives.


```python
def (i):      # return less for minimize and more for maximize
def norm(i,x): # returns (x - lo) / (hi - lo) where lo and hi
               # are the min,max values for objective i

def better(this, that):
  x  = scores[ id(this) ]
  y  = scores[ id(that) ]
  l1 = loss(x,y)
  l2 = loss(y,x)
  return l1 < l2 # this is better than that if this losses least.

def loss(x, y):
  losses= 0
  n = min(len(x),len(y))
  for i,(x1,y1) in enumerate(zip(x,y)):
    x1 = norm(i,x1) # normalization
    y1 = norm(i,y1) # normalization
    losses += expLoss( i,x1,y1,n )
  return losses / n  # return mean loss

def expLoss(i,x1,y1,n):
  "Exponentially shout out the difference"
  w = -1 if minimizing(i) else 1 # adjust for direction of comparison
  return -1*math.e**( w*(x1 - y1) / n ) # raise the differences to some exponent
```  
