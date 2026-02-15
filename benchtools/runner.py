# module to create and run benchmarks
import os
from benchtools.task import Task
# from benchtools.designer import build_dir, init_repo, create_about, setup_task
# from log_file.py import log_agent_interaction


class BenchRunner():
    '''
    TODO: this might not be how this ends up, but thi si scurrent thign
    '''

    def run(self, tasks_torun=[], model='gemma3', api_url=None):
        '''
        Run the benchmark by running each task in the benchmark and logging the interactions.
        Parameters:
        -----------
        tasks_torun: list of str
            A list of task names to run. If empty, all tasks will be run.
        model: str default 'gemma3'
            The name of the model to use for running the tasks. Default is 'gemma3'.
        api_url: str
            The URL of the API to use for running the tasks. If None, the default API
        '''
        tasks = os.listdir(self.tasks_folder)
        for task in tasks:
            task_folder = os.path.join(self.tasks_folder,task)
            content = os.listdir(task_folder)
            for file in content:
                if file.endswith("csv"):
                    self.tasks.append(Task('csv', task, task_folder, self.log_folder))
                elif file.endswith("yml"):
                    self.tasks.append(Task('yml', task, os.path.join(task_folder,file), self.log_folder))

        tasks_torun = [task.name for task in self.tasks] if tasks_torun == [] else tasks_torun
        # print(tasks_torun)
        # print(self.tasks)
        for task in self.tasks:
            if task.name in tasks_torun:
                print("\n")
                name, prompts, answers = task.name, task.sub_tasks, task.answers
                print("Task: " + name)
                print("Prompts: ", end='')
                print(prompts)
                print("Answers: ", end='')
                print(answers)
                task.run(model, api_url)
                print("Responses: ", end='')
                print(task.responses)

            # log_agent_interaction(prompt, response)
            # task.score()