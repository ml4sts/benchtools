import os
import yaml
import json
# import logging 
import datetime
import dataclasses
# from dataclasses import dataclass

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        #if it is a function, use its string name
        elif hasattr(o, '__call__'):
            return o.__name__
        return super().default(o)


class Logger:
    ''' 
    A class that holds all information and methods related to logging the interactions between the runner and the model. The logger will create the logging structure for each run of a task, and will log the prompt, response, and any other relevant information such as tokens used, stop reason, errors, etc...
    '''

    def __init__(self, log_path):
        '''
        Initializes the logger by creating the log directory if it doesn't exist.

        Parameters:
        -------------
        log_path: str
            The path to the log dir where the log file will be created.
        '''
        self.log_path = log_path
        # self.init_log_directory() # Create the log folder structure for the task
        os.makedirs(self.log_path, exist_ok=True)

        self.bench_info = {}


    def log_bench_info(self, bench_info):
        # Get timestamp without fractions of seconds
        timestamp = int(datetime.datetime.now().timestamp())

        bench_info[f'bench_run_id'] = str(timestamp)
        self.bench_info = bench_info
        if self.log_path != f"{bench_info['bench_path']}/logs":
            self.log_path = os.path.join(self.log_path, f"bench_{bench_info['bench_name']}")
            os.makedirs(self.log_path, exist_ok=True)


    def log_task_info(self, task_info, id_prompt_list: list):
        '''
        Logs the task info to the log folder specified by the user

        Parameters:
        -------------
        task_info: dict
            A dictionary with all the task's info for which the logger is being initialized.
        '''
        # Get timestamp without fractions of seconds
        timestamp = int(datetime.datetime.now().timestamp())

        task_info['task_timestamp'] = str(timestamp)
        if self.bench_info:
            task_info['task_run_id'] = f"{self.bench_info['bench_run_id']}_{task_info['task_timestamp']}"
        else:
            task_info['task_run_id'] = task_info['task_timestamp']
            
        self.task_info = task_info

        self.task_log_path = os.path.join(self.log_path, f"task_{task_info['name']}")
        os.makedirs(self.task_log_path, exist_ok=True)
        
        # with open(os.path.join(run_log_dir, "task_info.yml"), 'w') as f:
            # yaml.dump(task_info, f)

        # Add prompt_id of each value set to values
        for idx, (prompt_id, _) in enumerate(id_prompt_list):
            task_info['values'][idx].update({'prompt_id': prompt_id})


    def log_runner_info(self, runner_info):
        ''''
        Creates the log directories and sub-directories for a specific task.

        Parameters:
        -------------
        runner_info: dict
            Dictionary that contains information about the runner of a task
        '''

        self.model_dir = os.path.join(self.task_log_path, runner_info['model'])
        os.makedirs(self.model_dir, exist_ok=True)

        self.run_dir = os.path.join(self.model_dir, self.task_info['task_run_id'])
        os.makedirs(self.run_dir, exist_ok=True)
 
        self.runner_info = runner_info

        # Create run_info.yml with all the metadata
        self.run_info =  self.bench_info | self.task_info | self.runner_info
        self.run_info['log_path'] = str(self.task_log_path)

        with open(os.path.join(self.run_dir,'run_info.yml'), 'w') as f:
            yaml.dump(self.run_info, f)


    def log_interaction(self, response_info):
        """
        Logs the event to the log folder specified by the user

        Parameters:
        -------------
        response_info: dict
            A dictionary of logged information from the interaction with the LLM
        """

        # Making this into a directory in case more files (possibly steps) were to be held in here
        self.prompt_dir = os.path.join(self.run_dir, response_info['prompt_id'])
        os.mkdir(self.prompt_dir)

        with open(os.path.join(self.prompt_dir, "log.txt"), 'w') as f:
            f.write("------ prompt ------\n")
            f.write(f"{response_info['prompt']}\n\n")
            f.write("------ response ------\n")
            f.write(f"{response_info['response']}\n\n")


        step_trace = {
            'task_name': self.run_info['name'],
            'template': self.run_info['template'],
            'steps':{ 
                0: response_info,
            },
        }
        

        with open(os.path.join(self.prompt_dir, "log.json"), 'w') as f:
            json.dump(step_trace, f, indent=4, cls=EnhancedJSONEncoder)

        # TODO: What can we benifit from the logger?
        # logger.info(f'Input: {prompt}')
        # logger.info(f'Output: {response}')
        
        
        
    # def log_score(score):
    #     with open(os.path.join(run_log_dir, "run_info.yml"), 'r') as f:
    #             run_info = yaml.safe_load(f) 
        
    #     step_trace['steps'][0]['score'] = score