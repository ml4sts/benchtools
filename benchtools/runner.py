# module to create and run benchmarks
import os
import json
import yaml
import boto3
import pandas as pd
from pathlib import Path
from .logger import Logger
from ollama import chat, ChatResponse, Client


# possibly resurected for batch runs? 
class BenchRunner():
    '''
    A BenchRunner holds information about how a task is going to be run. 
    '''

    def __init__(self, runner_type='ollama', model='gemma3:1b', api=None, model_params=None):
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
        model_params: dict
            A dictionary with inference parameters to be used for the model generation such as temperature, max_tokens, top_p, stop_sequence, etc.
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

        self.inference_parameters= model_params
    
    @staticmethod
    def from_file(cls, file_path):
        runners = []
        model_params = {}
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        
        with open(os.path.join(file_path), 'r') as f:
            run_info = yaml.safe_load(f)
        type= run_info.pop('runner_type', 'ollama')
        model= run_info.pop('model', 'gemma3:1b')
        api= run_info.pop('api', None)

        # Any remaining keys are considered model parameters
        model_params = run_info if run_info else None

        return cls(type, model, api, model_params)

    def __str__(self):
        return f'{self.model} via {self.runner_type}'

    def run(self, prompt_id, prompt, values,  format, logger):
        '''
        Run method of a runner takes a prompt and a format and then finds the correct api call that matches the runner requested by the user. Runs the LLM call and returns the LLM response
        '''
        runner_info = {
            'runner_type': self.runner_type,
            'model': self.model,
            'api': self.api,
            'inference_parameters': self.inference_parameters
        }
        logger.log_runner_info(runner_info)

        response_info = {
            'prompt_id': prompt_id,
            'prompt': prompt,
            'values': values,
            'format': format,
            'response': '',
            'error': None,
            'prompt_tokens': 0,
            'response_tokens': 0,
            'total_tokens': 0,
            'stop_reason': None,
        }

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
                        ],
                        options=self.inference_parameters
                    )
                    response_info['response'] = completion.message.content
                    response_info['prompt_tokens'] = completion.prompt_eval_count
                    response_info['response_tokens'] = completion.eval_count
                    response_info['total_tokens'] = completion.eval_count + completion.prompt_eval_count
                    response_info['stop_reason'] = completion.done_reason


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
                        options=self.inference_parameters
                    )
                    response_info['response'] = completion["message"]["content"]
                    response_info['prompt_tokens'] = completion["prompt_eval_count"]
                    response_info['response_tokens'] = completion["eval_count"]
                    response_info['total_tokens'] = completion["eval_count"] + completion["prompt_eval_count"]
                    response_info['stop_reason'] = completion["done_reason"]


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
                    config={}
                    # bedrock has some shared inference parameters but also some model specific ones.
                    # We pop the shared ones and then send the rest as additionalModelRequestFields for the model to handle as needed.
                    if self.inference_parameters:
                        if "temperature" in self.inference_parameters: config.update({"temperature": self.inference_parameters.pop("temperature", None)})
                        if "topP" in self.inference_parameters: config.update({"topP": self.inference_parameters.pop("topP", None)})
                        if "maxTokens" in self.inference_parameters: config.update({"maxTokens": self.inference_parameters.pop("maxTokens", None)})
                        if "stopSequences" in self.inference_parameters: config.update({"stopSequences": self.inference_parameters.pop("stopSequences", None)})

                    client = boto3.client('bedrock-runtime', region_name='us-east-1')
                    try:
                        response = client.converse(
                            modelId=self.model,
                            messages=[
                                {
                                    'role': 'user',
                                    'content': [{'text': prompt}]
                                }
                            ],
                            inferenceConfig=config,
                            additionalModelRequestFields = self.inference_parameters, # For model-specific inference params
                            # additionalModelResponseFieldPaths[], # For model-specific return fields
                            outputConfig={
                                "textFormat": {
                                    "type": "json_schema",
                                    "structure": {
                                        "jsonSchema": {
                                            "schema": json.dumps(format),
                                            "name": format['title'],
                                            "description": format['description'] if 'description' in format else format['title']
                                        }
                                    }
                                }
                            }
                        )
                        # Catch the model family
                        # model_fam = None
                        # if self.model.startswith("meta") or self.model.startswith("us.meta"): model_fam = "meta"
                        # elif self.model.startswith("google"): model_fam = "gemma"
                        # elif self.model.startswith("nova") or self.model.startswith("us.nova"): model_fam = "nova"
                        # match model_fam:
                        #     case "meta" |"nova":
                        #         response_info['response'] = response['output']['message']['content'][0]['text']
                        #     case "gemma" | "_":
                        #         response_info['response'] = response['output']['message']['content']['text']
                        response_info['response'] = response['output']['message']['content'][0]['text']
                        response_info['prompt_tokens'] = response['usage']['inputTokens']
                        response_info['response_tokens'] = response['usage']['outputTokens']
                        response_info['total_tokens'] = response['usage']['totalTokens']
                        response_info['stop_reason'] = response['stopReason']

                    except Exception as e:
                        response_info['error'] = e
                        print(f"bedrock converse API failed with model {self.model}.\n{e}")

                case _:
                    print(f"Runner type {self.runner_type} not supported")
                    return None
        except Exception as e:
            response_info['error'] = e

        logger.log_interaction(response_info)
        return response_info['response'], response_info['error']


    

class BenchRunnerList():
    '''
    a set of runner objects that can be used to run a benchmark on multiple models and/or runner types.
    '''
    def __init__(self, runners: list[BenchRunner]=[BenchRunner()]):
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
