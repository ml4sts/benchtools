# module to run benchmarks
import os
import yaml # requires pyyaml
import pandas
from pathlib import Path
from itertools import product
# from benchtools.task import PromptTask
# from log_file.py import log_agent_interaction


class Bench():
    '''
    '''
    def __init__(self, bench_dir, target_dir):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.tasks = []
    
        tasks_folder = os.path.join(bench_dir, "benchmarks")
        tasks = os.listdir(tasks_folder)
        # Both functions should have the same type return. porobably should be a list of PRompt_Task
        # TODO: use Prompt_Task
        for task in tasks:
            content = os.listdir(os.path.join(tasks_folder,task))
            for file in content:
                if file.endswith("csv"):
                    self.tasks.append((task, from_txt_csv(os.path.join(tasks_folder,task))))
                elif file.endswith("yml"):
                    self.tasks.append((task, from_yaml(os.path.join(tasks_folder,task,file))))
                    
        for name, (prompts, answers) in self.tasks:
            print("Task: " + name)
            print("Prompts: ", end='')
            print(prompts)
            print("Answers: ", end='')
            print(answers)



        

    def run(self, model):
        '''
        '''
        for task in self.tasks:
            (prompt, response) = task.run(model)
            log_agent_interaction(prompt, response)
            task.score()




# possibly private method?  # TODO: Fix csv indexing?
def from_txt_csv(task_folder):
    '''
    load a template from txt and create task objects for each row of a csv
    '''
    # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor
    prompt = ""
    with open(os.path.join(task_folder, "task.txt"), "r") as f:
        prompt = f.read()

    csvFile = pandas.read_csv(os.path.join(task_folder, "values.csv"))
    # answers = pandas.read_csv(os.path.join(task_folder, "results"))
    storedTasks = []
    storedAnswers = []
    for x in range(len(csvFile)):
        processed_prompt = prompt.replace("{a}", str(csvFile.iloc[x,0]))
        processed_prompt = processed_prompt.replace("{b}", str(csvFile.iloc[x, 1]))
        storedTasks.append(processed_prompt)
        print("Prompt: "+ processed_prompt)
        storedAnswers.append(str(csvFile.iloc[x, 2]))
    
    return (storedTasks, storedAnswers)


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
    return (storedTasks, storedAnswers)