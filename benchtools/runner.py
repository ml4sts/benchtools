# module to run benchmarks
import pandas
import yaml # requires pyyaml
from itertools import product
from task import PromptTask
from pathlib import Path

class Bench():
    '''
    '''


    def __init__(self, dir, target_dir):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.tasks = []

        

    def run(self, model):
        '''
        
        '''
        for task in self.tasks:
            task.run(model)

    # possibly private method? 
    def from_txt_csv():
        '''
        load a template from txt and create task objects for each row of a csv
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor

        return self


    def from_yaml(self, yaml_file):
        """
        Load tasks from a YAML file and generate PromptTask objects.

        Parameters
        ----------
        yaml_file : str
            Path to the YAML file containing task templates and values.

        Returns
        -------
        self : Bench
            The Bench instance with tasks populated.
        """
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)

        self.tasks = []

        for entry in data:
            template = entry["template"]  # Extract template
            values_dict = entry["values"]  # Extract values dictionary

            # Generate all possible value combinations using itertools.product
            keys = values_dict.keys()
            value_combinations = product(*values_dict.values())

            # Create a PromptTask for each combination
            for values in value_combinations:
                value_mapping = dict(zip(keys, values))  # Pair keys with values
                filled_prompt = template.format(**value_mapping)  # Format the template
                self.tasks.append(PromptTask(prompt=filled_prompt))  # Store task

        return self
