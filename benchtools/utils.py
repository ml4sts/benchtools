import os
import yaml
import importlib.resources as resources

def load_asset(filename):
    '''
    pass sub path to the needed file from assets as separate parameters and load the 
    content from the file
    '''
    # template_rel = os.path.join('assets', *args)
    # template_path = resources.path(__name__, template_rel)
    # with open(template_path, 'r') as tmpt_f:
    #     template = tmpt_f.read()
    template_dir = resources.files('benchtools').joinpath('assets',filename)
    # with open(resources.as_file(template_dir),'r') as f:
    template = template_dir.read_text()
    
    return(template)

def load_asset_yml(filename):
    '''
    pass sub path to the needed file from assets as separate parameters and load the 
    content from the file
    '''
    template_dir = resources.files('benchtools').joinpath('assets',filename)
    with resources.as_file(template_dir) as p:
        with open(p,'r') as file:
            template = yaml.safe_load(file)
    
    return(template)

def concatenator_id_generator(name,values_dict):
    '''
    create an id for individual prompts from task name and values
    '''

    values = values_dict.values()
    return name +'_' + '-'.join([str(v) for v in values])

def selector_id_generator(name,values_dict):
    '''
    if provided
    '''
    return values_dict['id']