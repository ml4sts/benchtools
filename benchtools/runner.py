# module to run benchmarks
import pandas
import yaml

class Bench():
    '''
    '''
    def __init__(dir, target_dir):
        '''
        '''
        # load tasks from file strucutre and instantiate task objects for each, store those in a list.
        #    loading will 
        self.tasks

        

    def run(self, model):
        '''
        
        '''
        for task in self.tasks:
            task.run(model)

    # possibly private method? 
    def from_txt_csv():
        '''
        load a template from txt and create task objects for each row of a csv
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor

        return self

    
    def from_yaml():
        '''
        laod from a yaml
        '''