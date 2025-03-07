# module to run benchmarks
import pandas
import yaml
import os
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
    def from_txt_csv():
        '''
        load a template from txt and create task objects for each row of a csv
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor

        return self

    
    def from_yaml():
        '''
        laod from a yaml
        '''