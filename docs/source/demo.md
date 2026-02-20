# Demo Usage 




##  install

Installing from source means you can pull to update. 

First, clone the repo: 

```{code-cell} bash
:tags: ["skip-execution"]
git clone https://github.com/ml4sts/benchtools.git
```

```{code-block} console
Cloning into 'benchtools'...
remote: Enumerating objects: 908, done.
remote: Counting objects: 100% (277/277), done.
remote: Compressing objects: 100% (165/165), done.
remote: Total 908 (delta 145), reused 170 (delta 83), pack-reused 631 (from 2)
Receiving objects: 100% (908/908), 2.34 MiB | 405.00 KiB/s, done.
Resolving deltas: 100% (513/513), done.

```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
benchtools

```

Then install: 
::::::{important}
this needs to be `benchtools/` for it to be the path; `benchtools` will pull from pypi. Alternatively, `cd benchtools` then `pip install .`
:::::::
```{code-cell} bash
:tags: ["skip-execution"]
pip install benchtools/
```

```{code-block} console
Processing ./benchtools
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: click in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (8.3.0)

Successfully built benchtools
Installing collected packages: benchtools
  Attempting uninstall: benchtools
    Found existing installation: benchtools 0.2.0
    Uninstalling benchtools-0.2.0:
      Successfully uninstalled benchtools-0.2.0
Successfully installed benchtools-0.2.0

```
::::{note}
the above is truncated, but the last few lines are the most important
:::::::

## Exploring the Demo benchmarks

we have two tiny demo benchmarks in a demos folder: 

```{code-cell} bash
:tags: ["skip-execution"]
cd benchtools/demos/
ls
```

```{code-block} console
folderbench	listbench
```

`benchtools` supports two formats for storing tasks:
- a list of tasks in a single `.yml` file
- a set of folders with each task having its own. 


Let's examine the folder-based example first: 

```{code-cell} bash
:tags: ["skip-execution"]
cd folderbench/
```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
README.md	tasks
```

The tasks folder is the main content: 
```{code-cell} bash
:tags: ["skip-execution"]
cd tasks/
:tags: ["skip-execution"]
ls
```

it has two tasks, one folder for each
```{code-block} console
add	symbols
```

We can look inside one: 
```{code-cell} bash
:tags: ["skip-execution"]
cd add/
ls
```

it has two files: a template and values
```{code-block} console
template.txt	values.csv
```


```{code-block} console
:filename: template.txt
what is {a} + {b}?
```

```{code-cell} bash
:tags: ["skip-execution"]
cat values.csv 
```

```{code-block} console
:filename: values.csv
a,b,reference
2,3,5
4,5,9
8,9,17
```

:::::{important}
The columns in the csv match the variables in `{}` in the template, plus a `reference` column for the answer (this can be empty, but the heading should be there)
:::::::

we can look at the other task too:
```{code-cell} bash
:tags: ["skip-execution"]
cd ../symbols/

```

```{code-cell} bash
:tags: ["skip-execution"]
cat template.txt 
```

```{code-block} console
what is the name for the following symbol? {symb}
```

```{code-cell} bash
:tags: ["skip-execution"]
cat values.csv 
```

```{code-block} console 
symb, reference
@, at
#, pound
\$, dollar sign
```

```{code-cell} bash
:tags: ["skip-execution"]
cd ../../../
```




```{code-cell} bash
:tags: ["skip-execution"]
benchtool run --help
```

```{code-block} console
Usage: benchtool run [OPTIONS] BENCHMARK_PATH

  Running the benchmark and generating logs , help="The path to the benchmark
  repository where all the task reside."

Options:
  -r, --runner-type [ollama|openai|aws]
                                  The engine that will run your LLM.
  -m, --model TEXT                The LLM to be benchmarked.
  -a, --api-url TEXT              The api call required to access the runner
                                  engine.
  -l, --log-path TEXT             The path to a log directory.
  --help                          Show this message and exit.

```

:::::{warning}
this will be filled in later
:::::::

```{code-cell} bash
:tags: ["skip-execution"]
benchtool run listbench/
```

```{code-block} console
Running list_bench now

```

