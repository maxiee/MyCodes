import os
from smolagents import OpenAIServerModel, CodeAgent, PythonInterpreterTool, Tool
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv("tencent_model_deepseek_v3")  # "Qwen/Qwen2.5-7B-Instruct"
api_base = os.getenv("tencent_apibase")
api_key = os.getenv("tencent_key")

model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(
    tools=[
        Tool.from_space(
            space_id="black-forest-labs/FLUX.1-schnell",
            name="image_generator",
            description="Generate an image from a prompt",
        )
    ],
    model=model,
)

agent.run("Create a image of 'a cat coding using a retro computer'. First improve the prompt, and then Generate an image from the prompt")
