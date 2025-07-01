import click
# from task import PromptTask
# from runner import Bench
import os

@click.group()
def cli():
    """
    BenchTools is a tool that helps researchers set up benchmarks.
    """
    pass

@click.command()
@click.argument('bench_name')
def generate_demo_bench(bench_name):
    """
    Generate a demo benchmark
    """

    # Set up directory for the demo bench
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    # Change this to use the current path or possibly take a path as an argument
    demo_bench_path = os.path.join(parent_dir, bench_name)
    os.makedirs(demo_bench_path, exist_ok=True)

    tasks_folder = os.path.join(demo_bench_path, "Tasks")
    report_folder = os.path.join(demo_bench_path, "Report")

    os.makedirs(tasks_folder, exist_ok=True)
    os.makedirs(report_folder, exist_ok=True)

    click.echo(f"Folder '{bench_name}' created at {demo_bench_path}")
    click.echo("Subfolders 'Tasks' and 'Report' created.")


# What us creating a new task
@click.command()
@click.argument('task_name')
def add_task(task_name):
    """Creating a new task."""
    new_task = PromptTask()
    click.echo("Adding " + task_name)


@click.command()
@click.argument('task_name')
def run_task(task_name):
    """Running a task."""
    
    click.echo(result)


cli.add_command(add_task)
cli.add_command(run_task)
cli.add_command(generate_demo_bench)


if __name__ == "__main__":
    cli()
