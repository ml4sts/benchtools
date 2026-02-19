<!-- BenchTools documentation master file, created by
   sphinx-quickstart on Wed Feb 11 16:55:24 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive. -->



# BenchTools

A library for building and running benchmarks


## Install 

You can install  directly from github or after cloning

### diect install 



### By clone

You can clone first
```
git clone https://github.com/ml4sts/benchtools.git
```

and then install 
```
pip install benchtools
```
(possibly `pip3`)

if you clone in order to develop, you may want to install with pip's `-e` option

```
pip install -e benchtools
```

To update, pull and install again. 

## Usage 

benchtools allows you to express templated tasks in multiple ways:
- a yaml format listing the tasks with a values key
- a folder for each task with txt file with template and a csv file of values for variations of the task

a  benchmark can consist of tasks that all fit a single format above or a mixture of meta-tasks each represented as a folder
and then the specific tasks in one of the forms above

There are two main ways to use BenchTools. The user can mix and match between the two methods.

```{toctree}
:caption: Contents:
:maxdepth: 2

cli.md
pylib.md

```


```{eval-rst}
.. click:: benchtools.cli:benchtool
   :prog: benchtools 
   :nested: full
   :commands:

```