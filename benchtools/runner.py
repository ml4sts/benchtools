# module to create and run benchmarks


# possibly resurected for batch runs? 
class BenchRunner():
    '''
    A BenchRunner holds information about how a task is going to be run. 
    '''

    def __init__(self, runner_type='ollama', model='gemma3:1b', api_url=None):
        '''
        The constructor for BenchRunner will have default values for all attributes to have a full default runner ready to be used for running any task.
        P.S. Requires Ollama to be installed and running on your machine.
        -----------
        runner_type: str default 'ollama'
            The used engine for running an LLM. Default is ollama that will need to be installed and running on your machine
        model: str default 'gemma3'
            The name of the LLM to use for running the tasks. Default is 'gemma3'. P.S. Will need to have the model downloaded locally if using ollama
        api_url: str
            The URL of the API to use for accessing an LLM. If None, the default API will be http://localhost:11434 as this is used by ollama by default
        '''

        self.runner_type = runner_type
        self.model = model
        self.api = api_url


        # tasks = os.listdir(self.tasks_folder)
        # for task in tasks:
        #     task_folder = os.path.join(self.tasks_folder,task)
        #     content = os.listdir(task_folder)
        #     for file in content:
        #         if file.endswith("csv"):
        #             self.tasks.append(Task('csv', task, task_folder, self.log_folder))
        #         elif file.endswith("yml"):
        #             self.tasks.append(Task('yml', task, os.path.join(task_folder,file), self.log_folder))

        # tasks_torun = [task.name for task in self.tasks] if tasks_torun == [] else tasks_torun
        # print(tasks_torun)
        # print(self.tasks)


        # for task in self.tasks:
        #     if task.name in tasks_torun:
        #         print("\n")
        #         name, prompts, answers = task.name, task.sub_tasks, task.answers
        #         print("Task: " + name)
        #         print("Prompts: ", end='')
        #         print(prompts)
        #         print("Answers: ", end='')
        #         print(answers)
        #         task.run(model, api_url)
        #         print("Responses: ", end='')
        #         print(task.responses)

            # log_agent_interaction(prompt, response)
            # task.score()

