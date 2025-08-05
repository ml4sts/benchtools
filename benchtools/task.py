#  defines a class object for a task
from ollama import generate
from scorerers import exact_match

scoring_fx = {'exact_match':exact_match}

class PromptTask:
    '''
    defines a basic prompt task with a simple scoring function
    '''
    def __init__(self,prompt=None,scoring_function=None, reference=None, runner_type='ollama'):
        '''
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
        '''
        self.prompt = prompt
        if type(scoring_function) == str:
            self.scoring_function = scoring_fx[scoring_function]
        else:
            self.scoring_function = scoring_function

        self.reference = reference
        self.runner_type = runner_type

    def run(self,model):
        '''
        '''
        #  this should actually be a better switch structure 
        #  these types should be documented in the constructor method (init)
        if self.runner_type == 'ollama':
            return generate(model,self.prompt,)


    def score(self,response):
        '''
        score the response using the defined function

        Parameters
        ----------
        response : string
            the value to score
        '''
        return self.scoring_function(response,self.reference)
        

# additional classes for other types of tasks

# likely an agent task that can pass environment assets