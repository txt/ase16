
# Things to Notes on "ase.py"

This document is introductory notes of
[ase.py](ase.py), some sample Python code that
lets us teach model-based methods to newbs.

## Things to Notice

- Global vs local variables
- Multiple assignments, transposing variables
- initializing lists, dictionaries
- ternary operators 
- functions can be named at load time
- or set as variables in _lambda_ bodies.
- Strings can be simple, or multi-line

     """
     Multi-line 
     string
     """

- Functions:
      - inputs: args, defaults, variable length arguments `\*l`, `\*\*d`
      - outputs: multi-valued returns
      - return vs yield https://github.com/crista/exercises-in-programming-style/blob/master/27-lazy-rivers/tf-27.py

```
def simple_generator_function():
    yield 1
    yield 2
    yield 3
```
    
And here are two simple ways to use it:

```
for value in simple_generator_function():
     print(value)
```

Some examples

```
def evens(lst):
   for n in lst:
     if n % 2 == 0:
        yield n
```

E.g. for all non-blank lines do:

```
def csvRows(file):
  with open(file) as fs:
    for line in fs:
        line = re.sub(r'([\n\r\t]|#.*)', # kill white space
                      "", line)
        cells = line.split(",")  # split ","
        row = map(lambda z:z.strip(), cells) # zap wrapping white space
        if len(row)> 0:
           yield row

for row in csvRows(file):
  -- do something
```

Note that the `row` is generated one-at-a-time (so entire file
never read into RAM.




