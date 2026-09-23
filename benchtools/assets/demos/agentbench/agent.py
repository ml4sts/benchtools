

from smolagents import InferenceClientModel, CodeAgent


class SmolAgent():

    def __init__():

        # Using a specific model from Hugging Face
        model = InferenceClientModel(
                        model_id="meta-llama/Llama-2-70b-chat-hf",
                        temperature=temp,
                        max_tokens=max_tokens
                        )


        agent = CodeAgent(
            add_base_tools=True, #DuckDuckGo web search, Python code interpreter, Transcriber
            model=model,
        )

    def run(prompt):

        # Now the agent can search the web!
        result = agent.run(prompt)
        return(result)