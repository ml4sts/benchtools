import json
def calculated_answer(response,values):
    '''
    example function for calcuating the correct answer from the values
    '''
    # parse the response object
    response_object = json.loads(response)
    # compute the answer
    ref = values['a'] *values['b']
    # check the answer or otherwise calculate
    return int(ref == response_object['answer'])

def check_name_dir(response,values):
    '''
    '''
    # parse the response object
    response_object = json.loads(response)
    return {'name':values['name']==response_object['name'],
            'direction':values['direction']==response_object['direction'],}

def add_justify(response,values):
    response_object = json.loads(response)
    return int('add' in response_object['justification'])