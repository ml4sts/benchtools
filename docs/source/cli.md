# CLI


We an initialize without tasks

```bash
cd demos
benchtool init testbench -a "to test a simple example" --no-git
```

<!-- this is still needing fix -->
```bash
cd testbench
benchtool add-task ../new_test/ FillIn ../datasets/miscops/
```



```
benchtool run demos/folderbench
```

<!-- The following will grab all docstrings within cli.py -->
```{eval-rst}
.. click:: benchtools.cli:benchtool
   :prog: benchtool 
   :nested: full
   :commands:

```