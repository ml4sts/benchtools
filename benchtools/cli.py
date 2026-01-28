import os
import click
from benchtools.runner import Bench
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
def init(benchmark_name:str, path:str, about:str, no_git:bool, tasks:(str,str)):
    """Initializing a new benchmark."""

    if not benchmark_name:
        benchmark_name = click.prompt("Enter the name of your benchmark/project (will be used as folder and repo name)", type=str)
    

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

    # Handle passed path to setup an absolute benchmark path
    if path.startswith('/'):
        abs_path = path
    else:
        abs_path = os.path.abspath(path)
    bench_path = os.path.join(abs_path, benchmark_name)
    
    click.echo(f"Creating {benchmark_name} in {bench_path}")
    benchmark = Bench(benchmark_name, bench_path)
    if benchmark.build(about, no_git, tasks):
        click.echo(f"Built {benchmark_name} benchmark successfully!")

    # TODO: Call betterbench CLI here

    # Run?
    to_run = click.prompt("Would you like to run the benchmark?", type=click.Choice(['y','n'], case_sensitive=False), show_choices=True)
    if to_run in ['y', 'Y']:
        benchmark.run()

## TODO: Is it computationally better to use pickle to save the object in the benchmark folder??

@benchtool.command()
@click.argument('benchmark-path', required = True, type=str)
@click.argument('task-name',  required = True, type=str)
@click.argument('task-path',  required = True, type=str)
def add_task(benchmark_path, task_name, task_path):
    """Set up a new task."""
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
    """Running the benchmark and generating logs"""
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
    """Running the tasks and generating logs"""
    bench_path = os.path.abspath(benchmark_path)
    if os.path.exists(bench_path):
        bench_path = bench_path[:-1] if bench_path.endswith('/') else bench_path
        benchmark = Bench(bench_path.rsplit('/',1)[1], bench_path)
        click.echo(f"Running {task_name} now")
        benchmark.run([task_name])