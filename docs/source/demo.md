# Example

This is an example of installing and then using the `benchtools` for a simple benchmark


##  install from Source

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


See it creates a folder
```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
benchtools

```

Then install: 
::::::{important}
the following command needs to specifically say `benchtools/` for it to be the path; otherwise `benchtools` will try to pull from pypi. Alternatively, `cd benchtools` then `pip install .`
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

Benchrools is packaged with two demos, you can install them to create a copy and explore

```{code-cell} bash
:tags: ["skip-execution"]
benchtool demo list
```

```{code-block} console
folderbench	
listbench
```

`benchtools` supports two formats for storing tasks:
- a list of tasks in a single `.yml` file
- a set of folders with each task having its own. 


Let's examine the folder-based example first: 

```{code-cell} bash
:tags: ["skip-execution"]
benchtool demo install -n folderbench
cd folderbench
```

```{code-cell} bash
:tags: ["skip-execution"]
ls
```

```{code-block} console
README.md  bench_info.yml  custom_scorer.py  multiple_models.yml  runner.yml  tasks 
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
add  multiply  symbols
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


```{code-block} console
:filename: values.csv
a,b,reference
2,3,5
4,5,9
8,9,17
```

:::::{important}
The columns in the csv match the variables in `{}` in the template, plus a `reference` column for the answer (this can be empty, but the heading should be there), and optionally an `id` if you have an alternative naming scheme for the subtasks (each row is a subtask)
:::::::

we can look at the other task too:


```{code-cell} console
:filename: sybmols/template.txt 
what is the name for the following symbol? {symb}
```



```{code-block}  console
:filename: symbols/values.csv 
symb, reference, exmeta
@, at, email
#, pound, number
$, dollar sign, currency
```


:::::{notice}
`exmeta` here is an additional refernence for the values that will be shown in the logs and could be used later by the user in the custom scorer
:::::::

## Running a benchmark

let's install the other benchmark to run it
```{code-cell} bash
:tags: ["skip-execution"]
benchtool demo install -n listbench
```


We can see the help for the command


```{code-block} bash
:tags: ["skip-execution"]
benchtool run --help
```

```{code-cell} console
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


We can run a benchmark by name

::::{note}
The default runner is ollama. Make sure `ollama` is running in advence.
:::::::

```{code-cell} bash
:tags: ["skip-execution"]
benchtool run listbench/
```

```{code-block} console
Running list_bench now

```

:::::{warning}
When a run CLI command (or library method) is called for a benchmark. The status of the benchmark will be automatically commited and the commit hash will be included in the logs if the benchmark was a repository to ensure repeatability
:::::::



```{code-cell} bash
:tags: ["skip-execution"]
cd listbench/
:tags: ["skip-execution"]
ls
```

```{code-block} console
bench_info.yml  custom_response.py  custom_scorer.py  logs  runner.yml  tasks.yml

```

it creates a `logs` folder if one does not already exist


### Exploring a yaml benchmark
```{code-cell} console
:filename tasks.yml 
- name: product
  template: "find the product of {a} and {b}"
  values:
     a: [2,3,5]
     b: [3,4,5]
  reference: calculated
  scorer: "calculated_answer"
  format: "IntAnswer"
- name: product_combination
  template: "find the product of {a} and {b}"
  values:
     a: [2,3,5]
     b: [3,4,5]
  reference: calculated
  value_combinations: combinations
  scorer: 
    - calculated_answer
    - add_justify
  format: "IntJustification"
- name: symbol
  template: "what is the name for the following symbol? {symb}"
  values: 
     symb: ["@","$","#"]
     exmeta: ['internet', 'world', 'internet']
  reference: ["at", "dollar sign", "pound"]
  scorer: "contains"
- name: symbol_dir
  template: "what direction does the {symb} symbol point? and what is its name "
  values: 
     symb: ["^","<",">"]
     name: [carat, less,greater]
     direction: ["up", "left", "right"]
  scorer: check_name_dir
  reference: calculated
  format: NameSource
```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/
```

```{code-block} console
task_product  task_product_combination  task_symbol  task_symbol_dir

```

there will be a folder per task

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/task_product/
```

```{code-block} console
qwen.qwen3-32b-v1:0
```
then per LLM

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/task_product/qwen.qwen3-32b-v1:0
```

```{code-block} console
1783715070_1783715082
```

then per run, named by the timestamp of the run start

:::::{notice}
There are two timestamps here. The first one refers to the entire benchmark run timestamp whereas the second one is the timestamp of running the specific task from the benchmark run. This way we can group multiple task run together by the benchmark's run timestamp
:::::::

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/task_product/qwen.qwen3-32b-v1:0/1783715070_1783715082
```

```{code-block} console
product_2-3	product_3-4	product_5-5	run_info.yml

```

```{code-cell} bash
:tags: ["skip-execution"]
cat logs/task_product/qwen.qwen3-32b-v1:0/1783715070_1783715082/run_info.yml 
```

```{code-block} console
api: ''
bench_name: listbench
bench_path: listbench
bench_run_id: '1783715070'
commit_hash: null
commit_message: null
concept: simple example of a benchmark defined by a task list in a yaml file, includes
  custom scoring and reponse types
description: "a template based task with template: find the product of {a} and {b} and values like:\n\
  \n |    |   a |   b |   reference |\n|---:|----:|----:|------------:|\n|  0 |  \
  \ 2 |   3 |           6 |\n|  1 |   3 |   4 |           12 |\n|  2 |   5 |   5 |\
  \          25 |"
format: IntAnswer
id_generator: concatenator_id_generator
inference_parameters: null
log_path: listbench/logs/task_product
model: qwen.qwen3-32b-v1:0
name: product
reference:
  product_2-3: 6
  product_3-4: 12
  product_5-5: 25
  runner_type: bedrock
scorer: exact_match
task_run_id: '1783715070_1783715082'
task_timestamp: '1783715082'
template: find the product of {a} and {b}
values:
values:
- a: 2
  b: 3
  prompt_id: product_2-3
- a: 3
  b: 4
  prompt_id: product_3-4
- a: 5
  b: 5
  prompt_id: product_5-5

```
it stored overall information for the run

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/task_product/qwen.qwen3-32b-v1:0/1783715070_1783715082/product_2-3/
```

```{code-block} console
log.json	log.txt

