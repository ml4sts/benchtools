# module to run benchmarks

class Bench():
    '''
    '''
    def __init__(dir, model):
        # check dir for tasks and load them

        self.tasks

        self.model = model

    def run(self):
        '''
        '''
        for task in self.tasks:
            task.run(self.model)