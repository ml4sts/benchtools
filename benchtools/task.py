#  defines a class object for a task
from ollama import Client
from openai import OpenAI

from scorerers import exact_match

scoring_fx = {"exact_match": exact_match}


class PromptTask:
    """
    defines a basic prompt task with a simple scoring function
    """

    def __init__(
        self, prompt=None, scoring_function=None, reference=None, runner_type="ollama"
    ):
        """
        init a task object

        Parameters
        ----------
        dir : string or path
            directory containing the task assets
        prompt : string
            prompt that will pass to the model
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
        self.prompt = prompt
        if type(scoring_function) is str:
            self.scoring_function = scoring_fx[scoring_function]
        else:
            self.scoring_function = scoring_function

        self.reference = reference
        self.runner_type = runner_type

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
        match self.runner_type:
            case "ollama":
                client = Client(
                    host=api_url if api_url else "http://localhost:11434",
                )
                response = client.chat(
                    model,
                    messages=[
                        {
                            "role": "user",
                            "content": self.prompt,
                        },
                    ],
                )
                return (self.prompt, response["message"]["content"])
            case "openai":
                client = OpenAI(
                    base_url=api_url if api_url else "https://api.openai.com/v1",
                )
                chat_completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": self.prompt,
                        }
                    ],
                )
                return (self.prompt, chat_completion.choices[0].message.content)
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
