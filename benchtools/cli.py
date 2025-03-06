import click
from task import PromptTask
from runner import Bench
import os

@click.group()
def cli():
    """Benchmark Command-line Interface."""
    pass

@click.command()
@click.argument('bench_name')
def generate_demo_bench(bench_name):
    current_dir = os.getcwd()
    parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
    new_folder_path = os.path.join(parent_dir, bench_name)
    os.makedirs(new_folder_path, exist_ok=True)
    click.echo(f"Folder '{bench_name}' created at {new_folder_path}")

    tasks_folder = os.path.join(new_folder_path, "Tasks")
    report_folder = os.path.join(new_folder_path, "Report")

    os.makedirs(tasks_folder, exist_ok=True)
    os.makedirs(report_folder, exist_ok=True)

    click.echo("Subfolders 'Tasks' and 'Report' created.")



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
