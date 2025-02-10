from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, launch_gradio_demo
import os
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv('model_id')
api_base = os.getenv('api_base')
api_key = os.getenv('api_key')

# model = HfApiModel(model_id=model_id, api_base=api_base, api_key=api_key)
# agent = CodeAgent(tools=[], model=model)


launch_gradio_demo(DuckDuckGoSearchTool())