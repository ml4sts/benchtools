# built in default scoring functions
import json

def exact_match(response, reference):
    '''
    score 1 if the response exactly matches the reference, 0 otherwise
    '''
    response_object = json.loads(response)
    try:
        score = int(response_object['answer'] == reference)
    except:
        score = 0
    return score

def contains(response, reference):
    '''
    score 1 if the reference is contained in the response, 0 otherwise
    '''
    response_object = json.loads(response)

    try:
        if isinstance(reference, list):
            score = int(any(ref in response_object['answer'] for ref in reference))
        else:
            score = int(reference in response_object['answer'])
    except:
        score = 0
    
    return score
    
    
scoring_fx_list = {"exact_match": exact_match, 
              "contains":contains}
