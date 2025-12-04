# module to run benchmarks
import os
from pathlib import Path
from itertools import product
from benchtools.task import Task
# from log_file.py import log_agent_interaction


class Bench():
    '''
    '''
    def __init__(self, bench_dir):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.directory = bench_dir
        self.tasks = []
    
        tasks_folder = os.path.join(bench_dir, "benchmarks")
        tasks = os.listdir(tasks_folder)
        for task in tasks:
            content = os.listdir(os.path.join(tasks_folder,task))
            for file in content:
                if file.endswith("csv"):
                    self.tasks.append(Task('csv', task, os.path.join(tasks_folder,task)))
                elif file.endswith("yml"):
                    self.tasks.append(Task('yml', task, os.path.join(tasks_folder,task,file)))
                    
        for task in self.tasks:
            name, prompts, answers = task.name, task.sub_tasks, task.answers
            print("Task: " + name)
            print("Prompts: ", end='')
            print(prompts)
            print("Answers: ", end='')
            print(answers)
            print("Responses: ", end='')
            task.run("gemma3")
            print(task.responses)


        


    def run(self, model, api_url=None):
        '''
        '''
        for task in self.tasks:
            task.run(model, api_url)
            # log_agent_interaction(prompt, response)
            # task.score()
            print(task.responses)