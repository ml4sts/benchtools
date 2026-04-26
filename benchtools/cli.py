import os
import click
import json
import pandas as pd
from pathlib import Path, PurePath
from datetime import datetime
from benchtools.task import Task
from benchtools.benchmark import Bench
from benchtools.runner import BenchRunner, BenchRunnerList
from benchtools.betterbench import BetterCheckList
from .demo import copy_demo_files, list_demos

# from task import PromptTask

@click.group()
def benchtool():
    """
    BenchTools is a tool that helps researchers set up benchmarks.
    """
    pass

# Initialize the benchmark 
@benchtool.command()
@click.argument('benchmark-name', required=False)
@click.option('-p',  '--path', help="The path where the new benchmark repository will be placed", 
              default=".", type=str)
@click.option('-a', '--about', help="Benchmark describtion. Content will go in the about.md file",
               default="", type=str)
@click.option('--no-git',      help="Don't make benchmark a git repository. Default is False", 
              is_flag=True)
# @click.option('-t', '--tasks', help="Add benchmark tasks to your benchmark (can add multiple). Format: <name> <path>", default=[], type=(str, str), multiple=True)
def init(benchmark_name, path, about, no_git):
    """
    Initializes a new benchmark.
    
    Benchmark-name is required, if not provided, requested interactively.

    this command creates the folder for the benchmark. 

    """

    if not benchmark_name:
        benchmark_name = click.prompt("Enter the name of your benchmark (will be used as folder and repo name)", type=str)
    benchmark_name = benchmark_name.strip() # Strip from surrouding whitespace

    # TODO: Handle existing benchmark
    if not os.path.exists(path):
        try:
            path = path[:-1] if path.endswith('/') else path
            split_path = path.rsplit('/', 1)
            if split_path[1] == benchmark_name:
                path = path[0]
            else:
                raise ValueError("The passed path doesn't exist.")
        except Exception as e:
            # click.echo("The passed path doesn't exist.", nl=False)
            # path = click.prompt("Enter an existing path where the new benchmark folder will be created.")
            click.echo("The passed path doesn't exist.")
            exit(4356)

    # create full path
    folder_name = benchmark_name.replace(" ", "_").lower()
    benchmark_path = os.path.join(path, folder_name)

    tasks = []
    tasks_desired = click.confirm("Do you want to add any tasks now?")
    while tasks_desired:
        tasks_exist = click.confirm("Do you have task files already prepared?", default=False)
        if tasks_exist:
            path = click.prompt('Enter the path to the files')
        else:
            template_type = click.prompt("What type of template would you like to add?",
                                          type=click.Choice(['csv', 'yaml']), 
                                          show_choices=True)
            task_name = click.prompt("what is the name of your task?")
            tasks.append(Task.from_example(task_name,template_type))

        tasks_desired = click.confirm("Do you want to add another?")


    click.echo(f"Creating {benchmark_name} Benchmark in {benchmark_path}")
    benchmark = Bench(name =benchmark_name, benchmark_path = benchmark_path, 
                      concept = about, tasks=tasks)

    # Build the benchmark folder
    if benchmark.initialize_dir(no_git):
        click.echo(f"Created {benchmark_name} benchmark successfully!")

    # TODO: Call betterbench CLI here
    if click.confirm("Do you want to go through the BetterBench checklist now?", default=True) :
        better_session(benchmark_path)

    # Run?
    if benchmark.tasks:
        to_run = click.confirm("Do you want to run the benchmark now?", default=True)
        if to_run:
            # TODO: Get runner info and create runner object?
            # benchmark.run(runner)
            benchmark.run()



@benchtool.command()
@click.argument('task-name',  required = True, type=str, ) 
@click.option('-p','--bench-path', default='.', help="The path to the benchmark repository where the task will be added.", type=str)
@click.option('-s','--task-source', type=str,help="The relative path to  content that already exists`", required=True)
@click.option('-t','--task-type', type=click.Choice(['folders', 'list']), 
              help="The type of the task content being added. Options are csv or yml", required=True)
