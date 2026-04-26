import json
def calculated_answer_prod(response,values):
    '''
    example function for calcuating the correct answer from the values
    '''
    # parse the response object
    response_object = json.loads(response)
    # compute the answer
    ref = values['a'] *values['b']
    # check the answer or otherwise calculate
    return int(ref == response_object['answer'])