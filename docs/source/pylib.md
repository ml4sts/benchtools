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

<!-- Doesn't really run anything 
File "/work/pi_brownsarahm_uri_edu/ayman_uri/BenchTools/benchtools/benchtools/task.py", line 497, in run
    for (prompt_id, prompt),values in zip(id_prompt_list,self.variant_values):
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not iterable
 -->

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
add_task = Task.from_txt_csv('benchtools/assets/demos/folderbench/tasks/add')
tiny_bench.add_task(add_task)
```

For demo purposes we delete the folder, if it exists, before running. 
```{code-cell} bash
rm  -rf tiniest_demo
```

<!-- Same problem with run -->

We create a new folder for a benchmark to store it in the file system
```{code-cell}
tiny_bench.initialize_dir()
tiny_bench.run()
```


```{code-cell}
pre_built_yml = Bench.from_yaml('benchtools/assets/demos/listbench')
pre_built_yml.written
```

we can access individual tasks:

```{code-cell}
pre_built_yml.tasks['product'].variant_values
```

```
[{'a': 2, 'b': 3}, {'a': 3, 'b': 4}, {'a': 5, 'b': 5}]
```

Make sure you have `ollama serve` running to run the benchmark

```{code-cell}
pre_built_yml.run()
```

Logs will be found in `benchtools/assets/demos/listbench/logs`


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