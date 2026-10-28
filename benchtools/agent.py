'''
Basic agent class used to define what an Agent's inputs and outputs 
should look like to benchmark them using BenchTools
'''

from typing import Protocol, Any
from dataclasses import dataclass, field
from smolagents import ActionStep, TaskStep, PlanningStep

@dataclass
class Step:
    """One unit of agent activity, for trajectory-level eval."""
    type: str
    content: str
    tool_name: str | None = None
    metadata: dict = field(default_factory=dict)

@dataclass
class AgentResult:
    final_answer: str
    success: bool
    steps: list[Step] = field(default_factory=list)
    error: str | None = None
    raw: Any = None                # untouched framework-native output, for debugging
    usage: dict = field(default_factory=dict)


class Agent(Protocol):
    """ Base class for agents """

    def __init__(self, **kwargs):        
        self.args = kwargs
        self.agent_type = "Basic"
        self.agent_tools = ["reading", "doing math"]

    def run(self, prompt, **kwargs):
        """ Run the agent on the environment. """
        # A simple baseline that always executes train.py and reports final answer
        final_answer = "This is a basic example agent final answer"
        response = AgentResult(
            final_answer = final_answer,
            success = True,
            steps=[
                Step(type="task", content=task),
                Step(type="thought", content="Let's begin"),
                Step(type="final_answer", content=final_answer),
            ],
            usage={"total_tokens": 500},
        )
        return(response)

    def __str__(self):
        return(f"This is the {self.agent_type} Agent Class")
    
    def __repr__(self):
        return(f"{self.agent_type} Agent Class")


# class SmolAgentAdapter(Agent):
class SmolagentsAdapter:
    def __init__(self, smol_agent):
        self.agent_type = "smol_agent"
        self.agent = smol_agent  # e.g. a smolagents CodeAgent instance

    def run(self, task: str) -> AgentResult:
        try:
            answer = self.agent.run(task)
        except Exception as e:
            # keep whatever trajectory exists up to the failure
            return AgentResult(final_answer="", success=False,
                               steps=steps_from_memory(self.agent), error=repr(e))
        steps = steps_from_memory(self.agent)
        steps.append(Step(type="final_answer", content=str(answer)))
        return AgentResult(final_answer=str(answer), success=True, steps=steps, raw=answer)
        

def steps_from_memory(agent) -> list[Step]:
    memory = getattr(agent, "memory", None)
    raw_steps = getattr(memory, "steps", []) if memory is not None else []

    steps = []
    for m in raw_steps:
        if isinstance(m, ActionStep):
            tool_calls = getattr(m, "tool_calls", None) or []
            steps.append(Step(
                type="tool_call" if tool_calls else "thought",
                content=getattr(m, "model_output", None) or "",
                tool_name=getattr(tool_calls[0], "name", None) if tool_calls else None,
                metadata={
                    "step_number": getattr(m, "step_number", None),
                    "tool_calls": [
                        {"name": getattr(tc, "name", None), "arguments": getattr(tc, "arguments", None)}
                        for tc in tool_calls
                    ],
                    "observation": getattr(m, "observations", None),
                    "error": str(m.error) if getattr(m, "error", None) else None,
                },
            ))
        elif isinstance(m, TaskStep):
            steps.append(Step(type="task", content=getattr(m, "task", "") or ""))
        elif isinstance(m, PlanningStep):
            steps.append(Step(type="plan", content=getattr(m, "plan", "") or ""))
        else:
            steps.append(Step(type=type(m).__name__.lower(), content=str(m)))
    return steps

class LangGraphAdapter(Agent):

    def __init__(self, graph):
        self.agent_type = "lang_graph"
        self.graph = graph

    def run(self, task, **kwargs):
        return self.graph.invoke(
            {"messages": [{"role": "user", "content": task}]}
        )



class OpenAIAgentAdapter(Agent):

    def __init__(self, agent):
        self.agent_type = "OpenAI_agnet"
        self.agent = agent

    def run(self, task, **kwargs):
        return Runner.run_sync(self.agent, task)