import os
import yaml
import click
from .utils import load_asset_yml
# from click_prompt import choice_option

class CheckListItem():

    def __init__(self, category: str, question: str, cid: str, rubric: dict, response: str, justification: str, skipped: bool, score: int):
        self.category=category
        self.question=question
        self.cid=cid
        self.rubric=rubric
        self.response=response
        self.justification=justification
        self.skipped=skipped
        self.score=score
    


class BetterCheckList():
    '''
    The checklist below is based on the benchmark quality assessment proposed in
    BetterBench. It is supposed to help authors identify if they adhere to best 
    practices in their benchmark development. If you want to have your benchmark
    added to the BetterBench Repository, please also fill out the justifications.
    These should be about one sentence long each, and include the page numbers of
    your paper or your webpage where the information can be found. You can also
    copy-paste quotes from any of your publicly available materials here as
    evidence. In this case, please also add a link to the source. Reuel et. al.

    To understand methodology and justification of questions please view 
    [BetterBench Methodology](https://betterbench.stanford.edu/methodology.html)
        
    Attributes
    ----------
        checklist: list[CheckListItem]

    Methods
    -------
            Create a new checklist using the BetterBench template
        from_template()
            Load a betterbench checklist from a yaml file
        from_file(checklist_path: str)
            Initiate an interactive session to fill out the checklist
        interactive_session()
            Add a CheckListItem to the checklist
        add_item(item)
            score checklist object
        score_checklist()
            print betterbench scores
        print_score()

    '''

    def __init__(self, items: list[CheckListItem]):
        self.items: list[CheckListItem] = items
        self.ids = [item.cid for item in self.items]
        self.categories = list({item.category for item in self.items})
        # self.total_score = 15 * len(self.items)

    @classmethod
    def from_template(cls):
        main_checklist = load_asset_yml("betterbench.yml")
        bench_checklist=[]
        # Loop until user opts out 
        for item in main_checklist: 
            bench_checklist.append(CheckListItem(category=item["category_name"],
                                                question=item["criterion_text"],
                                                cid=item["criterion_id"],
                                                rubric=item["rubric"],
                                                response="",
                                                justification="",
                                                score=0,
                                                skipped=True,
                                                ))

        return cls(bench_checklist)


    @classmethod
    def from_file(cls, checklist_path: str):
        bench_checklist = []
        # Confirm the benchmark exists
        if not checklist_path.endswith('.yml') or not os.path.exists(checklist_path):
            click.echo("Incorrect betterbench checklist path: " + checklist_path)
            exit()

        # Load existing BetterBench checklist if applicable 
        bench_checklist=[]
        with open(checklist_path, 'r') as f:
           checklist_dict = yaml.safe_load(f)
           if checklist_dict: bench_checklist = checklist_dict
           else: click.echo("WARNING: The provided checklist path was empty or failed to load. Returning empty list.")

        if bench_checklist: better_checklist = [CheckListItem(**item) for item in bench_checklist]
        return cls(better_checklist)

    def add_item(self, item: CheckListItem):
        self.items.append(item)

    # def interactive_session(self, questions:list = None, file:str = None):
    #     pass


    def interactive_session(self):

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

        # Check if want to change answer on any questions
        review = click.confirm("Would you like to review previous respopnses? ", default=False)

        opt_out = False
        # Loop until user opts out 
        for item in self.items: 

            if not opt_out:
                available_choices = ["yes", "no", 'q', '']
                available_choices+= ['na'] if item.rubric['na'] else []

                if item.skipped:
                    choice = click.prompt(f"{item.question}?\nEnter to skip. q to end this session...",
                                      type=click.Choice(available_choices , case_sensitive=False),
                                      show_choices=True, default='')
                elif review:
                    previous = f'Reviewing {item.question}:\nResponse: {item.response}\n'\
                        f'Justification: {item.justification}\nScore: {item.score}'
                    click.echo(previous)
                    choice = click.prompt(f"{item.question}?\nEnter to skip. q to end this session...",
                                      type=click.Choice(available_choices , case_sensitive=False),
                                      show_choices=True, default='')
                else:
                    continue

                match choice:
                    case 'q':
                        opt_out = True
                        break
                    case '':
                        continue
                    case 'no':
                        item.skipped = False
                        item.response = choice
                        item.justification = item.rubric[0]
                        item.score = 0
                    case 'na':
                        item.skipped = False
                        item.response = choice
                        item.justification = item.rubric['na']
                        item.score = None
                        # self.total_score -=15
                    case 'yes':
                        if not item.rubric['na']: item.rubric.pop('na') # n/a criterion
                        rubric_text = "\n ".join([f"{i}- {crit}" for i,crit in item.rubric.items()])
                        score = click.prompt(f"Please enter score based on the rubric:\n {rubric_text}",
                                               type=click.IntRange(min=0,max=15,clamp=True), show_choices=True, default=5)
                        # Pick justification closer to score
                        rubric_idx = 0 if score == 0 else ((score-1)//5+1)*5
                        justification = click.edit(f"Justification: {item.rubric[rubric_idx]}")
                        justification = justification.split('Justification: ', 1)[1].strip() if not justification==None else item.rubric[rubric_idx]
                        item.skipped = False
                        item.response = choice if score > 0 else 'no'
                        item.justification = justification
                        item.score = score


    def score_checklist(self):
        '''
        Score betterbench checklist. 
        '''
        
        scores = dict(score = 0,
                        total = 0,
                        )
        
        for category in self.categories:
            scores.update({f'{category}_score': 0})
            scores.update({f'{category}_total': 0})
        
        for item in self.items:
            if not item.response =='na':
                scores['total'] += 15
                scores[f'{item.category}_total'] += 15
                if not item.skipped:
                    scores['score'] += item.score
                    scores[f'{item.category}_score'] += item.score

        return (scores)


    def print_score(self):
        scores = self.score_checklist()
        output = f"""
Your benchmark's score: {scores.pop('score')}/{scores.pop('total')}
"""
        for key in scores.keys():
            if "_score" in key:
                category_name = key.split('_',1)[0]
                output += f"\n{category_name}: {scores[f'{category_name}_score']}/{scores[f'{category_name}_total']}"

        click.echo(output)

    def save(self, bench_path: str):
        # Confirm the benchmark exists
        if not os.path.exists(bench_path):
            click.echo("No benchmark reposiory at " + bench_path)

        # Load existing BetterBench checklist if applicable 
        checklist_path = os.path.join(bench_path, "betterbench.yml")
        # Convert objects to a list of dicts before saving
        bench_checklist = [item.__dict__ for item in self.items]
        # Save current checklist into the benchmark repo
        with open(checklist_path, 'w') as f:
            yaml.dump(bench_checklist, f)

