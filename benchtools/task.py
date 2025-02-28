#  defines a class object for a task
from ollama import generate
from scorerers import exact_match

scoring_fx = {'exact_match':exact_match}

class PromptTask:
    '''
    defines a basic prompt task with a simple scoring function
    '''
    def __init__(self,prompt=None,scoring_function=None, reference=None):
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
            solution that will be passed with the model answer

        '''
        self.prompt = prompt
        if type(scoring_function) == str:
            self.scoring_function = scoring_fx[scoring_function]
        else:
            self.scoring_function = scoring_function

        self.reference = reference


    def run(self,model):
        '''
        '''
        return generate(model,self.prompt)


    def score(self,response):
        '''
        score the response using the defined function

        Parameters
        ----------
        response : string
            the value to score
        '''
        return self.scoring_function(response,self.reference)
        

# additional classes that inherit for other types of tasks

# likely an agent task that can pass environment assets