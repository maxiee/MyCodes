import os
from smolagents import Tool, OpenAIServerModel, CodeAgent
from dotenv import load_dotenv

load_dotenv()

model_id = "Qwen/Qwen2.5-7B-Instruct"
api_base = os.getenv('siliconflow_api_base')
api_key = os.getenv('siliconflow_key')

class HFModelDownloadsTool(Tool):
    name = "model_download_counter"
    description = """
    这是一个工具，传入指定任务，返回最多下载次数的模型的ID。
    返回 checkpoint 的名称。"""
    inputs = {
        "task": {
            "type": "string",
            "description": "任务分类（例如 text-classification, depth-estimation)"
        }
    }
    output_type = "string"

    def forward(self, task:str):
        from huggingface_hub import list_models
        model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
        return model.id


model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(tools=[HFModelDownloadsTool()], model=model)

agent.run('下载最多的coder模型是什么？')