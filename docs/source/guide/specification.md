# Example Files


## Task List


An example `task.yml` file: 

:::{literalinclude} ../../../benchtools/assets/demos/listbench/tasks.yml
:language: yaml
:linenos:
:caption: tasks.yml
:::

## Folder specified Task

It comprises a text file for the template

:::{literalinclude} ../../../benchtools/assets/demos/folderbench/tasks/add/template.txt
:caption: template.txt
:::

and then values for the template feilds are in a csv file:

:::{literalinclude} ../../../benchtools/assets/demos/folderbench/tasks/add/values.csv
:caption: values.csv
:::

<!-- :lines: 1-8 -->

## Runner Specification


### Single run settings

:::{literalinclude} ../../../benchtools/assets/demos/folderbench/runner.yml
:linenos:
:language: yaml
:caption: runner.yml
:::


### Specifying multiple models: 

:::{literalinclude} ../../../benchtools/assets/demos/folderbench/multiple_models.yml
:linenos:
:language: yaml
:caption: multiple_models.yml
:::


## Custom Response format

Classes should be like those in the [responses](response.md) class. Use `pydantic.BaseModel` for the response formats an `enum.Enum` to restrict options. 

:::{literalinclude} ../../../benchtools/assets/demos/listbench/custom_response.py
:linenos:
:language: python
:caption: custom_response.py
:lines: 1-2
:::


In order to constrain options, create a class for that: 
:::{literalinclude} ../../../benchtools/assets/demos/listbench/custom_response.py
:linenos:
:language: python
:caption: custom_response.py
:lines: 4-7
:::


Then that can be a field in a response. 
:::{literalinclude} ../../../benchtools/assets/demos/listbench/custom_response.py
:linenos:
:language: python
:caption: custom_response.py
:lines: 9-11
:::

## Custom Scorer

For custom scoring, add a file `custom_scorer.py`.  There can be multiple functions in one file.  A function should take two inputs, the `response` and the `reference`.  

If `reference` is set to "calculated" in the `tasks.yml` for list-style or  `info.yml` for a folder-style, then the `reference` will be a dictionary of the values for the class, with the `prompt_id` added. 


:::{literalinclude} ../../../benchtools/assets/demos/listbench/custom_scorer.py
:linenos:
:language: python
:caption: custom_scorer.py
:::

The function can return either a scalar numerical value or a dictionary for multiple values. 