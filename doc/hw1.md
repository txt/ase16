<em>"Because engineering is optimization and optimization is search."</em><br>
[<img width=900 src="https://raw.githubusercontent.com/txt/ase16/master/img/mase16.png">](http://tiny.cc/ase2016)   
[home](http://tiny.cc/ase2016) |
[overview](https://github.com/txt/ase16/blob/master/doc/overview.md) |
[syllabus](https://github.com/txt/ase16/blob/master/doc/syllabus.md) |
[src](https://github.com/txt/ase16/tree/master/src) |
[give](http://tiny.cc/ase16give) |
[chat](https://ase16.slack.com/) |
[&copy;2016](https://github.com/txt/ase16/blob/master/LICENSE.md) tim&commat;menzies.us

______


# Homework1

## Before you begin

- Get your URL shortener going. Go get an account at http://tiny.cc. 
- Get your Github environment going (public github, not ncstate). Add `timm` and
`bigfatnoob` as collaborators  to that repo.
     + The name of that repo should be `fss16xxx` where `xxx` is anything you like.
     + Add directories to that repo as follows

```
project
paper
read   -- all your weeklies readings go here
code/1 -- code for week1.
code/1/README.md : answers to any questions asked this week
code/2
code/3
etc
```

- Get your development environment going. This should be:
       - code that is checked into git and saved,
         regularly to your Gibhub account, and shared with any team members.
       - Some place where you can run Python 2.7.
       - Note that all your team members need to running the same environment (which makes
         c9.io an attractive option).
- Review your team. Ideally, a team should contain at least one moderate expert
  in Python. Got to http://tiny.cc/ase16give and check out
  our random assignments to the teams. Ask for a change if NO ONE on your team is
  expert on the language you are using. If you make a change:
       - mark your people with the same letter in column C, BELOW Row 20
       - add your Gibub url in column B ABOVE row 20

Important note: For this subject, the lecturer and support will support your
Python code on the intenet IDE [Cloud9](http://c9.io).  You can use any other
platform you like, of course, but any systems issues (e.g. installing of
important packages) are your responsibility.

While you do not need to use Cloud9, you do need
to show that you have a _power platform_ for Python development:

+ Check you have `pip` installed
+ Check you have `easy_install` install
+ Check your code editor does syntax highligting of your Python code.

## Read Something

Write a summary of one research paper from 2012 relating to automated software engineering
For more details see [Reading12345678](Reading12345678.md).

## Code Something

### Get your Test-Driven Development On.


1. Watch the great [Kent Beck video on how to write a test engine in just a few lines of code](https://www.youtube.com/watch?v=nIonZ6-4nuU). Note
that that example is in CoffeeScript. For the equivalent Python code, see
[utest.py](../src/utest.py).
2. Get the Python equivalent of the watch command used by Beck. Specifically, run the command
   `sudo pip install rerun`
3. Download the `utest.py`
4. Write a python file `main.py` that imports `utest.py` and code from `who1.py who2.py who3.py`;
   i.e. one file per member of your team.
4. Get two windows open:
	 + One editing main.py
	 + One in a shell
5. In the shell, type `rerun "python -B main.py"`
6. Add one more unittest to `main.py`.
     + Important... leave behind at least one failing test.
     + Save the file. Watch the code run.
 
____

## Working with Cloud9

As of June 2015, the procedure for doing that was:

+ Go to Github and create an empty repository.
+ Log in to Cloud9 using your GitHub username (at `http://c9.io`, there is a button for that, top right).
+ Hit the green _CREATE NEW WORKSPACE_ button
    + Select _Clone from URL_;
    + Find _Source URL_ and enter in `http://github.com/you/yourRepo`
	+ Wait ten seconds for the screen to change.
	+ Hit the green _START EDITING_ button. 

This will drop you into the wonderful Cloud9
integrated development environment. Here, you can
edit code and backed up your code outside Cloud9, over at
`Github.com` (which means that if ever Cloud9 goes
away, you will still have your code).

The good news about Cloud9 is that it is very easy
to setup and configure. The bad news is that each
Cloud9 workspace has the same limits as Github- a
1GB size limit. Also, for CPU-intensive
applications, shared on-line resources like Cloud9
can be a little slow. That said, for the newbie,
Cloud9 is a very useful tool to jump start the
learning process.

For sites other than Cloud9, see Koding, Nitrous.IO and many more besides.


