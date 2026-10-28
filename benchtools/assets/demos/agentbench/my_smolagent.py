'''
Simple SmolAgent agent module used for basic search purposes.
This module is not equipped to be tested by BenchTools as is.
'''
from smolagents import CodeAgent, DuckDuckGoSearchTool

from smolagents import LiteLLMModel
model = LiteLLMModel(
    model_id="ollama_chat/llama3.2-vision:latest",
    api_base="http://localhost:11434",
    num_ctx=8192,
    )

my_smol_agent = CodeAgent(
    model=model,
    tools=[DuckDuckGoSearchTool()],
    max_steps=3
)