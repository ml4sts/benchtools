---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.15.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---


# BenchTools as a Python Library

```{code-cell}
from benchtools import Bench

tiny_bench = Bench('Tiniest Demo', concept ='a simplest test')
```


```{code-cell}
from benchtools import Task

tt = Task('greeting','Hello','hi', 'contains')
```


```{code-cell}
tiny_bench.add_task(tt)
```


```{code-cell}
response = tt.run()
```


```{code-cell}
tt.score(response)
```


```{code-cell}
tiny_bench.run()
```



## Creating a Benchmark object
<!-- Testing which is better -->
```{eval-rst}
.. automodule:: benchtools.runner
    :members:
```

## Benchmark class
<!-- Testing which is better -->
```{eval-rst}
.. autoclass:: benchtools.runner.Bench
    :members:
```