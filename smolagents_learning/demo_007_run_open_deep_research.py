import threading
from tkinter.messagebox import QUESTION
from dotenv import load_dotenv
from huggingface_hub import login
import os
from open_deep_research.scripts.text_inspector_tool import TextInspectorTool
from smolagents import OpenAIServerModel, CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool

from open_deep_research.scripts.text_web_browser import ArchiveSearchTool, FindNextTool, FinderTool, PageDownTool, PageUpTool, SimpleTextBrowser, VisitTool

question = "I want to know about more about the bootloader on Android devices."

AUTHORIZED_IMPORTS = [
    "requests",
    "zipfile",
    "os",
    "pandas",
    "numpy",
    "sympy",
    "json",
    "bs4",
    "pubchempy",
    "xml",
    "yahoo_finance",
    "Bio",
    "sklearn",
    "scipy",
    "pydub",
    "io",
    "PIL",
    "chess",
    "PyPDF2",
    "pptx",
    "torch",
    "datetime",
    "fractions",
    "csv",
]

load_dotenv(override=True)
login(os.getenv("HF_TOKEN"))

append_answer_lock = threading.Lock()

model_id = f'{os.getenv(
    "siliconflow_model_Qwen2.5-Coder-7B-Instruct"
)}'  # "Qwen/Qwen2.5-7B-Instruct"

api_base = os.getenv("siliconflow_api_base")
api_key = os.getenv("siliconflow_key")

custom_role_conversions = {"tool-call": "assistant", "tool-response": "user"}

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"

BROWSER_CONFIG = {
    "viewport_size": 1024 * 5,
    "downloads_folder": "downloads_folder",
    "request_kwargs": {
        "headers": {"User-Agent": user_agent},
        "timeout": 300,
    },
    "serpapi_key": os.getenv("SERPAPI_API_KEY"),
}

os.makedirs(f"./{BROWSER_CONFIG['downloads_folder']}", exist_ok=True)


def main():
    text_limit = 100000

    model = OpenAIServerModel(model_id=model_id, api_base=api_base, api_key=api_key)
    document_inspection_tool = TextInspectorTool(model, text_limit)
    browser = SimpleTextBrowser(**BROWSER_CONFIG)

    WEB_TOOLS = [
        # SearchInformationTool(browser),
        DuckDuckGoSearchTool(),
        VisitTool(browser),
        PageUpTool(browser),
        PageDownTool(browser),
        FinderTool(browser),
        FindNextTool(browser),
        ArchiveSearchTool(browser),
        TextInspectorTool(model, text_limit),
    ]

    text_webbrowser_agent = ToolCallingAgent(
        model=model,
        tools=WEB_TOOLS,
        max_steps=20,
        verbosity_level=2,
        planning_interval=4,
        name="search_agent",
        description="""A team member that will search the internet to answer your question.
    Ask him for all your questions that require browsing the web.
    Provide him as much context as possible, in particular if you need to search on a specific timeframe!
    And don't hesitate to provide him with a complex search task, like finding a difference between two webpages.
    Your request must be a real sentence, not a google search! Like "Find me this information (...)" rather than a few keywords.
    """,
        provide_run_summary=True,
    )
    text_webbrowser_agent.prompt_templates["managed_agent"]["task"] += """You can navigate to .txt online files.
    If a non-html page is in another format, especially .pdf or a Youtube video, use tool 'inspect_file_as_text' to inspect it.
    Additionally, if after some searching you find out that you need more information to answer the question, you can use `final_answer` with your request for clarification as argument to request for more information."""

    manager_agent = CodeAgent(
        model=model,
        tools=[document_inspection_tool],
        max_steps=12,
        verbosity_level=2,
        additional_authorized_imports=AUTHORIZED_IMPORTS,
        planning_interval=4,
        managed_agents=[text_webbrowser_agent],
    )

    answer = manager_agent.run(question)

    print(f"Got this answer: {answer}")

if __name__ == "__main__":
    main()