def add_task(task_name, benchmark_path, task_source,task_type):
    """
    Set up a new task.

    """
    
    benchmark = Bench.load(benchmark_path)    
    
    # Create Task object
    if task_source: 
        if os.path.isdir(task_source):
            task = Task.from_txt_csv(task_source)
        elif os.path.isfile(task_source):
            task = Task.from_yaml(task_source)
    elif task_type:
        match task_type: 
            case 'folders':
                storage_type = 'csv'
            case 'list':
                storage_type = 'yaml'
        task = Task.from_example(name=task_name, storage_type=storage_type)
        # task.write()
    else:
        click.echo("Invalid task content type. Either provide content with --task-source or specify the type of task content with --type.")
        exit(4356)

    # Add Task to Bench, will write as well
    benchmark.add_task(task)
    click.echo(f"Added {task_name} to {benchmark.bench_name} benchmark successfully!")



@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
@click.argument('task_name', required = True)
@click.option('-r', '--runner-type', type=click.Choice(['ollama', 'openai', 'bedrock']), 
                                                       default="ollama", help="The engine that will run your LLM.")
@click.option('-m', '--model', type=str, default="gemma3",
               help="The LLM to be benchmarked.")
@click.option('-a', '--api-url', type=str, default=None, 
              help="The api call required to access the runner engine.")
@click.option('-l', '--log-path', type=str, default=None,
               help="The path to a log directory.")
def run_task(benchmark_path: str, task_name, runner_type, model, api, log_path):
    """
    Running the tasks and generating logs

    , help="The path to the benchmark repository where all the task reside."
    , help="The name of the specific task you would like to run"
    """
    
    # Create BenchRunner object
    runner = BenchRunner(runner_type, model, api)

    benchmark = Bench.load(benchmark_path)

    
    click.echo(f"Running {task_name} of benchmark {benchmark.bench_name} now")
    benchmark.run_task(task_name, runner, log_path)

@benchtool.command()
@click.argument('benchmark-path', required = False, 
                type=click.Path(), default=Path('.'),)
@click.option('-r', '--runner-type', type=click.Choice(['ollama', 'openai', 'bedrock']),
               default="ollama", help="The engine that will run your LLM.")
@click.option('-m', '--model', type=str, default="gemma3", 
              help="The LLM to be benchmarked.")
@click.option('-a', '--api', type=str, default=None, 
              help="The api base url required to access the runner engine.")
@click.option('-l', '--log-path', type=str, default=None, 
              help="The path to a log directory.")
@click.option('-s','--score',is_flag=True,
              help='flag to score each task while running')
@click.option('-R','--runner-file', default=None, 
              help='use runner.yml configuration, if provided overrides options')

def run(benchmark_path: str, runner_type: str, 
        model: str, api: str, log_path: str,
        score: bool, runner_file):
    '''
    Run the benchmark, generate logs, and optionally sore
    '''

    # Create BenchRunner object
    if runner_file:
        if not(os.path.exists(runner_file)):
            runner_file = os.path.join(benchmark_path,runner_file)
        runner_list = BenchRunnerList.from_file(runner_file)
    else:
        runner_list = BenchRunnerList([BenchRunner(runner_type, model, api)])

    benchmark = Bench.load(benchmark_path)
    
    
    for runner in runner_list.runners:
        click.echo(f"Running {benchmark.bench_name} on {runner}")
        benchmark.run(runner, log_path,score)

@benchtool.command()
@click.argument('benchmark-path', required = False, type=str, default='.')
@click.option('-r', '--result-id', type=str, default='last', 
              help="runs to score: 'last','all' or specific ids")
@click.option('-c','--csv',is_flag=True,
              help ='save csv of eval in additon to json')

@click.option('-C','--collate',is_flag=True,
              help='collate scores rather than recomputing them')
