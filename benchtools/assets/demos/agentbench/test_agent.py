'''
Agent module linking my custom smolagent with BenchTools adapter to be benchmark-ready
'''

from my_smolagent import my_smol_agent
from benchtools.agent import SmolagentsAdapter

# Use the builtin adapter to link my custom smolagent to BenchTools agent
agent = SmolagentsAdapter(my_smol_agent)   