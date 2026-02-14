# CLI


```
benchtool init new_test -p ../ -t add ../datasets/add/ -t Gaps ../datasets/miscops/ -a "this is a demo for benchtools"
```
```
Creating new_test in ../
Setting up add...Success
Setting up Gaps...Success
Would you like to run the benchmark? y/n? n
```
```
benchtool add-task ../new_test/ FillIn ../datasets/miscops/
```
```
Setting up FillIn...Success
```

```
benchtool run testRuns/111
```

<!-- The following will grab all docstrings within cli.py -->
```{eval-rst}
.. click:: benchtools.cli:benchtool
   :prog: benchtool 
   :nested: full
   :commands:

```