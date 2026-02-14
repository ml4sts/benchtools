# built in default scoring functions

def exact_match(response, reference):
    '''
    score 1 if the response exactly matches the reference, 0 otherwise
    '''
    return int(response == reference)

def contains(response, reference):
    '''
    score 1 if the reference is contained in the response, 0 otherwise
    '''
    if isinstance(reference, list):
        return int(any(ref in response for ref in reference))
    else:
        return int(reference in response)
    
scoring_fx_list = {"exact_match": exact_match, 
              "contains":contains}
