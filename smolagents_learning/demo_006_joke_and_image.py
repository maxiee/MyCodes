import os
import requests
from smolagents import OpenAIServerModel, CodeAgent, PythonInterpreterTool, Tool, tool
from dotenv import load_dotenv

load_dotenv()

model_id = os.getenv("siliconflow_model_Qwen2.5-Coder-7B-Instruct")  # "Qwen/Qwen2.5-7B-Instruct"
api_base = os.getenv("siliconflow_api_base")
api_key = os.getenv("siliconflow_key")

@tool
def get_joke() -> str:
    """
    Fetches a random joke from the JokeAPI.
    This function sends a GET request to the JokeAPI to retrieve a random joke.
    It handles both single jokes and two-part jokes (setup and delivery).
    If the request fails or the response does not contain a joke, an error message is returned.
    Returns:
        str: The joke as a string, or an error message if the joke could not be fetched.
    """
    url = "https://v2.jokeapi.dev/joke/Any?type=single"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if "joke" in data:
            return data["joke"]
        elif "setup" in data and "delivery" in data:
            return f"{data['setup']} - {data['delivery']}"
        else:
            return "Error: Unable to fetch joke."

    except requests.exceptions.RequestException as e:
        return f"Error fetching joke: {str(e)}"

model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
agent = CodeAgent(
    tools=[
        get_joke,
        Tool.from_space(
            space_id="black-forest-labs/FLUX.1-schnell",
            name="image_generator",
            description="Generate an image from a prompt",
        )
    ],
    model=model,
)

print('running agent')
agent.run("fetch a joke. improve the fetched joke into an detailed imgae generation prompt, which is a funny crazy meme image. And then generate a image with the generated prompt.")
