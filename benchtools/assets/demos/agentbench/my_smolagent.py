'''
Simple SmolAgent agent module used for basic search purposes.
This module is not equipped to be tested by BenchTools as is.
'''
from smolagents import InferenceClientModel, CodeAgent, DuckDuckGoSearchTool
# Using a specific model from Hugging Face
model = InferenceClientModel()
my_smol_agent = CodeAgent(
    model=model,
    tools=[DuckDuckGoSearchTool()],
)