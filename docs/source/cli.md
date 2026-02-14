# CLI


```bash
benchtool init new_test -p . -t add ../datasets/add/ -t Gaps ../datasets/miscops/ -a "this is a demo for benchtools"
```

```bash
benchtool add-task ../new_test/ FillIn ../datasets/miscops/
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