#  defines a class object for a task
# from openai import OpenAI
import os
import yaml
import json
import boto3
import pandas as pd
import itertools
from ollama import chat, ChatResponse, Client
from .logger import init_log_folder, log_interaction
from pathlib import PurePath
from datasets import load_dataset
from .runner import BenchRunner
import importlib
import sys
from .response import StringAnswer, StringJustification, IntAnswer, IntJustification

from .scorers import scoring_fx_list, contains, exact_match

from .utils import concatenator_id_generator, selector_id_generator

prompt_id_fx = {'concatenator_id_generator':concatenator_id_generator,
                'selector_id_generator':selector_id_generator}

class UnMatchedModel(Exception):
    """
    Exception raised for a bedrock model that isn't accounted for in the match statement
    Follow https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html for a list of available models on bedrock and their inferance parameters
    """
    def __init__(self, model):
        self.model = model
        message = f"Cannot call the model ${attempted_withdrawal} using aws Bedrock. Please fetch the correct inferance parameters for it and add it in a PR to BenchTools."
        super().__init__(message) # Call the base class constructor


class Task:
    """
    defines a basic prompt task with a simple scoring function
    """

    def __init__(self, task_name, template, reference=None, scoring_function=None,
                  variant_values = None, storage_type = 'yaml', description = None, 
                  prompt_id_generator_fx = concatenator_id_generator,
                  format='StringAnswer', source_path=None):
        """
        init a task object from a prompt and reference, and a scoring function. If no 
        scoring function is provided, defaults to exact match.

        Parameters
        ----------
        dir : string or path
            directory containing the task assets
        template: string
            prompt template
        reference: string,  number, or list of strings or numbers the same shape as variant values, 
            solution that will be passed with the model answer to the scoring function,
            or "calculated" to pass the values to a scorer that calculates the answer
        scoring_function : function handle or string
            if string, must be name of built in eval function provided here
        variant_values: dicttionary or list of dictiornaries
             with values to fill in a template, if the task is a template based task. 
             If provided, the prompt will be used as a template and the values in 
             variant_values will be used to fill in the template to create the final prompts 
             for the task. The reference should then be a list of answers corresponding to each prompt variant.
        storage_type : 'yaml' or 'csv'
            how to save the task
        description : string
            textual description of the task, not provided to the model
        prompt_id_generator_fx : callable or string
            how to create ids for each
        format : string
            name of a class 
        source_path : string or path
            path to where custom code will be for scorer or id generator (benchmark path typically)
        """
        self.name = task_name
        self.task_id = task_name.strip().replace(" ", "_").lower() 
        self.description = description 

        self.template = template
        self.variant_values = variant_values

        # set up to name individual prompts
        if not callable(prompt_id_generator_fx):
            self.prompt_id_generator  = prompt_id_fx.get(prompt_id_generator_fx,'custom')

            if self.prompt_id_generator =='custom': 
                
                custom_path = os.path.join(source_path,'custom_labeler.py')
                spec = importlib.util.spec_from_file_location('custom_labeler',custom_path )
                labeler_module = importlib.util.module_from_spec(spec)
                
                spec.loader.exec_module(labeler_module)
                
                self.prompt_id_generator_fx = getattr(labeler_module,prompt_id_generator_fx)
        else:
            self.prompt_id_generator = prompt_id_generator_fx


        if reference == "calculated":
            self.reference = variant_values
        else:
            self.reference = reference
        self.label_references()
        
        # setup for response format
        mod = sys.modules[__name__]
        if hasattr(mod,format):
            self.FormatClass = getattr(mod,format)
        else:
            # load 
            custom_path = os.path.join(source_path,'custom_response.py')
            spec = importlib.util.spec_from_file_location('custom_response',custom_path )
            response_module = importlib.util.module_from_spec(spec)
            
            spec.loader.exec_module(response_module)
            
            self.FormatClass = getattr(response_module,format)


        self.storage_type = storage_type
        
        if scoring_function: 
            if type(scoring_function)==list:
                
                parsed_list = [self.parse_scorer(sc,source_path) 
                               for sc in scoring_function]
                self.scoring_function = lambda res,ref: {p.__name__:(res,ref) 
                                                       for p in parsed_list}
            else:
                self.scoring_function  = self.parse_scorer(scoring_function,source_path)
        else:
            self.scoring_function = exact_match 

            
    @classmethod
    def from_txt_csv(cls, task_path, task_name = None,
                      scoring_function = None,
                     prompt_id_generator_fx = concatenator_id_generator,
                     source_path=None):
        '''
        load a template from txt and create task objects for each row of a csv

        folder must contain a template.txt file with the template, 
        and a values.csv file with the values to fill in the template, 
        and the reference answers. it can optionally have an info.yml with additional 
        settings

        Parameters
        -----------
        task_path: string or path
            where the task files are
        task_name: string
            name
        scoring_function: callable or string
            how to score the task
        prompt_id_generator_fx: callable or string
            over-ruled if 'id' columns in values.csv
        source_path : string or file buffer
            path to custom code
        '''


        if not task_name:
            # get the folder name if not provided
            task_name = PurePath(task_path).parts[-1]
            # decide if using this: .replace("_", " ").title()

        prompt = ""
        with open(os.path.join(task_path, "template.txt"), "r") as f:
            prompt = f.read()

        values_file = os.path.join(task_path, "values.csv")
        # load and strip whitespace from column names and values
        value_answer_df = pd.read_csv(values_file).rename(columns=lambda x: x.strip()).applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        if 'reference' in value_answer_df.columns:
            variant_values = value_answer_df.drop(columns='reference').to_dict(orient='records')
        
            reference = value_answer_df['reference'].tolist()
        else:
            variant_values = value_answer_df.to_dict(orient='records')
            reference = 'calculated'

        if 'id' in value_answer_df.columns:
            prompt_id_generator_fx = selector_id_generator
        
        # TODO: improve this 
        description_file = os.path.join(task_path, "description.txt")
        if os.path.exists(description_file):
            with open(description_file, "r") as f:
                description = f.read()
        else:
            description = f"a template based task with template: {prompt} and values like:\n\n {value_answer_df.head().to_markdown()}"

        info_file = os.path.join(task_path,'task.yml')
        if os.path.exists(info_file):
            with open(info_file, "r") as f:
                info_dict = yaml.safe_load(f) 
        else:
            info_dict= {}

        
        return cls(task_name, template= prompt,
                    variant_values = variant_values, 
                    description = description,
                    reference=reference,
                    storage_type ='csv', 
                   scoring_function = info_dict.get("scorer", scoring_function), 
                   format = info_dict.get('format', 'StringAnswer'),
                   prompt_id_generator_fx =info_dict.get('id_generator', prompt_id_generator_fx),
                    source_path=source_path)
    
    @classmethod
    def from_example(cls, task_name, storage_type):
        '''
        make a blank task 
        '''
        supplemental_files = {'csv':'columns in the csv file',
                              'yaml':'keys below' }
        template = 'Your {noun} for the model here with values that should vary\
              denoted in brackets. {verb} matching  ' + supplemental_files[storage_type]
        variant_values = {'noun':['text','task'],
                          'verb':['use','select']}
        variant_values = [{k:v for k,v in zip(variant_values.keys(),vals)} for vals in zip(*variant_values.values())]
        description = 'give your task a short description '
        return cls(task_name, template= template, variant_values = variant_values, 
                   description = description,  reference='', 
                   storage_type = storage_type, scoring_function = exact_match,
                   source_path=None)


    @classmethod
    def from_yaml(cls, source_path, task_name = None, scoring_function = None):
        '''
        load a task from a yaml file. The yaml file should have the following structure:
        name: string
        template: string
        values: list of dicts (optional)
        reference: "calculated" or string, number, or list of strings or numbers the same 
            shape as variant values (optional)
        scoring_function: string or function handle (optional)
        '''
        yaml_file = os.path.join(source_path, "task_info.yml")
        with open(yaml_file, 'r') as file:
            task_dict = yaml.safe_load(file)  

        value_interpretation = task_dict.get('value_combinations','tuple')
        
        match value_interpretation:
            case 'tuple':
                variant_values = pd.DataFrame(task_dict['values']).to_dict(orient='records')
            case 'combinations':
                
                    # run all combinations
                variant_values = [{k:v for k,v, in zip(task_dict['values'].keys(),vals)} 
                                    for vals in itertools.product(task_dict['values'].values())]

        
        
        return cls(task_dict['name'], 
                   template= task_dict['template'], 
                   variant_values = variant_values, 
                   description = task_dict.get('description', None),
                    reference=task_dict['reference'],
                      storage_type ='yaml', 
                      scoring_function=task_dict.get('scorer', scoring_function),
                    prompt_id_generator_fx =task_dict.get('id_generator', concatenator_id_generator),
                    format = task_dict.get('format', 'StringAnswer'),
                    source_path=source_path)


    @classmethod
    def from_dict(cls, task_dict,prompt_id_generator_fx=concatenator_id_generator,
                  source_path=None):
        '''
        load a task from a dictionary,  The dictionary should have the following structure:
        {
            "template": string,
            "values": list of dicts (optional),
            "reference": string, number, or list of strings or numbers the same shape as variant values (optional),
            "scoring_function": string or function handle (optional)
        }
        '''
        compact_values = task_dict.get("values", None)
        
        if compact_values:
            #  this flips it to a list of dicts 
            match task_dict.get('value_combinations','tuple'):
                case 'tuple':
                    expanded_values = pd.DataFrame(task_dict['values']).to_dict(orient='records')
                case 'combinations':
                    # run all combinations
                    
                    expanded_values = [{k:v for k,v, in zip(task_dict['values'].keys(),vals)} 
                                    for vals in itertools.product(*task_dict['values'].values())]
                    
                    
        else:
            expanded_values = None
        
        if 'id' in compact_values.keys():
            prompt_id_generator_fx = selector_id_generator
        

        return cls(task_dict.get("name", "unnamed_task"),
                   template = task_dict.get("template", ""), 
                   variant_values=expanded_values,
                   storage_type='yaml',
                   reference = task_dict.get("reference", None), 
                   scoring_function = task_dict.get("scorer", None), 
                   description = task_dict.get("description", None),
                   format = task_dict.get('format', 'StringAnswer'),
                   prompt_id_generator_fx =task_dict.get('id_generator', prompt_id_generator_fx),
                   source_path = source_path)
    
    @classmethod
    def from_hf_dataset(cls,task_name, hf_path, prompt_column='prompt', answer_column='canonical_solution'):
        '''
        dataset must have columns 'prompt' and 'canonical_solution' for now, can be expanded in the future.
        '''
        
        dataset = load_dataset(hf_path)
        dataset_test = dataset['test']   

        stored_tasks = dataset_test[prompt_column]
        stored_answers = dataset_test[answer_column]
                
        description = f"a task base don the Hugging Face dataset {hf_path} with prompt column {prompt_column} and answer column {answer_column}"

        return cls(task_name, prommpt =description, variant_values = stored_tasks,
                    reference=stored_answers, storage_type ='csv')
    
    def generate_prompts(self):
        '''
        if the task is a template based task, generate the prompts by filling 
        in the template with the variant values
        '''
        # TODO: consider if this could be a generator function if there are a lot of variants, to avoid memory issues. For now, we will assume that the number of variants is small enough to generate all prompts at once.
        if self.variant_values:
            id_prompt_list = []
            
            for value_set in self.variant_values:
                prompt = self.template
                prompt = prompt.format(**value_set)
                prompt_id = self.prompt_id_generator(self.task_id,value_set)
                id_prompt_list.append((prompt_id,prompt))

            return id_prompt_list
        else:
            return [(self.name, self.template)]
        
    def label_references(self):
        if self.variant_values:
            labeled_refs = {}
            
            for value_set,ref in zip(self.variant_values,self.reference):
                
                prompt_id = self.prompt_id_generator(self.task_id,value_set)
                labeled_refs[prompt_id] = ref

            self.reference = labeled_refs
        else:
            self.reference = {self.name: self.reference}

    @staticmethod
    def parse_scorer(scoring_function,source_path):
        '''
        parse a scorer from input into a callable
        '''

        if isinstance(scoring_function, str):
            parsed_scorer = scoring_fx_list.get(scoring_function,'custom')
        elif callable(scoring_function):
            parsed_scorer = scoring_function

        if parsed_scorer =='custom': 
            
            custom_path = os.path.join(source_path,'custom_scorer.py')
            spec = importlib.util.spec_from_file_location('custom_scorer',custom_path )
            scoring_module = importlib.util.module_from_spec(spec)
            
            spec.loader.exec_module(scoring_module)
            
            parsed_scorer = getattr(scoring_module,scoring_function)
        return parsed_scorer
        
    def get_bench_data(self):
        '''
        get the data for the benchark info file, which includes the name, and storage type.
        '''
        return {
            "name": self.name,
            "id": self.task_id,
            "storage_type": self.storage_type
        }


    def write(self, target_path):
        '''
        write the task
        '''
        # choose the writer and call it 
        match self.storage_type:
            case 'yaml':
                self.write_yaml(target_path)
            case 'csv':
                self.write_csv(os.path.join(target_path,'tasks'))

    def get_dict(self):
        task_dict = {
            "name": self.name,
            "template": self.template,
            "values": self.variant_values,
            "reference": self.reference,
            "scorer": self.scoring_function.__name__ if callable(self.scoring_function) else self.scoring_function,
            "description": self.description,
            "id_generator":self.prompt_id_generator.__name__ ,
            "format":self.FormatClass.__name__
        }
        return task_dict
    
    def write_yaml(self, target_path):
        '''
        write the task to a yaml file
        '''
        data = self.get_dict()
        
        with open(os.path.join(target_path,'task_info.yml'), 'w') as file:
            yaml.dump(data, file)

    def write_csv(self, target_folder):
        '''
        write the task to a csv file with a task.txt template file
        '''
        # Create task folder 
        os.mkdir(os.path.join(target_folder, self.task_id))
        
        # write the template 
        with open(os.path.join(target_folder,self.task_id, 'template.txt'), 'w') as f:
            f.write(self.template)

         
        with open(os.path.join(target_folder,self.task_id, 'description.txt'), 'w') as f:
            f.write(self.description)

        # write the values and answers to a csv
        if self.variant_values:
            value_answer_df = pd.DataFrame(self.variant_values)
            # Add the references to the values
            value_answer_df['reference'] = self.reference
            value_answer_df.to_csv(os.path.join(target_folder,self.task_id, 'values.csv'), index=False)


    
    def run(self, runner=BenchRunner(), log_dir='logs', 
            benchmark=None, bench_path=None,
            score = False):
        """
        run the task on the stated model and log the interactions.

        Parameters
        ----------
        runner: BenchRunner 
            define which runner should be used for the task.
        
            runner.model : string
                the model to run the task on
            runner.api_url : string
                the url of the api to use for the task
            runner.runner_type: {ollama,openai}
                to use the Ollama runner, the script expects the model to be installed, and `ollama serve` running on localhost:11434
                to use OpenAI runner, you must have an API key set in your OPENAI_API_KEY environment variable
        log_dir: str
            Path to where the logs should be saved. If empty a log folder will be created in the current working directory

        Returns
        -------
        response : list
            model response(s)
        """

        responses = []
        # Gerenate all the prompts of the task
        id_prompt_list = self.generate_prompts()

        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        run_log=""
        # Create logging structure for a task within a log directory
        try:
            run_log = init_log_folder(log_dir, runner.model, self.get_dict(), 
                                        id_prompt_list, benchmark, bench_path)
        except Exception as e:
            print(f"Couldn't create log directory in {log_dir}...\n{e}")


        for (prompt_id, prompt),values in zip(id_prompt_list,self.variant_values):
            
            error = None
            response = ''
            try:
                match runner.runner_type:
                    case "ollama":
                        completion: ChatResponse = chat(
                            model=runner.model, 
                            format = self.FormatClass.model_json_schema(),
                            messages=[
                            {
                            'role': 'user',
                            'content':prompt,
                            },
                        ])
                        # print("response: " + response.message.content)
                        response = completion.message.content
                        

                    case "ollama_api":
                        client = Client(
                            host=runner.api_url if runner.api_url else "http://localhost:11434",
                        )
                        completion = client.chat(
                            runner.model,
                            format = self.FormatClass.model_json_schema(),
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
                            base_url=runner.api_url if runner.api_url else "https://api.openai.com/v1",
                        )
                        chat_completion = client.chat.completions.create(
                            model=runner.model,
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt,
                                }
                            ],
                        )
                        response = chat_completion.choices[0].message.content
                        
                    case "bedrock":
                        bedrock_client = boto3.client('bedrock-runtime')
                        # Bedrock has multiple foundational models that will each differ in request parameters and response fields we included cases for a couple of them
                        # for available foundational models and their inferance parameters follow 
                        # https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html
                        # Catch the model family first
                        model_fam = None
                        if runner.model.startswith("meta"): model_fam = "llama"
                        elif runner.model.startswith("google"): model_fam = "gemma"
                        match model_fam:
                            case "llama":
                                # Embed the prompt in Llama 3's instruction format.
                                formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""
                                # Format the request payload using the model's native structure.
                                request = {
                                    "prompt": formatted_prompt,
                                    # "max_gen_len": 512,
                                    # "temperature": 0.5,
                                }
                                # Convert the native request to JSON.
                                request = json.dumps(request)
                                completeion = bedrock_client.invoke_model(
                                    modelId = runner.model,
                                    body = request
                                )
                                # Decode the response body.
                                response = json.loads(completeion["body"].read())
                                response = response["generation"]
                            case "gemma":
                                completeion = bedrock_client.invoke_model(
                                    modelId = runner.model,
                                    body = json.dumps(
                                        {
                                            'messages': [
                                                {
                                                'role': 'user',
                                                'content': prompt
                                                }
                                            ]
                                        }
                                    )
                                )
                                # Decode the response body.
                                response = json.loads(completeion['body'].read())
                                response = response['choices'][0]['message']['content']
                            case _:
                                raise UnMatchedModel(runner.model)
                        
                    case _:
                        print(f"Runner type {runner.runner_type} not supported")
                        return None
            except Exception as e:
                error = e
            if score:
                score_val = self.scoring_function(response, self.reference[prompt_id])
                
            else: 
                score_val = None

            log_interaction(run_log, prompt_id, prompt, response, str(error),values,score_val)
            responses.append(response)

        
        self.responses = responses 
        


        return self.responses

    
    def score(self, response,prompt_id=None):
        """
        score the response using the defined function

        Parameters
        ----------
        response : string
            the value to score
        """
                
        if prompt_id:
            return self.scoring_function(response,self.reference[prompt_id])
        else:
            return self.scoring_function(response, self.reference)


# additional classes for other types of tasks

# likely an agent task that can pass environment assets

