# module to run benchmarks
import os
import task
import yaml # requires pyyaml
import pandas
from task import PromptTask
from pathlib import Path
from log_file.py import log_agent_interaction
from itertools import product
from log_file.py import log_agent_interaction


class Bench():
    '''
    '''
    def __init__(self, dir, target_dir):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 

        task_folder = os.listdir(dir)
        for file in task_folder:
            if file.endswith("csv"):
                self.tasks = self.from_txt_csv(dir)
            elif file.endswith("yml"):
                self.tasks = self.from_yaml(dir)
        # Both functions should have the same type return. porobably should be a list of PRompt_Task
                    


        

    def run(self, model):
        '''
        

        '''
        for task in self.tasks:
            (prompt, response) = task.run(model)
            log_agent_interaction(prompt, response)
            task.score()






        

    # possibly private method? 
    def from_txt_csv(task_folder):
        '''
        load a template from txt and create task objects for each row of a csv
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor
        textFile = open(task_folder + "task.txt", "r")
        csvFile = pandas.read_csv(task_folder + "values.csv")
        answers = pandas.read_csv(task_folder + "results")

        storedTasks = []
        storedAnswers = []
        for x in range(len(csvFile)):
            processed_prompt = textFile.replace("{a}", csvFile.iloc[x,1])
            processed_prompt.replace("{b}", csvFile.iloc[x, 2])
            storedTasks.append(processed_prompt)
            storedAnswers.append(csvFile.iloc[x, 3])
        
        return storedTasks, storedAnswers


    def from_yaml(yaml_file):
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

        storedTasks = []
        storedAnswers = []

        for entry in data:
            template = entry["template"]  # Extract template
            values_dict = entry["values"]  # Extract values dictionary
            storedAnswers = entry["result"]

            # Generate all possible value combinations using itertools.product
            keys = values_dict.keys()
            value_combinations = zip(*values_dict.values())

            # Create a PromptTask for each combination
            for values in value_combinations:
                value_mapping = dict(zip(keys, values))  # Pair keys with values
                filled_prompt = template.format(**value_mapping)  # Format the template
                storedTasks.append(filled_prompt)  # Store task

        return storedTasks, storedAnswers