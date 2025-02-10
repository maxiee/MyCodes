from smolagents import CodeAgent, DuckDuckGoSearchTool, OpenAIServerModel
import os
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv('siliconflow_model_Qwen2.5-Coder-7B-Instruct')
api_base = os.getenv('siliconflow_api_base')
api_key = os.getenv('siliconflow_key')

model = OpenAIServerModel(model_id="Qwen/Qwen2.5-7B-Instruct", api_base=api_base, api_key=api_key)
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

agent.write_memory_to_messages()
agent.run('How to use LLM for reading source code?')