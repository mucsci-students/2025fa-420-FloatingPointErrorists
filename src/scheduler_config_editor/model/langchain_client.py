import functools
import os
from typing import Optional

from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from scheduler_config_editor.model import JsonConfig, Faculty


class AddFacultyArgs(BaseModel):
    name: str
    maximum_credits: int
    minimum_credits: int
    unique_course_limit: int
    times: dict[str, list[str]]
    course_preferences: Optional[dict[str, int]] = None
    room_preferences: Optional[dict[str, int]] = None
    lab_preferences: Optional[dict[str, int]] = None

class DelFacultyArgs(BaseModel):
    name: str

def get_tool_list(json_config: JsonConfig) -> list[StructuredTool]:
    return [
        StructuredTool.from_function(
            name ="add_faculty",
            func=functools.partial(Faculty.add_faculty, json_config),
            description=("Add a faculty member to the scheduler configuration. "
                        "Required fields: name, maximum_credits, minimum_credits, unique_course_limit, times. "
                        "The 'times' field must be a dictionary mapping 3-letter day codes to lists of time ranges. "
                        "Example:\n"
                        "{\"MON\": [\"09:00-17:00\"], \"WED\": [\"10:00-12:00\"]}"),
            return_direct=True,
            args_schema=AddFacultyArgs
        ),
        StructuredTool.from_function(
            name="del_faculty",
            func=functools.partial(Faculty.del_faculty, json_config),
            description="Delete a faculty member from the scheduler config.",
            return_direct=True,
            args_schema=DelFacultyArgs
        )
    ]

class LangchainClient:
    def __init__(self, json_config: JsonConfig, api_key: str = None) -> None:
        """Initializes the LangchainClient with a React agent for modifying the configuration file."""
        load_dotenv()
        if not os.environ.get("OPENAI_API_KEY"):
            if api_key is None:
                raise ValueError("API key must be provided if OPENAI_API_KEY is not set in the environment.")
            os.environ["OPENAI_API_KEY"] = api_key
        model = init_chat_model("gpt-5-mini", model_provider="openai")
        tool_list = get_tool_list(json_config)
        initial_prompt = """
            Your name is Jarvis and you will help users modify a configuration file. Using the list of tools you will be 
            able to add, modify, and delete faculty, rooms, labs, and courses from the configuration file.
        """
        self.__client = create_react_agent(model, tool_list, prompt=initial_prompt)

    def send_query(self, query: str) -> str:
        """Sends a query to the Langchain React agent and returns the response."""
        result = self.__client.invoke({"messages": [HumanMessage(content=query)]})
        messages = [ m.content for m in result["messages"][1:] ]
        return "\n".join(messages)