```{code-cell} bash
:tags: ["skip-execution"]
cd listbench/
```

```{code-block} console

```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
info.yml	logs		tasks.yml

```

```{code-cell} bash
:tags: ["skip-execution"]
cat tasks.yml 
```

```{code-block} console
- name: product
  template: "find the product of {a} and {b}"
  values:
     a: [2,3,5]
     b: [3,4,5]
  reference: [6,12,25]
  scorer: "exact_match"
- name: symbol
  template: "what is the name for the following symbol? {symb}"
  values: 
     symb: ["@","$","#"]
  reference: ["at", "dollar sign", "pound"]
  scorer: "contains"
```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/
```

```{code-block} console
gemma3

```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/
```

```{code-block} console
product	symbol

```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/product/
```

```{code-block} console
1771533769

```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/product/1771533769/
```

```{code-block} console
product_2-3	product_3-4	product_5-5	run_info.yml

```

```{code-cell} bash
:tags: ["skip-execution"]
cat logs/gemma3/product/1771533769/run_info.yml 
```

```{code-block} console
bench_name: list_bench
bench_path: listbench/
description: null
id_generator: concatenator_id_generator
log_path: listbench/logs/gemma3/product/1771533769
name: product
reference:
- 6
- 12
- 25
run_id: '1771533769'
scorer: exact_match
template: find the product of {a} and {b}
values:
- a: 2
  b: 3
- a: 3
  b: 4
- a: 5
  b: 5

```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/product/1771533769/product_2-3/
```

```{code-block} console
log.json	log.txt

```

```{code-cell} bash
:tags: ["skip-execution"]
cat logs/gemma3/product/1771533769/product_2-3/log.txt 
```

```{code-block} console
------ prompt ------
find the product of 2 and 3

------ response ------
The product of 2 and 3 is 2 * 3 = 6.

So the answer is $\boxed{6}$.


```

```{code-cell} bash
:tags: ["skip-execution"]
cat logs/gemma3/product/1771533769/product_2-3/log.json 
```

```{code-block} console
{
    "task_name": "product",
    "template": "find the product of {a} and {b}",
    "prompt_name": "product_2-3",
    "error": "None",
    "steps": {
        "0": {
            "prompt": "find the product of 2 and 3",
            "response": "The product of 2 and 3 is 2 * 3 = 6.\n\nSo the answer is $\\boxed{6}$."
        }
    }
}
```



```{code-cell} bash
:tags: ["skip-execution"]
benchtool
```

```{code-block} console
Usage: benchtool [OPTIONS] COMMAND [ARGS]...

  BenchTools is a tool that helps researchers set up benchmarks.

Options:
  --help  Show this message and exit.

Commands:
  add-task  Set up a new task.
  init      Initializes a new benchmark.
  run       Running the benchmark and generating logs , help="The path to...
  run-task  Running the tasks and generating logs

```

```{code-cell} bash
:tags: ["skip-execution"]
benchtool init --help
```

```{code-block} console
Usage: benchtool init [OPTIONS] [BENCHMARK_NAME]

  Initializes a new benchmark.

  Benchmark-name is required, if not provided, requested interactively.

  this command creates the folder for the benchmark.

Options:
  -p, --path TEXT   The path where the new benchmark repository will be placed
  -a, --about TEXT  Benchmark describtion. Content will go in the about.md
                    file
  --no-git          Don't make benchmark a git repository. Default is False
  --help            Show this message and exit.

```

```{code-cell} bash
:tags: ["skip-execution"]
benchtool init example --about 'in class example benchmark'
Do you want to add any tasks now? [y/N]: y
Do you have task files already prepared? [y/N]: N
What type of template would you like to add? (csv, yaml): yaml
what is the name of your task?: animal
Do you want to add another? [y/N]: N
Creating example Benchmark in ./example
Created example benchmark successfully!
Do you want to go through the BetterBench checklist now? [Y/n]: n
Do you want to run the benchmark now? [Y/n]: n

```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
benchtools	example

```

```{code-cell} bash
:tags: ["skip-execution"]
cd example/
```

```{code-block} console

```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
about.md	info.yml	tasks

```

