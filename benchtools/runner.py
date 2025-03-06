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

    
    def from_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
        self.tasks = []
        for each in data:
            template = each.get('template', '')
            values = each.get('values', [])
            processed_values = []
            for val in values:
                for key, value in val.items():
                    if isinstance(value, str): 
                        processed_values.append((key, list(map(int, value.split(',')))))
                    else:
                        processed_values.append((key, value))
            keys = [key for key, _ in processed_values]
            value_lists = [value for _, value in processed_values]
            value_combinations = list(zip(*value_lists))
            for combination in value_combinations:
                value_dict = dict(zip(keys, combination))
                temp = template.format(**value_dict)
                self.tasks.append(temp)
        return self.tasks
