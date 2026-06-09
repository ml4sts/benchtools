# module to create and run benchmarks
import os
import json
import yaml
import boto3
import pandas as pd
from pathlib import Path
from ollama import chat, ChatResponse, Client


# possibly resurected for batch runs? 
class BenchRunner():
    '''
    A BenchRunner holds information about how a task is going to be run. 
    '''

    def __init__(self, runner_type='ollama', model='gemma3:1b', api=None):
        '''
        The constructor for BenchRunner will have default values for all attributes to have a full default runner ready to be used for running any task.
        P.S. Requires Ollama to be installed and running on your machine.
        -----------
        runner_type: str default 'ollama'
            The used engine for running an LLM. Default is ollama that will need to be installed and running on your machine
        model: str default 'gemma3'
            The name of the LLM to use for running the tasks. Default is 'gemma3'. P.S. Will need to have the model downloaded locally if using ollama
        api: str
            The URL of the API to use for accessing an LLM. If None, the default API will be http://localhost:11434 as this is used by ollama by default
        '''

        self.runner_type = runner_type
        self.model = model
        api_default = {'ollama_api': "http://localhost:11434",
                           'openai':"https://api.openai.com/v1",
                           'ollama':"",
                           'bedrock': ""}
        if api:
            self.api = api 
        else:
            self.api = api_default[runner_type]

    def __str__(self):
        return f'{self.model} via {self.runner_type}'

    def run(self, prompt, format):
        '''
        Run method of a runner takes a prompt and a format and then finds the correct api call that matches the runner requested by the user. Runs the LLM call and returns the LLM response
        '''
        error = None
        response = ''
        try:
            match self.runner_type:
                case "ollama":
                    completion: ChatResponse = chat(
                        model=self.model,
                        format = format,
                        messages=[
                        {
                        'role': 'user',
                        'content':prompt,
                        },
                    ])
                    response = completion.message.content


                case "ollama_api":
                    client = Client(
                        host=self.api ,
                    )
                    completion = client.chat(
                        self.model,
                        format = format,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                    )
                    response = completion["message"]["content"]


                case "openai":
                    client = OpenAI(
                        base_url=self.api,
                    )
                    chat_completion = client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ],
                    )
                    response = chat_completion.choices[0].message.content

                case "bedrock":
                    client = boto3.client('bedrock-runtime', region_name='us-east-1')
                    try:
                        response = client.converse(
                            modelId=self.model,
                            messages=[
                                {
                                    'role': 'user',
                                    'content': [{'text': prompt}]
                                }
                            ]
                        )
                        # Catch the model family
                        model_fam = None
                        if self.model.startswith("meta") or self.model.startswith("us.meta"): model_fam = "meta"
                        elif self.model.startswith("google"): model_fam = "gemma"
                        elif self.model.startswith("nova") or self.model.startswith("us.nova"): model_fam = "nova"
                        match model_fam:
                            case "meta" |"nova":
                                response = response['output']['message']['content'][0]['text']
                            case "gemma" | "_":
                                response = response['output']['message']['content']['text']

                    except Exception as e:
                        error = e
                        print(f"bedrock converse API failed with model {self.model}.\n{e}")

                case _:
                    print(f"Runner type {self.runner_type} not supported")
                    return None
        except Exception as e:
            error = e
        return response, error


    

class BenchRunnerList():
    '''
    a set of runners
    '''
    def __init__(self, runners: list[BenchRunner]):
        '''

        Parameters
        -----------
        runners: list[BenchRunner]
            runners to execute
        '''
        self.runners = runners 

    @classmethod
    def from_file(cls,file_path):
        '''
        load from yaml file file can have a list with values for 
        all 3 fields or a single set of values. the `model` key can take a list
        missing values get the defaults. 

        Paramters
        ---------
        file_path : path or string
            path to file or dir with runner.yml

        '''
        
        if os.path.isdir(file_path):
            file_path = os.path.join(file_path,'runner.yml')

        with open(file_path,'r') as f:
            runner_info = yaml.safe_load(f)

        
        # check if any have a list in model key and expand
        if isinstance(runner_info,list):
            df = pd.DataFrame(runner_info)
            runner_expanded = df.explode('model').reset_index(drop=True).to_dict('records')
            runner_list = [BenchRunner(**r) for r in runner_expanded]
        else:
            if isinstance(runner_info['model'],list):
                
                runner_list = [BenchRunner(runner_type=runner_info.get('runner_type',None),
                                           api= runner_info.get('api',None), model=m,) 
                            for m in runner_info['model']]
            else: 
                runner_list = [BenchRunner(**runner_info)]
        
        return cls(runner_list)
