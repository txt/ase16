

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

# Homework6: coding homework:  Generic Experiments

NOTE TO STUDENTS: if this homework seems too complex, then reflect
a little more on the prior optimizing
examples.
This code generalizes prior work to
the point where we can quickly write many models and many optimizers.
So it actually _simplifies_ the optimization process.... at the
cost of some extra architecture.

## What to Hand in


From the following, show the output of running sa, mws on Schaffer, Osyczka2, Kursawe.


# To Do

Rewrite your SA and MWS code such that you can run the following loop:

```python
for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [sa, mws]:
           optimizer(model())
```

This is the _generic experiment loop_ that allows for rapid extension to handle more models and more optimizers.

## Tips

### Another Model

The above loops requires the  [Kursawe](models/moeaProblems.pdf) model.

### Optimizer as function

The above code assumes that _mws_, _sa_ are functions that accept one argument: a description of the model they are processing.

### Model as Class

For the above loop to work, each model (e.g. _Schaffer_) has to be class that produces an instance via _model()_.
That model defines:

+ the number of decisions;
+ the number of objectives;
+ the name of each decision/objective;
+ the min/max range of each decision/objective;
+ the _any_ function that scores a candidate
+ the _ok_ function that checks if a particular candidate is valid (for _Schaffer and Kursawe_, this returns _True_ while
for _Osyczka2_, this does some checking).
+ the _eval_ function that computes the objective scores for each candidate


