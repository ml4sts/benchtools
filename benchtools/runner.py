# module to run benchmarks
import pandas
import yaml
import task
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
    def from_txt_csv(task_folder):
        '''
        load a template from txt and create task objects for each row of a csv
        '''
        # using pandas to load the csv is easy, then use python string formatting to set up the final prompt to apss to the task constructor
        textFile = open(task_folder + "task.txt", "r")
        csvFile = pandas.read_csv(task_folder + "values.csv")
        answers = pandas.read_csv(task_folder + "results")
        x = 0
        storedTasks = []
        storedAnswers = []
        while x < len(csvFile):
            processed_prompt = textFile.replace("{a}", csvFile.iloc[x,1])
            processed_prompt.replace("{b}", csvFile.iloc[x, 2])
            storedAnswers.append(answers[x,1])
            storedTasks.append(processed_prompt)
        
        return storedTasks, storedAnswers

    
    def from_yaml():
        '''
        laod from a yaml
        '''