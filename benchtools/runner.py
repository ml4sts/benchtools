# module to create and run benchmarks
import os
from benchtools.task import Task
from benchtools.designer import build_dir, init_repo, create_about, setup_task
# from log_file.py import log_agent_interaction


class Bench():
    '''
        Benchmark with multiple tasks


    Attributes
    ----------
    bench_name : str
        Name of the benchmark.
    bench_path: str
        Path to where the benchmark folder and all its content reside
    task_folder:
        Path to tasks folder insise benchmark folder
    log folder:
        Path to logs folder inside benchmark folder
    tasks: tuple<str,str>
        A tas
    is_built: bool

    Methods
    -------
    build()
        Build the benchmark directory.
    add_task()
        Add new tasks to the benchmark
    run()
        Run one task or all tasks of the benchmark.
    '''
    def __init__(self, name, path):
        '''
        Initialize the benchmark object with the name and path to the benchmark folder.

        Parameters:
        -----------
        name: str
            name of the benchmark will be used for folder
        path: str or buffer
            path to the benchmark folder. If the folder does not exist, it will be created 
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.bench_name = name.strip().replace(" ", "_").lower()
        self.bench_path = path
        self.tasks_folder = os.path.join(self.bench_path, 'tasks')
        self.log_folder = os.path.join(self.bench_path, 'logs')
        self.tasks = []
        self.built = os.path.exists(self.bench_path)
    

    def build(self, about_text, no_git, new_tasks) -> bool:
        '''
        
        Parameters:
        -----------
        about_text: str
            description of the benchmark to be included in the about.md file
        no_git: bool
            whether to initialize a git repository in the benchmark folder
        new_tasks: list of tuples (task_name, task_path)
            list of tasks to be added to the benchmark. Each task is represented as a tuple containing

        Returns:
        --------        
        self.built : bool
            True if the benchmark was successfully built, False otherwise
        '''

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