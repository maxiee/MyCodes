import os
from smolagents import Tool, OpenAIServerModel, CodeAgent
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv("siliconflow_model_Qwen2.5-Coder-7B-Instruct") #"Qwen/Qwen2.5-7B-Instruct"
api_base = os.getenv('siliconflow_api_base')
api_key = os.getenv('siliconflow_key')

class HFModelDownloadsTool(Tool):
    name = "model_download_counter"
    description = """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint."""
    inputs = {
        "task": {
            "type": "string",
            "description": "the task category (such as text-classification, depth-estimation, etc)",
        }
    }
    output_type = "string"

    def forward(self, task:str):
        from huggingface_hub import list_models
        model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
        return model.id


model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(tools=[HFModelDownloadsTool()], model=model)

agent.run('whaht is the most download model for chat?')