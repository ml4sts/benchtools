import os
import yaml
# import json
import click
# import dataclasses
from dataclasses import dataclass, asdict
from .utils import load_asset_yml
# from click_prompt import choice_option


# class EnhancedJSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if dataclasses.is_dataclass(o):
#             return dataclasses.asdict(o)
#         #if it is a function, use its string name
#         elif hasattr(o, '__call__'):
#             return o.__name__
#         return super().default(o)

# We'll see if this is needed:
@dataclass
class Question:
    question_text: str
    justification: str
    criteria: list[str]
    NA: bool

# @dataclass
# class ChecklistItem:
#     # question: Question # Again, we'll see...
#     skipped: bool
#     response: str
#     justification: str
#     score: int
#     # criteria: list[str]

# def calculate_score(response: str, justification: str) -> int:
#     if response == 'no':
#         return 0
#     else:
#         TODO


def better_session(bench_path) -> dict:
# def betterbench(checklist_path) -> dict:
    """
    The checklist below is based on the benchmark quality assessment proposed in
    BetterBench. It is supposed to help authors identify if they adhere to best 
    practices in their benchmark development. If you want to have your benchmark
    added to the BetterBench Repository, please also fill out the justifications.
      These should be about one sentence long each, and include the page numbers 
      of your paper or your webpage where the information can be found. You can 
      also copy-paste quotes from any of your publicly available materials here 
      as evidence. In this case, please also add a link to the source.
    Reuel et. al.

    To understand methodology and justification of questions please view 
    [BetterBench Methodology](https://betterbench.stanford.edu/methodology.html)


    ---- 
    checklist_path: Path to Benchmark's betterbench checklist file
    
    """

    
    main_checklist = load_asset_yml("betterbench.yml") 

    # Intro
    welcome_prompt='''
#########################################################################
# Entering interactive session for BetterBench!                         #
# This interactive session is meant guide the benchmark to follow the   #
# standards developed by reuel et. al. named the BetterBench Checklist! #
# This interactive session is optional and you can always come back to  #
# it with the `betterbench resume` command                              #
#########################################################################

'''
    click.echo(welcome_prompt)
    
    # Confirm the benchmark exists
    if not os.path.exists(bench_path):
        click.echo("No benchmark reposiory at " + bench_path)

    # Load existing BetterBench checklist if applicable 
    checklist_path = os.path.join(bench_path, "betterbench.yml")
    bench_checklist={}
    if os.path.exists(checklist_path):
        with open(checklist_path, 'r') as f:
           bench_checklist = yaml.safe_load(f)

    
    # Check if want to change answer on any questions
    review = click.confirm("Would you like to review previous respopnses? ", default=False)
    
    opt_out = False
    # Loop until user opts out 
    for question, criteria in main_checklist.items(): 
        # declare an empty checklist item
        if not question in bench_checklist:
            bench_checklist[question] = dict(skipped=True,
                                                response="",
                                                justification="",
                                                score=0)
        if not opt_out:
            available_choices = ["yes", "no", 'q', '']
            available_choices+= ['na'] if len(criteria) >4  else []

            if bench_checklist[question]['skipped']:
                choice = click.prompt(f"{question}?\nEnter to skip. q to end this session...",
                                  type=click.Choice(available_choices , case_sensitive=False),
                                  show_choices=True, default='')
            elif review:
                previous = f'reviewing {question}:\nResponse: {bench_checklist[question]['response']}\nJustification: '\
                    f'{bench_checklist[question]['justification']}\nScore: {bench_checklist[question]['score']}'
                click.echo(previous)
                choice = click.prompt(f"{question}?\nEnter to skip. q to end this session...",
                                  type=click.Choice(available_choices , case_sensitive=False),
                                  show_choices=True, default='')
            else:
                continue

            match choice:
                case 'q':
                    opt_out = True
                    continue
                case '':
                    continue
                case 'no':
                    bench_checklist[question]['skipped'] = False
                    bench_checklist[question]['response'] = choice
                    bench_checklist[question]['justification'] = criteria[0]
                    bench_checklist[question]['score'] = 0
                case 'na':
                    bench_checklist[question]['skipped'] = False
                    bench_checklist[question]['response'] = choice
                    bench_checklist[question]['justification'] = criteria[4]
                    bench_checklist[question]['score'] = None
                case 'yes':
                    criteria_dict = {i*5: crit for i,crit in enumerate(criteria)}
                    if len(criteria) >4: criteria_dict.pop(20) # n/a criterion
                    criteria_text = "\n ".join([f"{i}- {crit}" for i,crit in criteria_dict.items()])
                    score = click.prompt(f"Please pick score level:\n {criteria_text}",
                                           type=click.Choice([0, 5, 10, 15]), show_choices=True, default=5)
                    justification = click.edit(f"Justification: {criteria_dict[score]}")
                    justification = justification.split('Justification: ', 1)[1].strip() if not justification==None else criteria_dict[score]
                    bench_checklist[question]['skipped'] = False
                    bench_checklist[question]['response'] = choice # no if score==0?
                    bench_checklist[question]['justification'] = justification
                    bench_checklist[question]['score'] = score
            
    # Save current checklist into the benchmark repo
    with open(checklist_path, 'w') as f:
        yaml.dump(bench_checklist, f)


def get_score() -> int:
    return 99
    

