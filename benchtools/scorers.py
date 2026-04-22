# built in default scoring functions
import json

def exact_match(response, reference):
    '''
    score 1 if the response exactly matches the reference, 0 otherwise
    '''
    response_object = json.loads(response)
    
    return int(response_object['answer'] == reference)

def contains(response, reference):
    '''
    score 1 if the reference is contained in the response, 0 otherwise
    '''
    response_object = json.loads(response)
    
    if isinstance(reference, list):
        return int(any(ref in response_object['answer'] for ref in reference))
    else:
        return int(reference in response_object['answer'])
    
scoring_fx_list = {"exact_match": exact_match, 
              "contains":contains}
