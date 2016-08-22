





# Homework2

## Active Shooter Exercise.

1. Watch the video

- Go go https://moodle-projects.wolfware.ncsu.edu/enrol/index.php?id=827
- Click on the "Shots Fired On Campus: When Lightning Strikes" button (at bottom). Go to next page.
- Click on the "Enroll me" button. Go to next page.
- Find the text <em>Shots Fired - Student Edition
Please click here in order to veiw the training video. It will take about 50 seconds to load.</em>
- Click on the "here" and watch the 25 minute video

2. Answer these questions

- List two things _not_ to do during an active shooter event.
- List two things _best_ to do during an active shooter event.


## Write Your First Learner: ZeroR

Within `ninja.rc` there are all these learners that accept a training
and test set. E.g.

```
j48() {
	local learner=weka.classifiers.trees.J48
	$Weka $learner -p 0 -C 0.25 -M 2 -t $1 -T $2
}
```
which is called like in `eg3`:

```
eg3 () {
    echo;
    j48 data/weather.arff data/weather.arff
}
```
    
Functions like `j48` accept `arff` files as inputs; e.g.


```
@relation weather

@attribute outlook {sunny, overcast, rainy}
@attribute temperature real
@attribute humidity real
@attribute windy {TRUE, FALSE}
@attribute play {yes, no}

@data
sunny,85,85,FALSE,no
sunny,80,90,TRUE,no
overcast,83,86,FALSE,yes
rainy,70,96,FALSE,yes
rainy,68,80,FALSE,yes
rainy,65,70,TRUE,no
overcast,64,65,TRUE,yes
sunny,72,95,FALSE,no
sunny,69,70,FALSE,yes
rainy,75,80,FALSE,yes
sunny,75,70,TRUE,yes
overcast,72,90,TRUE,yes
overcast,81,75,FALSE,yes
rainy,71,91,TRUE,no
```

These functions generate output like what `eg5` generates:

```
=== Predictions on test data ===

 inst#     actual  predicted error prediction
     1       2:no       2:no       1
     2       2:no       2:no       1
     3      1:yes      1:yes       1
     4      1:yes      1:yes       1
     5      1:yes      1:yes       1
     6       2:no       2:no       1
     7      1:yes      1:yes       1
     8       2:no       2:no       1
     9      1:yes      1:yes       1
    10      1:yes      1:yes       1
    11      1:yes      1:yes       1
    12      1:yes      1:yes       1
    13      1:yes      1:yes       1
    14       2:no       2:no       1
```

So if one were to write a new function, one could add their own function
providing that function read arff files and generated something like the above:

```
zeror() {
  myNewLearner $1 $2
}
```
then that learner could do anything at all as long as it copied the input output.

ZeroR is the world's dumbest classifier. It finds the majority class and
predicts that everything in the test set is that majority.

Your task is to

1. Implement ZeroR. and add it to the
2. Copy `eg10` to, say, `eg11`
3. Add your new learner to the line

```
local learners="j48 jrip nb rbfnet bnet yourLearnerHere";
```

### What to Hand in

Then run `eg11` and hand in the results.


## Write a Table Reader

Create a class `Table` that can read csv files
or arff files, with instance variables

- `row`s: a list
- `cols`: summary objects, one per column

When a `row` is added to a `Table`, then the summaries are updated.  Summary
objects are either `Num`s or `Sym`s.

### Nums

```python
def max(x,y) : return x if x>y else y
def min(x,y) : return x if x<y else y

class Num:
  def __init__(i):
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
```    

### Syms

```python
class Sym:
  def __init__(i):
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
  def ent(i):
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp  
```

### Implement a CSV reader

Don't confuse tables of rows with the details of reading strings from a csv file
and generating cells. 

```python
import string,re

def atoms(lst):
  return map(atom,lst)

def atom(x)  :
  try: return int(x)
  except:
    try:               return float(x)
    except ValueError: return x
    
def rows(file,prep=same):
  with open(file) as fs:
    for line in fs:
      line = re.sub(r'([\n\r\t]|#.*)', "", line)
      row = map(lambda z:z.strip(), line.split(","))
      if len(row)> 0:
         yield prep(row) if prep else row

for row in rows('../data/weather.csv',atoms):
   print(row)
```

### Implement a Table reader

Uses the csv reader to read data, passes it into a table instance, one row
at a time.

As a side-effect of reading that row, the `Num` and `Sym` objects in
`cols` get updated.

### What to hand-in

All your code and the results of
reading [weather.csv](https://github.com/txt/fss16/blob/master/data/weather.csv).

- Print mean and standard deviation of all numeric columns;
- Print mode and entropy of all symbolic columns.
