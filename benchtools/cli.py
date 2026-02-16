import os
import click
from benchtools.task import Task
from benchtools.benchmark import Bench
from benchtools.runner import BenchRunner
from benchtools.betterbench import better_session, get_score
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
    bench_path = os.path.join(path, folder_name)

    # tasks = []
    # if task_sources:
    #     # TODO: Look at content to create Task objects and add them to tasks
    #     continue

    click.echo(f"Creating {benchmark_name} Benchmark in {bench_path}")
    benchmark = Bench(name =benchmark_name, bench_path = bench_path, 
                      concept = about)

    # Build the benchmark folder
    if benchmark.initialize_dir(no_git):
        click.echo(f"Created {benchmark_name} benchmark successfully!")

    # TODO: Call betterbench CLI here
    if click.confirm("Do you want to go through the BetterBench checklist now?", default=True) :
        better_session(bench_path)

    # Run?
    if benchmark.tasks:
        to_run = click.confirm("Do you want to run the benchmark now?", default=True)
        if to_run:
            # TODO: Get runner info and create runner object?
            # benchmark.run(runner)
            benchmark.run()



@benchtool.command()
@click.argument('task-name',  required = True, type=str) 
@click.option('-p','--benchmark-path', default='.', help="The path to the benchmark repository where the task will be added.", type=str)
@click.option('-s','task-source', type=str,help="The relative path to  content that already exists`", required=True)
@click.option('-t','--task-type', type=click.Choice(['folders', 'list']), help="The type of the task content being added. Options are csv or yml", required=True)
def add_task(task_name, bench_path, task_source,task_type):
    """
    Set up a new task.

    """
    
    if os.path.exists(bench_path):
        benchmark = Bench.load(bench_path)
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
            task = Task(name=task_name, template= "fill in your prompt template here",
                            description = "add a description of your task here",
                        storage_type=storage_type)
        else:
            click.echo("Invalid task content type. Either provide content with --task-source or specify the type of task content with --type.")
            exit(4356)

        # TODO: handle adding to benchmark with metadata
        # benchmark.add_task(task)
        task.write(bench_path)
        click.echo(f"Added {task_name} to {benchmark.bench_name} benchmark successfully!")
    else:
        click.echo("No benchmark reposiory at " + bench_path)


@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
@click.argument('task_name', required = True)
def run_task(benchmark_path: str, task_name):
    """
    Running the tasks and generating logs

    , help="The path to the benchmark repository where all the task reside."
    , help="The name of the specific task you would like to run"
    """
    
    benchmark = Bench.load(benchmark_path)
    click.echo(f"Running {task_name} now")
    benchmark.run([task_name])

@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
def run(benchmark_path: str):
    """
    Running the benchmark and generating logs
    , help="The path to the benchmark repository where all the task reside."
    """
    # check folder to see if folder or yaml type to load benchmark
    if os.path.isdir(benchmark_path):
        content = os.listdir(benchmark_path)
        if 'tasks.yml' in content:
            benchmark = Bench.from_yaml(benchmark_path)
        else:
            benchmark = Bench.from_folders(benchmark_path)
    click.echo(f"Running {benchmark.bench_name} now")
    benchmark.run()


@click.group()
def betterbench():
    """
    Launch the BenchBench interactive tool
    """
    pass
    
@betterbench.command()
@click.argument('bench-path', default='.', type=str)
def resume(bench_path: str):
    """
    Running the betterbench interactive session
    """
    # benchmark = Bench.load(bench_path) # IS this needed? Maybe just check if written?
    better_session(bench_path)

    

@betterbench.command()
@click.argument('bench-path', required = True, type=str)
def score(bench_path: str):
    """
    Running the betterbench scoring function
    """
    # benchmark = Bench.load(bench_path) # IS this needed? Maybe just check if written?
    click.echo(f"Scoring now...")
    score = get_score()
    click.echo(f"Score: {score}")




