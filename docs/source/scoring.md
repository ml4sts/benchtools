# Scoring and Evaluation


You can set a scorer as one of the builtin or a custom one. 

To use a custom function include a file named `custom_scorer.py` and include a function that takes in:
- response: will be a string, formatted according to the `format` key
- reference: either the reference answer provided or the values used if `reference: calculated` in the setup

:::::{tip}
see the `product` task in the `listbench` demo for an example of custom scoring
:::::::

:::::{warning}
custom scoring not fully implemented for folder tasks, there needs to be a way to specify it and load it. 
:::::::