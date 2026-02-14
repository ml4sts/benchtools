import os
import json
import click
import dataclasses
from dataclasses import dataclass

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        #if it is a function, use its string name
        elif hasattr(o, '__call__'):
            return o.__name__
        return super().default(o)

@dataclass
class ChecklistQuestion:
    response: str
    justification: str
    score: int
    criteria: list[str]
    skipped: bool


def calculate_score(response: str, justification: str) -> int:
    if response == 'no':
        return 0
    else:
        TODO


Checklist = [
    # Design
    "The tested capability, characteristic, or concept is defined",
    "How tested capability or concept translates to benchmark task is described",
    "How knowing about the tested concept is helpful in the real world is described",
    "How benchmark score should or shouldn't be interpreted/used is described",
    "Domain experts are involved",
    "Use cases and/or user personas are described", # Has n/a
    "Domain literature is integrated",
    "Informed performance metric choice",
    "Metric floors and ceilings are included"
    "Human performance level is included", # Has n/a
    "Random performance level is included", # Has n/a
    "Automatic evaluation is possible and validated",
    "Differences to related benchmarks are explained",
    "Input sensitivity is addressed",
    # Implementation
    "The evaluation code is available",
    "The evaluation data or generation mechanism is accessible",
    "The evaluation of models via API is supported",
    "The evaluation of local models is supported",
    "A globally unique identifier is added or evaluation instances are encrypted",
    "A task to identify if model is included trained on benchmark data",
    "A script to replicate results is explicitly included",
    "Statistical significance or uncertainty quantification of benchmark results is reported",
    "Need for warnings for sensitive/harmful content is assessed",
    "A build status (or equivalent) is implemented",
    "Release requirements are specified",
    # Documentation
    "Requirements file or equivalent is available",
    "Quick-start guide or demo is available",
    "In-line code comments are used",
    "Code documentation is available",
    "Accompanying paper is accepted at peer-reviewed venue",
    "Benchmark construction process is documented",
    "Test tasks & rationale are documented",
    "Assumptions of normative properties are documented",
    "Limitations are documented",
    "Data collection, test environment design, or prompt design process is documented",
    "Evaluation metric is documented",
    "Applicable license is specified",
    # Maintenance
    "Code usability was checked within the last year",
    "Maintained feedback channel for users is available",
    "Contact person is listed"
]



def betterbench(checklist_path="/work/pi_brownsarahm_uri_edu/ayman_uri/BenchTools/testRuns/111/betterbench.json") -> dict:
    """
    The checklist below is based on the benchmark quality assessment proposed in BetterBench. It is supposed to help authors identify if they adhere to best practices in their benchmark development. If you want to have your benchmark added to the BetterBench Repository, please also fill out the justifications. These should be about one sentence long each, and include the page numbers of your paper or your webpage where the information can be found. You can also copy-paste quotes from any of your publicly available materials here as evidence. In this case, please also add a link to the source.
    Reuel et. al.

    :param checklist_path: _description_, defaults to "/work/pi_brownsarahm_uri_edu/ayman_uri/BenchTools/testRuns/1111/betterbench.json"
    :type checklist_path: str, optional
    :return: _description_
    :rtype: dict
    """

    checklist={}
    if os.path.exists(checklist_path):
        with open(checklist_path) as f:
           checklist = json.load(f)
    
    if not checklist:
        checklist = {}
        for question in Checklist:
            item = ChecklistQuestion(
                skipped=True,
                response="",
                justification="",
                score=0,
                criteria=[]
            )
            checklist[question] = item
    
    
    click.echo("Entering interactive session for BetterBench!")
    click.echo("This interactive session is meant to help you think about your benchmark in through the standards develope by reuel et. al. that are the BetterBench Checklist!")
    click.echo("This interactive session is optional and you can always come back to it with the `betterbench resume` command")
    
    # TODO: check if want to change answer on any questions

    # Loop until user opts out 
    for question, vals in checklist.items(): 
        # print(question)
        # print(vals)
        choice = click.prompt(f"{question}?\nEnter to skip. q to end this session...", type=click.Choice(["yes", "no", "n/a", 'q', ''], case_sensitive=False), show_choices=True, default='')

        # Check for user opt out
        if choice == 'q':
            break
        elif choice == '':
            continue
        else:
            justification = click.prompt("Justification? ")
        
        score = calculate_score(choice, justification)
        checklist[question]['response'] = choice
        checklist[question]['justification'] = justification
        checklist[question]['score'] = score

        
            
        
    json.dump(checklist, open(checklist_path, "w"), indent=4, cls=EnhancedJSONEncoder)

    exit(0)


def get_score() -> int:
    return 99
    