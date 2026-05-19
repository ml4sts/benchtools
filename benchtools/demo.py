import os
import yaml
import importlib.resources as resources
from pathlib import Path
import shutil



def copy_demo_files(demo_name:str, dest_dir: str) -> None:
    '''
    Copy demo to desination 
    
    Parameters
    -----------
    demo_name :str
        name of demo 
    dest_dir : path or str
        target destination
    '''
    dest_path = Path(dest_dir,demo_name) 
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Access the assets directory from your package
    assets = resources.files('benchtools').joinpath('assets','demos',demo_name)
    
    for item in assets.iterdir():
        if item.is_file():
            shutil.copy(item, dest_path / item.name)
        elif item.is_dir():
            shutil.copytree(item, dest_path / item.name)

def list_demos(concept=False):
    '''
    list available demos
    '''
    demo_dir = resources.files('benchtools').joinpath('assets','demos')
    demo_dirs = demo_dir.iterdir()
    demos = []
    for demo_path in demo_dir.iterdir():
        info_path = demo_path.joinpath('info.yml')
        with resources.as_file(info_path) as p:
            with open(p,'r') as file:
                info = yaml.safe_load(file)
        
        if concept:
            demos.append(f'{info['bench_name']}: {info['concept']}')
        else: 
            demos.append(info['bench_name'])


    return demos
    
