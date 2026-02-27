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

@dataclass
class ChecklistItem:
    # question: Question # Again, we'll see...
    skipped: bool
    response: str
    justification: str
    score: int
    # criteria: list[str]

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
    click.echo("Entering interactive session for BetterBench!")
    click.echo("This interactive session is meant guide the benchmark to follow " \
                "the standards developed by reuel et. al. named the BetterBench Checklist!")
    click.echo("This interactive session is optional and you can always come back " \
                "to it with the `betterbench resume` command")
    
    # Load existing BetterBench checklist if applicable 
    bench_checklist={}
    checklist_path = os.path.join(bench_path, "betterbench.yml")
    if os.path.exists(checklist_path):
        with open(checklist_path, 'r') as f:
           bench_checklist = yaml.safe_load(f)
    
    if not bench_checklist:
        # Create checklist items and add them to new checklist
        bench_checklist={}
        for question in main_checklist.keys():
            # print(question) # Debugging
            item = ChecklistItem(
                skipped=True,
                response="",
                justification="",
                score=0,
            )
            bench_checklist[question] = asdict(item)

        # Save empty checklist into the benchmark repo
        if os.path.exists(bench_path):
            with open(checklist_path, 'w') as f:
                yaml.dump(bench_checklist, f)

    
    # TODO: check if want to change answer on any questions

    # Loop until user opts out 
    for question, criteria in main_checklist.items(): 
        # TODO: add if(bench_checklist[skipped])
        # print(question) # DEbugging
        # # print(vals)
        available_choices = ["yes", "no", 'q', '']
        available_choices+= ['n/a'] if len(criteria) >4  else []
        
        choice = click.prompt(f"{question}?\nEnter to skip. q to end this session...", 
                              type=click.Choice(available_choices , case_sensitive=False), 
                              show_choices=True, default='')
        
        # TODO: check for n/a
        # Check for user opt out
        match choice:
            case 'q':
                break    
            case '':
                continue
            case 'no':
                item = ChecklistItem(
                                    skipped=False,
                                    response=choice,
                                    justification=criteria[0],
                                    score=0,
                )
                
            case 'yes':
                criteria_text = "\n ".join([f"{i*5}- {crit}" for i,crit in enumerate(criteria)])
                score = click.prompt(f"Please pick score level:\n {criteria_text}",
                                       type=click.Choice([0, 5, 10, 15]), show_choices=True, default=5)
                justification = click.prompt("Justification:  ")
                item = ChecklistItem(
                                    skipped=False,
                                    response=choice,
                                    justification=justification,
                                    score=score,
                                    )
        # store this question
        bench_checklist[question] = asdict(item)
        print(bench_checklist[question]) # remove this

        
        # score = calculate_score(choice, justification)
        # checklist[question]['response'] = choice
        # checklist[question]['justification'] = justification
        # checklist[question]['score'] = score

        
        
    print(checklist_path) #debugging 
    # Save current checklist into the benchmark repo
    if os.path.exists(bench_path):
        with open(checklist_path, 'w') as f:
            yaml.dump(bench_checklist, f)


def get_score() -> int:
    return 99
    

