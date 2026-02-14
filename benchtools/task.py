#  defines a class object for a task
# from openai import OpenAI
import os
import yaml # requires pyyaml
import pandas
from ollama import chat, ChatResponse, Client
from benchtools.logger import init_logger, log_agent_interaction

# from scorerers import exact_match
# scoring_fx = {"exact_match": exact_match}


class Task:
    """
    defines a basic prompt task with a simple scoring function
    """

    def __init__(
        self, task_name, prompt, reference, scoring_function=None, prompt_variants = None, 
    ):
        """
        init a task object from a prompt and reference, and a scoring function. If no scoring function is provided, defaults to exact match.

        Parameters
        ----------
        dir : string or path
            directory containing the task assets
        prompt: string
            prompt for task or overall description 
        scoring_function : function handle or string
            if string, must be name of built in eval function provided here
        reference: string or number or list of 
            solution that will be passed with the model answer to the scoring function
        """
        self.name = task_name

        if prompt_variants:
            self.sub_tasks = prompt_variants
            self.description = prompt 
        else:
            self.sub_tasks = [prompt]
            self.description = f"a basic prompt task with: {prompt}"

        
        self.reference = reference

        if type(scoring_function) is str:
            self.scoring_function = scoring_function[scoring_function]
        else:
            self.scoring_function = scoring_function

        
        # self.responses = []

        # self.logger = init_logger(self.log_path, self.name)

    

    @classmethod
    def from_txt_csv(cls, task_name, task_folder):
        '''
        load a template from txt and create task objects for each row of a csv

        folder must contain a task.txt file with the template, and a values.csv file with the values to fill in the template, and the reference answers. The csv should be structured as follows:
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor
        prompt = ""
        with open(os.path.join(task_folder, "task.txt"), "r") as f:
            prompt = f.read()

        value_answer_df = pandas.read_csv(os.path.join(task_folder, "values.csv"))
        # answers = pandas.read_csv(os.path.join(task_folder, "results"))
        storedTasks = []
        storedAnswers = []
        for x in range(len(value_answer_df)):
            processed_prompt = prompt.replace("{a}", str(value_answer_df.iloc[x,0]))
            processed_prompt = processed_prompt.replace("{b}", str(value_answer_df.iloc[x, 1]))
            storedTasks.append(processed_prompt)
            # print("Prompt: "+ processed_prompt) # Debugging
            storedAnswers.append(str(value_answer_df.iloc[x, 2]))
        
        description = f"a template based task with template: {prompt} and values like:\n\n {value_answer_df.head().to_markdown()}"

        return cls(task_name, prompt_variants = storedTasks, reference=storedAnswers)

        

    @classmethod
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
        for sub_task in data:
            template = sub_task["template"]  # Extract template
            values_dict = sub_task["values"]  # Extract values dictionary
            answers = sub_task["result"]
            # Generate all possible value combinations using itertools.product
            keys = values_dict.keys()
            value_combinations = zip(*values_dict.values())
            # Create a PromptTask for each combination
            for values in value_combinations:
                value_mapping = dict(zip(keys, values))  # Pair keys with values
                filled_prompt = template.format(**value_mapping)  # Format the template
                # print("Prompt: "+ filled_prompt) # Debugging
                storedTasks.append(filled_prompt)  # Store task
            for answer in answers:
                storedAnswers.append(answer)
        return (storedTasks, storedAnswers)

    def run(self, model,runner_type="ollama", api_url=None):
        """
        run the task on the model

        Parameters
        ----------
        model : string
            the model to run the task on
        api_url : string
            the url of the api to use for the task
        runner_type: string {ollama,openai}
            define which runner should be used for the task.
            to use the Ollama runner, the script expects the model to be installed, and `ollama serve` running on localhost:11434
            to use OpenAI runner, you must have an API key set in your OPENAI_API_KEY environment variable
        """

        for sub_task in self.sub_tasks:
            # print(sub_task)

            match runner_type:
                case "ollama":
                    response: ChatResponse = chat(model=model, messages=[
                        {
                          'role': 'user',
                          'content':sub_task,
                        },
                    ])
                    # print("response: " + response.message.content)
                    self.responses.append(response.message.content)

                case "ollama_api":
                    client = Client(
                        host=api_url if api_url else "http://localhost:11434",
                    )
                    response = client.chat(
                        model,
                        messages=[
                            {
                                "role": "user",
                                "content": sub_task,
                            },
                        ],
                    )
                    self.responses.append(response["message"]["content"])

                case "openai":
                    client = OpenAI(
                        base_url=api_url if api_url else "https://api.openai.com/v1",
                    )
                    chat_completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "user",
                                "content": sub_task,
                            }
                        ],
                    )
                    self.responses.append(chat_completion.choices[0].message.content)
                case _:
                    print(f"Runner type {self.runner_type} not supported")
                    return None
            
            log_agent_interaction(self.logger, sub_task, response.message.content)


    def score(self, response):
        """
        score the response using the defined function

        Parameters
        ----------
        response : string
            the value to score
        """
        return self.scoring_function(response, self.reference)


# additional classes for other types of tasks

# likely an agent task that can pass environment assets
