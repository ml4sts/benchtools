import os
import yaml
import importlib.resources as resources
from pathlib import Path




def load_demo(demo_name):
    demo_dir = resources.files('benchtools').joinpath('demo',demo_name)
    # with open(resources.as_file(template_dir),'r') as f:
    template = demo_dir.read_text()

def load_asset(filename):
    '''
    pass sub path to the needed file from assets as separate parameters and load the 
    content from the file
    '''
    
    file_path = resources.files('benchtools').joinpath('assets',filename)
    
    template = file_path.read_text()
    
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

    values = [v for v in values_dict.values() if not(v=='prompt_id')]
    return name +'_' + '-'.join([str(v) for v in values])

def selector_id_generator(name,values_dict):
    '''
    if provided
    '''
    return values_dict['id']