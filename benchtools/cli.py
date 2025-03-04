import click
from task import PromptTask
from runner import Bench

@click.group()
def cli():
    """Benchmark Command-line Interface."""
    pass

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


if __name__ == "__main__":
    cli()
