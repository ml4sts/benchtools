#  defines a class object for a task
# from openai import OpenAI
import os
import yaml # requires pyyaml
import pandas
from ollama import chat, ChatResponse, Client

# from scorerers import exact_match
# scoring_fx = {"exact_match": exact_match}


class Task:
    """
    defines a basic prompt task with a simple scoring function
    """

    def __init__(
        self, data_type, name, path, scoring_function=None, reference=None, runner_type="ollama"
    ):
        """
        init a task object

        Parameters
        ----------
        dir : string or path
            directory containing the task assets

        scoring_function : function handle or string
            if string, must be name of built in eval function provided here
        reference: string or number
            solution that will be passed with the model answer to the scoring function
        runner_type: string {ollama}
            the way the runner should be called,
            solution that will be passed with the model answer
        runner_type: string {ollama,openai}
            define which runner should be used for the task.
            to use the Ollama runner, the script expects the model to be installed, and `ollama serve` running on localhost:11434
            to use OpenAI runner, you must have an API key set in your OPENAI_API_KEY environment variable
        """
        self.name = name
        self.sub_tasks = []
        self.answers = []
        match data_type:
            case 'csv':
                prompt, answer = from_txt_csv(path)
                self.sub_tasks=(prompt)
                self.answers=(answer)
            case 'yml':
                prompt, answer = from_yaml(path)
                self.sub_tasks=(prompt)
                self.answers=(answer)


        if type(scoring_function) is str:
            self.scoring_function = scoring_fx[scoring_function]
        else:
            self.scoring_function = scoring_function

        self.reference = reference
        self.runner_type = runner_type
        self.responses = []



    def run(self, model, api_url=None):
        """
        run the task on the model

        Parameters
        ----------
        model : string
            the model to run the task on
        api_url : string
            the url of the api to use for the task
        """

        for sub_task in self.sub_tasks:
            print(sub_task)

            match self.runner_type:
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
            print("Prompt: "+ filled_prompt)
            storedTasks.append(filled_prompt)  # Store task
        for answer in answers:
            storedAnswers.append(answer)
    return (storedTasks, storedAnswers)