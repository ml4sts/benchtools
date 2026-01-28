# module to run benchmarks
import os
from benchtools.task import Task
from benchtools.designer import build_dir, init_repo, create_about, setup_task
# from log_file.py import log_agent_interaction


class Bench():
    '''
    '''
    def __init__(self, name, path):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.bench_name = name
        self.bench_path = path
        self.tasks_folder = os.path.join(self.bench_path, 'benchmarks')
        self.log_folder = os.path.join(self.bench_path, 'logs')
        self.tasks = []
        self.built = os.path.exists(self.bench_path)
    

    def build(self, about_text, no_git, new_tasks) -> bool:

        # Create benchmark skeleton 
        build_dir(self.bench_path)

        # Create about.md
        create_about(self.bench_name, self.bench_path, about_text)

        # Initialize a git repo
        if not no_git:
            init_repo(self.bench_path)

        for task_name, task_path in new_tasks:
            self.add_task(task_name, task_path)

        self.built = True
        return self.built


    def add_task(self, task_name, task_path):
        if self.built:
            self.tasks.append(setup_task(self.tasks_folder, task_name, task_path))


    def run(self, tasks_torun=[], model='gemma3', api_url=None):
        '''
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

        tasks_torun = self.tasks if tasks_torun == [] else tasks_torun    
        print(tasks_torun)
        print(self.tasks)
        for task in self.tasks:
            if task.name in tasks_torun:
                print("\n\n\n")
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