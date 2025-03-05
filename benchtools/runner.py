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
        textFile = open(self.dir, "r")
        csvFile = pandas.read_csv(self.dir)
        x = 0
        storedPrompts = []
        while x < len(csvFile):
            processed_prompt = textFile.replace("{a}", csvFile.iloc[x,1])
            processed_prompt.replace("{b}", csvFile.iloc[x, 2])
            storedPrompts.append(processed_prompt)

        
        
        return storedPrompts

    
    def from_yaml():
        '''
        laod from a yaml
        '''