```

and a log for each prompt in both text and json format. The json file includes more details about the subtask and its metadata whereas the text file holds only a prompt and a response to simulate a conversation thread
```{code-cell} bash
:tags: ["skip-execution"]
cat logs/task_product/qwen.qwen3-32b-v1:0/1783715070_1783715082/product_2-3/log.txt 
```

```{code-block} console
------ prompt ------
find the product of 2 and 3

------ response ------
{
  "answer": 6
}

```

```{code-cell} bash
:tags: ["skip-execution"]
cat logs/task_product/qwen.qwen3-32b-v1:0/1783715070_1783715082/product_2-3/log.json 
```

```{code-block} console
{
    "task_name": "product",
    "template": "find the product of {a} and {b}",
    "steps": {
        "0": {
            "prompt_id": "product_2-3",
            "prompt": "find the product of 2 and 3",
            "values": {
                "a": 2,
                "b": 3,
                "prompt_id": "product_2-3"
            },
            "format": {
                "properties": {
                    "answer": {
                        "title": "Answer",
                        "type": "integer"
                    }
                },
                "required": [
                    "answer"
                ],
                "title": "IntAnswer",
                "type": "object"
            },
            "response": "{\n  \"answer\": 6\n}",
            "error": null,
            "prompt_tokens": 21,
            "response_tokens": 10,
            "total_tokens": 31,
            "stop_reason": "end_turn"
        }
    }
}
```

## Initializing a new benchmark

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
  demo      demo benchmarks package with benchtools
  init      Initializes a new benchmark.
  run       Run the benchmark, generate logs, and optionally sore
  run-task  Running the tasks and generating logs
  score     Running the benchmark and generating logs Parameters:...

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

it asks questions interactively
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

Let's mannually edit the task to make a good example.
```{code-cell} bash
:tags: ["skip-execution"]
nano tasks.yml 

```

```{code-block} console
- description: 'animal identifcaiton '
  format: StringAnswer
  id_generator: concatenator_id_generator
  name: animal
  reference: ['zebra', 'tiger', "cheetah"]
  scorer: contains
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
```

```{code-block}
about.md	info.yml	tasks.yml

```


```{code-cell} bash
:tags: ["skip-execution"]
benchtool run .
```

Let's see what happened after running the benchmark

```{code-cell} bash
:tags: ["skip-execution"]
ls

```

```{code-block}
about.md	info.yml	logs tasks.yml
```

Now we have a new `logs/` folder. Let's explore its contents 
```{code-cell} bash
:tags: ["skip-execution"]
ls logs/
```

```{code-block} 
gemma3
```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/
```

```{code-block} 
animal
```

```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/animal
```

```{code-block} 
1780063281
```

`1780063281` is the timestamp of when the benchmark was run which represents a single run of the benchmark


```{code-cell} bash
:tags: ["skip-execution"]
ls logs/gemma3/animal/1780063281
```


```{code-block} 
animal_spots-hairy-paws  animal_stripes-hairy-hooves  animal_stripes-hairy-paws  run_info.yml
```

Each run will have a folder for the different subtasks  


Let's run the scorer to score the LLM on the task at hand.

```{code-cell} bash
:tags: ["skip-execution"]
benchtool score .
```

```{code-block} console
Saved Eval: ./eval_1780069448
```

```{code-cell} bash
:tags: ["skip-execution"]
cat ./eval_1780069448.json
```

```{code-block} console
[{"task_name": "animal", "template": "an animal has a {pattern}, {feet}, and {skin}. what kind of animal is it?", "prompt_id": "animal_spots-hairy-paws", "error": "None", "values": {"pattern": "spots", "skin": "hairy", "feet": "paws", "prompt_id": "animal_spots-hairy-paws"}, "steps": {"0": {"prompt": "an animal has a spots, paws, and hairy. what kind of animal is it?", "response": "{\n    \"answer\": \"A dog\"\n}\n", "score": 0}}, "model": "gemma3", "task": "animal", "run": "1780063281"}, {"task_name": "animal", "template": "an animal has a {pattern}, {feet}, and {skin}. what kind of animal is it?", "prompt_id": "animal_stripes-hairy-hooves", "error": "None", "values": {"pattern": "stripes", "skin": "hairy", "feet": "hooves", "prompt_id": "animal_stripes-hairy-hooves"}, "steps": {"0": {"prompt": "an animal has a stripes, hooves, and hairy. what kind of animal is it?", "response": "{\n  \"answer\": \"A zebra!\"\n}", "score": 1}}, "model": "gemma3", "task": "animal", "run": "1780063281"}, {"task_name": "animal", "template": "an animal has a {pattern}, {feet}, and {skin}. what kind of animal is it?", "prompt_id": "animal_stripes-hairy-paws", "error": "None", "values": {"pattern": "stripes", "skin": "hairy", "feet": "paws", "prompt_id": "animal_stripes-hairy-paws"}, "steps": {"0": {"prompt": "an animal has a stripes, paws, and hairy. what kind of animal is it?", "response": "{\n  \"answer\": \"A zebra!\"\n}\n", "score": 0}}, "model": "gemma3", "task": "animal", "run": "1780063281"}]
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

