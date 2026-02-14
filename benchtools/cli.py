import os
import click
from benchtools.runner import Bench
from benchtools.betterbench import betterbench, get_score
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
@click.option('-p',  '--path', help="The path where the new benchmark repository will be placed", default=".", type=str)
@click.option('-a', '--about', help="Benchmark describtion. Content will go in the about.md file", default="", type=str)
@click.option('--no-git',      help="Don't make benchmark a git repository. Default is False", is_flag=True)
@click.option('-t', '--tasks', help="Add benchmark tasks to your benchmark (can add multiple). Format: <name> <path>", default=[], type=(str, str), multiple=True)
def init(benchmark_name, path, about, no_git, tasks):
    """
    Initializes a new benchmark.
    
    Even though the command doesn't have any required arguments. If the <benchmark-name> 
    argument wasn't passed the interface will ask for a name and wouldn't continue without one.

    This command is the starting point. With this, the process of creating a benchmark 
    structure and guiding the user into the correct mindset of a benchmark.

    After running this command, the folder structure of the benchmark will be created. 
    Task files will be loaded, the user will be asked a series of questions to demonstrate 
    the correct mindset of benchmarking, and finally, the user will be given the choice to 
    run the benchmark or not.


    """

    if not benchmark_name:
        benchmark_name = click.prompt("Enter the name of your benchmark/project (will be used as folder and repo name)", type=str)
    benchmark_name = benchmark_name.strip().replace(" ", "_").lower()

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
    bench_path = os.path.join(path, benchmark_name)
    
    click.echo(f"Creating {benchmark_name} in {bench_path}")
    benchmark = Bench(benchmark_name, bench_path)

    # Build the benchmark folder
    if benchmark.build(about, no_git, tasks):
        click.echo(f"Built {benchmark_name} benchmark successfully!")

    # TODO: Call betterbench CLI here
    # betterbench()

    # Run?
    to_run = click.confirm("Do you want to run the benchmark now?", default=True)
    if to_run:
        benchmark.run()

## TODO: Is it computationally better to use pickle to save the object in the benchmark folder??


@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
@click.argument('task-name',  required = True, type=str) 
@click.argument('task-path',  required = True, type=str)
def add_task(benchmark_path, task_name, task_path):
    """
    Set up a new task.

    # TODO explain arguments or convert to options. to use help
    benchmark-path: "The path to the benchmark repository where the task will be added."
    task-name: "The name of the task to be added. This will be used as the folder name for the task and should be unique within the benchmark."
    task-path "The relative path to the dataset used for the task. OR any dataset from huggingface that starts with `openai/`"
    """
    bench_path = os.path.abspath(benchmark_path)
    if os.path.exists(bench_path):
        bench_path = bench_path[:-1] if bench_path.endswith('/') else bench_path
        benchmark = Bench(bench_path.rsplit('/',1)[1], bench_path)
        benchmark.add_task(task_name, task_path)
    else:
        click.echo("No benchmark reposiory at " + bench_path)
    

@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
def run(benchmark_path: str):
    """
    Running the benchmark and generating logs
    , help="The path to the benchmark repository where all the task reside."
    """
    bench_path = os.path.abspath(benchmark_path)
    if os.path.exists(bench_path):
        bench_path = bench_path[:-1] if bench_path.endswith('/') else bench_path
        benchmark = Bench(bench_path.rsplit('/',1)[1], bench_path)
        click.echo(f"Running {benchmark.bench_name} now")
        benchmark.run()


@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
@click.argument('task_name', required = True)
def run_task(benchmark_path: str, task_name):
    """
    Running the tasks and generating logs

    , help="The path to the benchmark repository where all the task reside."
    , help="The name of the specific task you would like to run"
    """
    bench_path = os.path.abspath(benchmark_path)
    if os.path.exists(bench_path):
        bench_path = bench_path[:-1] if bench_path.endswith('/') else bench_path
        benchmark = Bench(bench_path.rsplit('/',1)[1], bench_path)
        click.echo(f"Running {task_name} now")
        benchmark.run([task_name])

@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
def score(benchmark_path: str):
    """
    Running the tasks and generating logs

    , help="The path to the benchmark repository where all the task reside."
    , help="The name of the specific task you would like to run"
    """
    bench_path = os.path.abspath(benchmark_path)
    if os.path.exists(bench_path):
        bench_path = bench_path[:-1] if bench_path.endswith('/') else bench_path
        benchmark = Bench(bench_path.rsplit('/',1)[1], bench_path)
        click.echo(f"Scoring {benchmark.bench_name} now...")
        score = get_score()
        click.echo(f"Score: {score}")


# For debugging
if __name__ == '__main__':
    init()