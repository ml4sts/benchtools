'''
Basic agent class used to define what an Agent's inputs and outputs 
should look like to benchmark them using BenchTools
'''

from typing import Protocol, Any
from dataclasses import dataclass

@dataclass
class Step:
    """One unit of agent activity, for trajectory-level eval."""
    type: str  # "thought" | "tool_call" | "tool_result" | "final_answer"
    content: str
    tool_name: str | None = None

@dataclass
class AgentResult:
    final_answer: str
    success: bool
    steps: list[Step]
    metadata: dict
    error: str | None = None
    raw: Any = None          # untouched framework-native output, for debugging


class Agent(Protocol):
    """ Base class for agents """

    def __init__(self, **kwargs):        
        self.args = kwargs
        self.agent_type = "Basic"
        self.agent_tools = ["reading", "doing math"]

    def run(self, prompt, **kwargs):
        """ Run the agent on the environment. """
        # A simple baseline that always executes train.py and reports final answer
        final_answer = "This is a basic example agent final answer",
        response = AgentResult(
            final_answer = final_answer,
            success = True,
            steps = [prompt, "Let's begin", final_answer],
            metadata = {"Tokens": 500}
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
            result = self.agent.run(task)
            steps = [
                Step(type="tool_call", content=str(m), tool_name=getattr(m, "tool_name", None))
                for m in getattr(self._agent, "memory", {}).get("steps", [])
            ]
            return AgentResult(final_answer=str(result), success=True, steps=steps, raw=result)
        except Exception as e:
            return AgentResult(final_answer="", success=False, error=str(e))



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