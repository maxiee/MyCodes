import os
from smolagents import OpenAIServerModel, CodeAgent, PythonInterpreterTool
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv("tencent_model_deepseek_v3")  # "Qwen/Qwen2.5-7B-Instruct"
api_base = os.getenv("tencent_apibase")
api_key = os.getenv("tencent_key")


model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(tools=[PythonInterpreterTool()], model=model)

agent.run("write a simple lisp interpreter and execute a hello world lisp demo. The demo must print 'Hello, World!'")