```{code-cell} bash
:tags: ["skip-execution"]
cat info.yml 
```

```{code-block} console
bench_name: example
concept: in class example benchmark
tasks:
- id: animal
  name: animal
  storage_type: yaml

```

```{code-cell} bash
:tags: ["skip-execution"]
cat tasks.yml 
```

```{code-block} console
- description: 'give your task a short description '
  id_generator: concatenator_id_generator
  name: animal
  reference: ''
  scorer: exact_match
  template: Your {noun} for the model here with values that should vary              denoted
    in brackets. {verb} matching  keys below
  values:
    noun:
    - text
    - task
    verb:
    - use
    - select

```

```{code-cell} bash
:tags: ["skip-execution"]
nano tasks.yml 

```

```{code-block} console
- description: 'animal identifcaiton '
  id_generator: concatenator_id_generator
  name: animal
  reference: ['zebra', 'tiger', "cheetah"]
  scorer: exact_match
  template: an animal has a {pattern}, {feet}, and {skin}. what kind of animal is it?
  values:
    pattern:
    - stripes
    - stripes
    - spots
    skin:
    - hairy
    - hairy
    - hairy
    feet: 
    - hooves
    - paws
    - paws
```


```{code-cell} bash
:tags: ["skip-execution"]
ls
about.md	info.yml	tasks.yml

```



```{code-cell} bash
:tags: ["skip-execution"]
benchtool run .
```


## Get updates

::::{tip}
Watch the repo to get notifications for important updates
::::

Then update by pulling 

```{code-cell} bash
:tags: ["skip-execution"]
cd benchtools/
git pull
```

and re-installing: 


```{code-cell} bash
:tags: ["skip-execution"]
pip install .
```

