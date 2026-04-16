import os
import yaml
import click
from .utils import load_asset_yml
# from click_prompt import choice_option


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
           checklist = yaml.safe_load(f)
           if checklist: bench_checklist = checklist

    
    # Check if want to change answer on any questions
    review = click.confirm("Would you like to review previous respopnses? ", default=False)
    
    opt_out = False
    # Loop until user opts out 
    for new_item in main_checklist: 
        question = new_item["criterion_text"]
        rubric = new_item["rubric"]
        cid = new_item["criterion_id"]
        category = new_item["category_name"]
        # declare an empty checklist item
        if not cid in bench_checklist:
            bench_checklist[cid] = dict(category_name=category,
                                        question=question,
                                        response="",
                                        justification="",
                                        score=0,
                                        skipped=True,
                                        )
        if not opt_out:
            available_choices = ["yes", "no", 'q', '']
            available_choices+= ['na'] if rubric['na'] else []

            if bench_checklist[cid]['skipped']:
                choice = click.prompt(f"{question}?\nEnter to skip. q to end this session...",
                                  type=click.Choice(available_choices , case_sensitive=False),
                                  show_choices=True, default='')
            elif review:
                previous = f'reviewing {question}:\nResponse: {bench_checklist[cid]['response']}\nJustification: '\
                    f'{bench_checklist[cid]['justification']}\nScore: {bench_checklist[cid]['score']}'
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
                    bench_checklist[cid]['skipped'] = False
                    bench_checklist[cid]['response'] = choice
                    bench_checklist[cid]['justification'] = rubric[0]
                    bench_checklist[cid]['score'] = 0
                case 'na':
                    bench_checklist[cid]['skipped'] = False
                    bench_checklist[cid]['response'] = choice
                    bench_checklist[cid]['justification'] = rubric['na']
                    bench_checklist[cid]['score'] = None
                case 'yes':
                    if not rubric['na']: rubric.pop('na') # n/a criterion
                    rubric_text = "\n ".join([f"{i}- {crit}" for i,crit in rubric.items()])
                    score = click.prompt(f"Please enter score based on the rubric:\n {rubric_text}",
                                           type=click.IntRange(0,15,True), show_choices=True, default=5)
                    rubric_idx = 0 if score == 0 else ((score-1)//5+1)*5
                    # TODO: pick justification closer to score
                    justification = click.edit(f"Justification: {rubric[rubric_idx]}")
                    justification = justification.split('Justification: ', 1)[1].strip() if not justification==None else rubric[rubric_idx]
                    bench_checklist[cid]['skipped'] = False
                    bench_checklist[cid]['response'] = choice if score > 0 else 'no'
                    bench_checklist[cid]['justification'] = justification
                    bench_checklist[cid]['score'] = score
            
    # Save current checklist into the benchmark repo
    with open(checklist_path, 'w') as f:
        yaml.dump(bench_checklist, f)


def score_checklist(bench_checklist: dict) -> (int,int):
    '''
    Score betterbench checklist. 

    Attributes
    ----------
    bench_checklist: dict
        A dictionary of betterbench questions and values as established by better_session function
    '''

    score = 0
    total = 0
    for _ , vals in bench_checklist.items():
        if not vals['response']=='na':
            total += 15
            if not vals['skipped']:
                score += vals['score']

    return (score,total)
        

def get_score(bench_path):
    '''
    Score benchmark using the betterbench checklist. 
    This function is meant to be run using the CLI.

    Attributes
    ----------
    bench_path: str
        Path to where the benchmark folder and all its content reside
    '''

    # Confirm the benchmark exists
    if not os.path.exists(bench_path):
        click.echo("No benchmark reposiory at " + bench_path)
        return

    # Load existing BetterBench checklist if applicable 
    checklist_path = os.path.join(bench_path, "betterbench.yml")
    bench_checklist={}
    if os.path.exists(checklist_path):
        with open(checklist_path, 'r') as f:
           bench_checklist = yaml.safe_load(f)
    if bench_checklist:
        score, total = score_checklist(bench_checklist)
    else:
        click.confirm("BetterBench checklist file empty or not initialized.\n"\
                        f"Would you like to initialize one for the benchmark in {bench_path}?",
                        default=True, abort=True)
        better_session(bench_path) # TODO: Change this to new betterbench function
        with open(checklist_path, 'r') as f:
           bench_checklist = yaml.safe_load(f)
        score, total = score_checklist(bench_checklist)
    
    click.echo(f"Your benchmark's score: {score}/{total}")

