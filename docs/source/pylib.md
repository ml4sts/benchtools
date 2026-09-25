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


# Library

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
add_task = Task.from_txt_csv('folderbench/tasks/add')
tiny_bench.add_task(add_task)
```

For demo purposes we delete the folder, if it exists, before running. 
```{code-cell} bash
rm  -rf tiniest_demo
```

We create a new folder for a benchmark to store it in the file system
```{code-cell}
tiny_bench.initialize_dir()
tiny_bench.run()
```


```{code-cell} python
pre_built_yml = Bench.from_yaml('listbench/')
pre_built_yml.written
```

we can access individual tasks, for example:

```{code-cell} python
print(pre_built_yml.tasks['product'].variant_values)
```

```
[{'a': 2, 'b': 3}, {'a': 3, 'b': 4}, {'a': 5, 'b': 5}]
```

Make sure `ollama` is running in advence on your system to run the benchmark

```{code-cell}
pre_built_yml.run()
```

Logs will be found in `listbench/logs`


## Runner class
```{eval-rst}
.. automodule:: benchtools.runner
    :members:
```

## Benchmark class
```{eval-rst}
.. autoclass:: benchtools.benchmark.Bench
    :members:
```


## Task class
```{eval-rst}
.. autoclass:: benchtools.task.Task
    :members:
```



## BetterBench
```{eval-rst}
.. autoclass:: benchtools.betterbench.BetterCheckList
    :members:
```