```{code-block} console

Processing /Users/brownsarahm/Documents/inclass/benchmarks/benchtools
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Requirement already satisfied: click in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (8.3.0)
Requirement already satisfied: datasets in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (4.5.0)
Requirement already satisfied: ollama in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (0.6.1)
Requirement already satisfied: openai in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (2.21.0)
Requirement already satisfied: pandas in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (2.3.2)
Requirement already satisfied: pyyaml in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from benchtools==0.2.0) (6.0.3)
Requirement already satisfied: filelock in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (3.20.0)
Requirement already satisfied: numpy>=1.17 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (2.3.3)
Requirement already satisfied: pyarrow>=21.0.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (23.0.0)
Requirement already satisfied: dill<0.4.1,>=0.3.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (0.4.0)
Requirement already satisfied: requests>=2.32.2 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (2.32.4)
Requirement already satisfied: httpx<1.0.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (0.28.1)
Requirement already satisfied: tqdm>=4.66.3 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (4.67.1)
Requirement already satisfied: xxhash in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (3.6.0)
Requirement already satisfied: multiprocess<0.70.19 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (0.70.18)
Requirement already satisfied: fsspec<=2025.10.0,>=2023.1.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (2025.10.0)
Requirement already satisfied: huggingface-hub<2.0,>=0.25.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (1.4.1)
Requirement already satisfied: packaging in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from datasets->benchtools==0.2.0) (25.0)
Requirement already satisfied: aiohttp!=4.0.0a0,!=4.0.0a1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (3.13.3)
Requirement already satisfied: anyio in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from httpx<1.0.0->datasets->benchtools==0.2.0) (4.11.0)
Requirement already satisfied: certifi in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from httpx<1.0.0->datasets->benchtools==0.2.0) (2025.10.5)
Requirement already satisfied: httpcore==1.* in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from httpx<1.0.0->datasets->benchtools==0.2.0) (1.0.9)
Requirement already satisfied: idna in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from httpx<1.0.0->datasets->benchtools==0.2.0) (3.10)
Requirement already satisfied: h11>=0.16 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from httpcore==1.*->httpx<1.0.0->datasets->benchtools==0.2.0) (0.16.0)
Requirement already satisfied: hf-xet<2.0.0,>=1.2.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (1.2.0)
Requirement already satisfied: shellingham in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (1.5.4)
Requirement already satisfied: typer-slim in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (0.23.1)
Requirement already satisfied: typing-extensions>=4.1.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (4.15.0)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (2.6.1)
Requirement already satisfied: aiosignal>=1.4.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (25.3.0)
Requirement already satisfied: frozenlist>=1.1.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (6.7.1)
Requirement already satisfied: propcache>=0.2.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (0.4.1)
Requirement already satisfied: yarl<2.0,>=1.17.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from aiohttp!=4.0.0a0,!=4.0.0a1->fsspec[http]<=2025.10.0,>=2023.1.0->datasets->benchtools==0.2.0) (1.22.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from requests>=2.32.2->datasets->benchtools==0.2.0) (3.4.2)
Requirement already satisfied: urllib3<3,>=1.21.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from requests>=2.32.2->datasets->benchtools==0.2.0) (2.5.0)
Requirement already satisfied: sniffio>=1.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from anyio->httpx<1.0.0->datasets->benchtools==0.2.0) (1.3.1)
Requirement already satisfied: pydantic>=2.9 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from ollama->benchtools==0.2.0) (2.12.5)
Requirement already satisfied: annotated-types>=0.6.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pydantic>=2.9->ollama->benchtools==0.2.0) (0.7.0)
Requirement already satisfied: pydantic-core==2.41.5 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pydantic>=2.9->ollama->benchtools==0.2.0) (2.41.5)
Requirement already satisfied: typing-inspection>=0.4.2 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pydantic>=2.9->ollama->benchtools==0.2.0) (0.4.2)
Requirement already satisfied: distro<2,>=1.7.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from openai->benchtools==0.2.0) (1.9.0)
Requirement already satisfied: jiter<1,>=0.10.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from openai->benchtools==0.2.0) (0.13.0)
Requirement already satisfied: python-dateutil>=2.8.2 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pandas->benchtools==0.2.0) (2.9.0.post0)
Requirement already satisfied: pytz>=2020.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pandas->benchtools==0.2.0) (2025.2)
Requirement already satisfied: tzdata>=2022.7 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from pandas->benchtools==0.2.0) (2025.2)
Requirement already satisfied: six>=1.5 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from python-dateutil>=2.8.2->pandas->benchtools==0.2.0) (1.17.0)
Requirement already satisfied: typer>=0.23.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (0.23.1)
Requirement already satisfied: rich>=10.11.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from typer>=0.23.1->typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (14.3.2)
Requirement already satisfied: annotated-doc>=0.0.2 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from typer>=0.23.1->typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (0.0.4)
Requirement already satisfied: markdown-it-py>=2.2.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from rich>=10.11.0->typer>=0.23.1->typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (3.0.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from rich>=10.11.0->typer>=0.23.1->typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (2.19.2)
Requirement already satisfied: mdurl~=0.1 in /Users/brownsarahm/miniforge3/lib/python3.12/site-packages (from markdown-it-py>=2.2.0->rich>=10.11.0->typer>=0.23.1->typer-slim->huggingface-hub<2.0,>=0.25.0->datasets->benchtools==0.2.0) (0.1.2)
Building wheels for collected packages: benchtools
  Building wheel for benchtools (pyproject.toml) ... done
  Created wheel for benchtools: filename=benchtools-0.2.0-py3-none-any.whl size=25379 sha256=cbaa73c7bbd64125d8066422631e6e44b30cc5e3b56af606d509a768cf1fe708
  Stored in directory: /private/var/folders/kj/kqly3_f917189vwrjg18kgvh0000gn/T/pip-ephem-wheel-cache-ebxkovdj/wheels/10/8a/b7/122083acfdf1e043b6947b84186debcd103f8f527cb995787a
Successfully built benchtools
Installing collected packages: benchtools
  Attempting uninstall: benchtools
    Found existing installation: benchtools 0.2.0
    Uninstalling benchtools-0.2.0:
      Successfully uninstalled benchtools-0.2.0
Successfully installed benchtools-0.2.0

```

```{code-cell} bash
:tags: ["skip-execution"]
ls
benchtools	example

```

```{code-cell} bash
:tags: ["skip-execution"]
benchtool run example/
Running example now

```

```{code-cell} bash
:tags: ["skip-execution"]
cd benchtools/

```

