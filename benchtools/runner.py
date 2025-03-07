# module to run benchmarks
import pandas
import yaml
import os
from log_file.py import log_agent_interaction
import task
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
        x = 0
        storedTasks = []
        storedAnswers = []
        while x < len(csvFile):
            processed_prompt = textFile.replace("{a}", csvFile.iloc[x,1])
            processed_prompt.replace("{b}", csvFile.iloc[x, 2])
            storedAnswers.append(answers[x,1])
            storedTasks.append(processed_prompt)
        
        return storedTasks, storedAnswers

    
    def from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        self.tasks = []
        for each in data:
            template = each.get('template', '')
            values = each.get('values', [])
            processed_values = []
            for val in values:
                for key, value in val.items():
                    if isinstance(value, str): 
                        processed_values.append((key, list(map(int, value.split(',')))))
                    else:
                        processed_values.append((key, value))
            keys = [key for key, _ in processed_values]
            value_lists = [value for _, value in processed_values]
            value_combinations = list(zip(*value_lists))
            for combination in value_combinations:
                value_dict = dict(zip(keys, combination))
                temp = template.format(**value_dict)
                self.tasks.append(temp)
        return self.tasks