# TODO: change to accept list
def score(benchmark_path: str, result_id,csv,collate):
    """
    Running the benchmark and generating logs
    Parameters:
        benchmark-path: The path to the benchmark repository where all the task reside.
    """
    # if not provided do the last one for each model-task combination
    
    benchmark = Bench.load(benchmark_path)
    
    score_list = benchmark.score(run=result_id,collate=collate)

    timestamp = str(int(datetime.now().timestamp()))
    eval_base = os.path.join(benchmark_path,'eval_'+timestamp)
    with open(eval_base+'.json','w') as f:
        json.dump(score_list,f)

    

    if csv:
        df_in = pd.DataFrame(score_list)
        step_df = df_in['steps'].apply(pd.Series).rename(columns = lambda c: 'step_'+c)
        step_expanded = [step_df[c].apply(pd.Series).rename(columns = lambda ci: c + '_' +ci) 
                         for c in step_df.columns]
        df = pd.concat([df_in.drop(columns='steps')] + step_expanded,
                       axis=1)
        df.to_csv(eval_base+'.csv',index=False)
    
    click.echo('Saved Eval: '+eval_base)


@benchtool.group()
def demo():
    '''
    demo benchmarks package with benchtools
    '''
    pass

@demo.command()
@click.option('-n','--demo-name',default=None)
@click.option('-t','--target-dir',default = '.',
              help='target directory for the demo')
@click.option('-r','--run',is_flag=True,
              help='optionally, run the demo after sintalling')
def install(demo_name,target_dir, run):
    '''
    install and optionally run a demo
    '''
    available_demos = list_demos()

    # if not valid, warn and delete
    if not(demo_name in available_demos):
        click.echo(f'{demo_name} does not exist')
        demo_name = None

    # if not selected (or deleted, ask for choice)
    enumerated_demos = '\n'.join([f'{str(i)}: {d}' 
                                  for i,d in enumerate(available_demos)])
    if not(demo_name):
        click.echo('Available demos:\n'+enumerated_demos)
        demo_id = click.prompt('Choose a demo ',
                    type=click.Choice(range(len(available_demos))))
        demo_name = available_demos[demo_id]

    copy_demo_files(demo_name,target_dir)
    benchmark_path =os.path.join(target_dir,demo_name)

    if run:
        benchmark = Bench.load(benchmark_path)
    
        click.echo(f"Running {benchmark.bench_name} on  with defaults")
        benchmark.run()
        
@demo.command()
@click.option('-c','--concept',is_flag=True,
              help='include concept descriptions in list')
def list(concept):
    '''
    list available demos
    '''
    demo_list = 'Available Demos:\n- ' + '\n- '.join(list_demos(concept))
    click.echo(demo_list)


@click.group()
def betterbench():
    """
    Launch the BenchBench interactive tool
    """
    pass
    
@betterbench.command()
@click.argument('bench-path', default='.', type=str)
def init(bench_path: str):
    """
    Initiate a betterbench checklist from template.
    Check if user would like to run an interactive session
    """
    checklist = BetterCheckList.from_template()

    # Check if user is interested in running an interactive session
    if click.confirm("Would you like to start an interactive session?", default=False):
        checklist.interactive_session()

    # Save the checklist to the file system
    checklist.save(bench_path)


@betterbench.command()
@click.argument('bench-path', default='.', type=str)
def resume(bench_path: str):
    """
    Running the betterbench interactive session
    """
    # Load the checklist from the file system
    checklist = BetterCheckList.from_file(os.path.join(bench_path, 'betterbench.yml'))
    # Start interactive session
    checklist.interactive_session()
    # Save the checklist to the file system
    checklist.save(bench_path)
    

@betterbench.command()
@click.argument('bench-path', default='.', type=str)
def score(bench_path: str):
    """
    Running the betterbench scoring function
    """
    click.echo(f"Scoring benchmark now...")
    # Load the checklist from the file system
    checklist = BetterCheckList.from_file(os.path.join(bench_path, 'betterbench.yml'))
    checklist.print_score()


