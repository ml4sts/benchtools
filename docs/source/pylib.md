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

## A tiny example

we can create a tiny benchmark programmatically
```{code-cell}
from benchtools import Bench

tiny_bench = Bench('Tiniest Demo', concept ='the simplest test')
```

we can also create a simple task programmatically
```{code-cell}
from benchtools import Task

tt = Task('greeting','Hello there','hi', 'contains')
```
<!-- there -->

```{code-cell}
response = tt.run()
```

```{code-cell}
tt.score(response)
```

```{code-cell}
tiny_bench.add_task(tt)
```

There are multiple ways to creating a Task object
```
add_task = Task.from_txt_csv('../../demos/folderbench/tasks/add')
tiny_bench.add_task(add_task)
```

For demo purposes we delete the folder, if it exists, before running. 
```{code-cell}
%%bash
rm  -rf tiniest_demo
```

We create a new folder for a benchmark to store it in the file system
```{code-cell}
tiny_bench.initialize_dir()
tiny_bench.run()
```


```{code-cell}
pre_built_yml = Bench.from_yaml('../../demos/listbench')
pre_built_yml.written
```

we can access individual tasks:

```{code-cell}
pre_built_yml.tasks['product'].variant_values
```



```{code-cell}
pre_built_yml.run()
```

```{code-cell}
demo_bench = Bench.from_yaml('../../demos/listbench')
```


<!-- ```{code-cell}
demo_bench = Bench.load('../../demobench')
``` -->





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