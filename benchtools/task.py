#  defines a class object for a task
# from openai import OpenAI
import os
import yaml # requires pyyaml
import pandas as pd
from ollama import chat, ChatResponse, Client
from .logger import init_log_folder, log_interaction
from pathlib import PurePath
from datasets import load_dataset
from .runner import BenchRunner
import sys
from .response import StringAnswer, StringJustification, IntAnswer, IntJustification

from .scorers import scoring_fx_list, contains, exact_match

from .utils import concatenator_id_generator, selector_id_generator

prompt_id_fx = {'concatenator_id_generator':concatenator_id_generator,
                'selector_id_generator':selector_id_generator}

class Task:
    """
    defines a basic prompt task with a simple scoring function
    """

    def __init__(self, task_name, template, reference=None, scoring_function=None,
                  variant_values = None, storage_type = 'yaml', description = None, 
                  prompt_id_generator_fx = concatenator_id_generator,
                  format='StringAnswer'):
        """
        init a task object from a prompt and reference, and a scoring function. If no scoring function is provided, defaults to exact match.

        Parameters
        ----------
        dir : string or path
            directory containing the task assets
        prompt: string
            prompt template
        scoring_function : function handle or string
            if string, must be name of built in eval function provided here
        reference: string,  number, or list of strings or numbers the same shape as variant values, 
            solution that will be passed with the model answer to the scoring function,
        variant_values: 
            dicttionary or list of dictiornaries with values to fill in a template, if the task is a template based task. If provided, the prompt will be used as a template and the values in variant_values will be used to fill in the template to create the final prompts for the task. The reference should then be a list of answers corresponding to each prompt variant.
        """
        self.name = task_name
        self.task_id = task_name.strip().replace(" ", "_").lower() 
        self.description = description 

        self.template = template
        self.variant_values = variant_values
        self.reference = reference

        # set up to name individual prompts
        if not callable(prompt_id_generator_fx):
            prompt_id_generator_fx  = prompt_id_fx[prompt_id_generator_fx]
        self.prompt_id_generator = prompt_id_generator_fx
        
        # setup for response format
        mod = sys.modules[__name__]
        self.FormatClass = getattr(mod,format)

        self.storage_type = storage_type
        if scoring_function: 
            if isinstance(scoring_function, str):
                self.scoring_function = scoring_fx_list.get(scoring_function, exact_match)
            elif callable(scoring_function):
                self.scoring_function = scoring_function
            else:
                # throw an error that scoring is not valid
                raise ValueError(f"Scoring function {scoring_function} is not valid, must be a string name"+
                           "of a built in function or a function handle")   
        else:
            self.scoring_function = exact_match 

            
    @classmethod
    def from_txt_csv(cls, source_folder, task_name = None, scoring_function = None,
                     prompt_id_generator_fx = concatenator_id_generator):
        '''
        load a template from txt and create task objects for each row of a csv

        folder must contain a template.txt file with the template, and a values.csv file with the values to fill in the template, and the reference answers. The csv should be structured as follows:
        '''


        if not task_name:
            # get the folder name if not provided
            task_name = PurePath(source_folder).parts[-1]
            # decide if using this: .replace("_", " ").title()

        prompt = ""
        with open(os.path.join(source_folder, "template.txt"), "r") as f:
            prompt = f.read()

        values_file = os.path.join(source_folder, "values.csv")
        # load and strip whitespace from column names
        value_answer_df = pd.read_csv(values_file).rename(columns=lambda x: x.strip()) 
        
        variant_values = value_answer_df.drop(columns='reference').to_dict(orient='records')
        reference = value_answer_df['reference'].tolist()

        if 'id' in value_answer_df.columns:
            prompt_id_generator_fx = selector_id_generator
        
        # TODO: improve this 
        if os.path.exists(os.path.join(source_folder, "description.txt")):
            with open(os.path.join(source_folder, "description.txt"), "r") as f:
                description = f.read()
        else:
            description = f"a template based task with template: {prompt} and values like:\n\n {value_answer_df.head().to_markdown()}"

        return cls(task_name, template= prompt, variant_values = variant_values, 
                   description = description, reference=reference, storage_type ='csv', 
                    scoring_function=scoring_function,
                    prompt_id_generator_fx =prompt_id_generator_fx)
    
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
        description = 'give your task a short description '
        return cls(task_name, template= template, variant_values = variant_values, 
                   description = description,  reference='', 
                   storage_type = storage_type, scoring_function = exact_match)


    @classmethod
    def from_yaml(cls, source_folder, task_name = None, scoring_function = None):
        '''
        load a task from a yaml file. The yaml file should have the following structure:
        name: string
        template: string
        values: list of dicts (optional)
        reference: string, number, or list of strings or numbers the same shape as variant values (optional)
        scoring_function: string or function handle (optional)
        '''
        yaml_file = os.path.join(source_folder, "task_info.yml")
        with open(yaml_file, 'r') as file:
            task_dict = yaml.safe_load(file)    
        
        return cls(task_dict['name'], template= task_dict['template'], 
                   variant_values = task_dict['values'], 
                   description = task_dict.get('description', None),
                    reference=task_dict['reference'],
                      storage_type ='yaml', 
                      scoring_function=task_dict.get('scorer', None) or scoring_function,
                    prompt_id_generator_fx =task_dict.get('id_generator', None))

    @classmethod
    def from_dict(cls, task_dict,prompt_id_generator_fx=concatenator_id_generator):
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
            expanded_values = pd.DataFrame(compact_values).to_dict(orient='records') 
        else:
            expanded_values = None
        
        if 'id' in task_dict.keys():
            prompt_id_generator_fx = selector_id_generator
        

        return cls(task_dict.get("name", "unnamed_task"),
                   template = task_dict.get("template", ""), 
                   variant_values=expanded_values,
                   reference = task_dict.get("reference", None), 
                   scoring_function = task_dict.get("scoring_function", None), 
                   description = task_dict.get("description", None),
                   storage_type='yaml',
                    prompt_id_generator_fx =task_dict.get('id_generator', prompt_id_generator_fx))
    
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
            "id_generator":self.prompt_id_generator.__name__ 
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
        # write the template 
        with open(os.path.join(target_folder,self.task_id, 'template.txt'), 'w') as f:
            f.write(self.template)

         
        with open(os.path.join(target_folder,self.task_id, 'description.txt'), 'w') as f:
            f.write(self.description)

        # write the values and answers to a csv
        if self.variant_values:
            value_answer_df = pd.DataFrame(self.variant_values)
        
            value_answer_df.to_csv(os.path.join(target_folder,self.task_id, 'values.csv'), index=False)
    

    
    def run(self, runner=BenchRunner(), log_dir='logs', benchmark=None, bench_path=None):
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
        """

        responses = []

        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        run_log=""
        # Create logging structure for a task within a log directory
        try:
            run_log = init_log_folder(log_dir, runner.model, self.get_dict(), benchmark, bench_path)
        except Exception as e:
            print(f"Couldn't create log directory in {log_dir}...\n{e}")



        for prompt_name, prompt in self.generate_prompts():
            
            error = None
            response = ''
            try:
                match runner.runner_type:
                    case "ollama":
                        completion: ChatResponse = chat(model=runner.model, 
                                                        format = self.FormatClass.model_json_schema(),
                                                        messages=[
                            {
                            'role': 'user',
                            'content':prompt,
                            },
                        ])
                        # print("response: " + response.message.content)
                        response = completion.message.content
                        responses.append(response)

                    case "ollama_api":
                        client = Client(
                            host=runner.api_url if runner.api_url else "http://localhost:11434",
                        )
                        completion = client.chat(
                            runner.model,
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt,
                                },
                            ],
                        )
                        response = completion["message"]["content"]
                        responses.append(response)

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
                        responses.append(response)
                    case _:
                        print(f"Runner type {runner.runner_type} not supported")
                        return None
            except Exception as e:
                error = e
            log_interaction(run_log, prompt_name, prompt, response, str(error))

        

        if self.variant_values:
            self.responses = responses
            # dict(zip([str(v) for v in self.variant_values], responses))
        else:
            self.responses = responses 

        return self.responses


    def score(self, response):
        """
        score the response using the defined function

        Parameters
        ----------
        response : string
            the value to score
        """
        if isinstance(self.reference, list) and isinstance(response, list):
            # TODO: error if the lengths don't match
            # if there are multiple reference answers, score against each 
            scores = [self.scoring_function(resp, ref) for resp,ref in zip(self.reference)]
            return scores
        else:
            return self.scoring_function(response, self.reference)


# additional classes for other types of tasks

# likely an agent task that can pass environment assets

