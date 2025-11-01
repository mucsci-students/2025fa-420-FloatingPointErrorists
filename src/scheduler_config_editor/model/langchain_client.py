import functools
import os
from typing import Optional
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from scheduler_config_editor.model import JsonConfig, Faculty, Course, Room, Lab


# ----- Show Config Function ----- #
def make_show(json_config):
    def show() -> str:
        """Show the current scheduler configuration in a pretty-printed format."""
        return str(json_config)

    return show


# ------ Wrappers & Argument Schemas for Faculty functions ----- #


def add_faculty(
    json_config: JsonConfig,
    name: str,
    maximum_credits: int,
    minimum_credits: int,
    unique_course_limit: int,
    times: dict[str, list[str]],
    course_preferences: Optional[dict[str, int]] = None,
    room_preferences: Optional[dict[str, int]] = None,
    lab_preferences: Optional[dict[str, int]] = None,
) -> str:
    try:
        return Faculty.add_faculty(
            json_config,
            name,
            maximum_credits,
            minimum_credits,
            unique_course_limit,
            times,
            course_preferences,
            room_preferences,
            lab_preferences,
        )
    except ValueError as e:
        return str(e)


def mod_faculty(
    json_config: JsonConfig,
    old_name: str,
    new_name: Optional[str] = None,
    maximum_credits: Optional[int] = None,
    minimum_credits: Optional[int] = None,
    unique_course_limit: Optional[int] = None,
    times: Optional[dict[str, list[str]]] = None,
    course_preferences: Optional[dict[str, int]] = None,
    room_preferences: Optional[dict[str, int]] = None,
    lab_preferences: Optional[dict[str, int]] = None,
) -> str:
    try:
        return Faculty.mod_faculty(
            json_config,
            old_name,
            new_name,
            maximum_credits,
            minimum_credits,
            unique_course_limit,
            times,
            course_preferences,
            room_preferences,
            lab_preferences,
        )
    except ValueError as e:
        return str(e)


class AddFacultyArgs(BaseModel):
    name: str
    maximum_credits: int
    minimum_credits: int
    unique_course_limit: int
    times: dict[str, list[str]]
    course_preferences: Optional[dict[str, int]] = None
    room_preferences: Optional[dict[str, int]] = None
    lab_preferences: Optional[dict[str, int]] = None


class ModFacultyArgs(BaseModel):
    old_name: str
    new_name: Optional[str] = None
    maximum_credits: Optional[int] = None
    minimum_credits: Optional[int] = None
    unique_course_limit: Optional[int] = None
    times: Optional[dict[str, list[str]]] = None
    course_preferences: Optional[dict[str, int]] = None
    room_preferences: Optional[dict[str, int]] = None
    lab_preferences: Optional[dict[str, int]] = None


class DelFacultyArgs(BaseModel):
    name: str


# ----- Wrappers & Argument Schema for Course functions ----- #


def del_course(json_config: JsonConfig, index: int) -> str:
    try:
        return Course.del_course(index, json_config)
    except IndexError as e:
        return str(e)


def add_course(
    json_config: JsonConfig,
    course_id: str,
    course_credits: int,
    room: list[str],
    faculty: list[str],
    lab: Optional[list[str]] = None,
    conflicts: Optional[list[str]] = None,
) -> str:
    try:
        return Course.add_course(
            json_config,
            course_id,
            course_credits,
            room,
            faculty,
            lab,
            conflicts,
        )
    except ValueError as e:
        return str(e)


def mod_course(
    index: int,
    json_config: JsonConfig,
    course_id: Optional[str] = None,
    course_credits: Optional[int] = None,
    room: Optional[list[str]] = None,
    lab: Optional[list[str]] = None,
    conflicts: Optional[list[str]] = None,
    faculty: Optional[list[str]] = None,
) -> str:
    try:
        return Course.mod_course(
            index,
            json_config,
            course_id,
            course_credits,
            room,
            lab,
            conflicts,
            faculty,
        )
    except (IndexError, ValueError) as e:
        return str(e)


class ListCoursesArgs(BaseModel):
    pass


class DelCourseArgs(BaseModel):
    index: int


class AddCourseArgs(BaseModel):
    course_id: str
    course_credits: int
    room: list[str]
    faculty: list[str]
    lab: Optional[list[str]] = None
    conflicts: Optional[list[str]] = None


class ModCourseArgs(BaseModel):
    index: int
    course_id: Optional[str] = None
    course_credits: Optional[int] = None
    room: Optional[list[str]] = None
    lab: Optional[list[str]] = None
    conflicts: Optional[list[str]] = None
    faculty: Optional[list[str]] = None


# ----- Wrappers & Argument Schema for Room & Lab functions ----- #


def add_room(json_config: JsonConfig, new_room: str) -> str:
    try:
        return Room.add_room(json_config, new_room)
    except Room.RoomExistsError as e:
        return str(e)


def mod_room(json_config: JsonConfig, room: str, new_room: str) -> str:
    try:
        return Room.mod_room(json_config, room, new_room)
    except (Room.RoomExistsError, Room.RoomMissingError) as e:
        return str(e)


def del_room(json_config: JsonConfig, room: str) -> str:
    try:
        return Room.del_room(json_config, room)
    except Room.RoomMissingError as e:
        return str(e)


def add_lab(json_config: JsonConfig, new_lab: str) -> str:
    try:
        return Lab.add_lab(json_config, new_lab)
    except Lab.LabExistsError as e:
        return str(e)


def mod_lab(json_config: JsonConfig, lab: str, new_lab: str) -> str:
    try:
        return Lab.mod_lab(json_config, lab, new_lab)
    except (Lab.LabExistsError, Lab.LabMissingError) as e:
        return str(e)


def del_lab(json_config: JsonConfig, lab: str) -> str:
    try:
        return Lab.del_lab(json_config, lab)
    except Lab.LabMissingError as e:
        return str(e)


class AddRoomArgs(BaseModel):
    new_room: str


class ModRoomArgs(BaseModel):
    room: str
    new_room: str


class DelRoomArgs(BaseModel):
    room: str


class AddLabArgs(BaseModel):
    new_lab: str


class ModLabArgs(BaseModel):
    lab: str
    new_lab: str


class DelLabArgs(BaseModel):
    lab: str


# ----- Tool List Definition ----- #


def get_tool_list(json_config: JsonConfig) -> list[StructuredTool]:
    return [
        StructuredTool.from_function(
            name="add_faculty",
            func=functools.partial(add_faculty, json_config),
            description=(
                "Add a faculty member to the scheduler configuration. "
                "Required fields: name, maximum_credits, minimum_credits, unique_course_limit, times. "
                "The 'times' field must be a dictionary mapping 3-letter day codes to lists of time ranges. "
                'All week days must be included even if the faculty is not available that day. ex: "FRI": []'
                "Example:\n"
                '{"MON": ["09:00-17:00"],"TUE": [], "WED": ["10:00-12:00"]. "THU": [], "FRI": []}'
                "All preferences should be valid dictionaries in the form of {str: int}."
            ),
            return_direct=True,
            args_schema=AddFacultyArgs,
        ),
        StructuredTool.from_function(
            name="mod_faculty",
            func=functools.partial(mod_faculty, json_config),
            description=(
                "Modify a faculty member in the scheduler configuration. "
                "Required fields: old_name, new_name, maximum_credits, minimum_credits, unique_course_limit, times. "
                "The 'times' field must be a dictionary mapping 3-letter day codes to lists of time ranges. "
                'All week days must be included even if the faculty is not available that day. ex: "FRI": []'
                "Example:\n"
                '{"MON": ["09:00-17:00"],"TUE": [], "WED": ["10:00-12:00"]. "THU": [], "FRI": []}'
                "All preferences should be valid dictionaries in the form of {str: int}."
            ),
            return_direct=True,
            args_schema=ModFacultyArgs,
        ),
        StructuredTool.from_function(
            name="del_faculty",
            func=functools.partial(Faculty.del_faculty, json_config),
            description="Delete a faculty member from the scheduler config.",
            return_direct=True,
            args_schema=DelFacultyArgs,
        ),
        StructuredTool.from_function(
            name="courses_string",
            func=functools.partial(Course.courses_string, json_config),
            description="List all courses in the scheduler configuration.",
            return_direct=True,
            args_schema=ListCoursesArgs,
        ),
        StructuredTool.from_function(
            name="del_course",
            func=functools.partial(del_course, json_config=json_config),
            description="Delete a course from the scheduler configuration by its index.",
            return_direct=True,
            args_schema=DelCourseArgs,
        ),
        StructuredTool.from_function(
            name="add_course",
            func=functools.partial(add_course, json_config=json_config),
            description="Add a course to the scheduler configuration.",
            return_direct=True,
            args_schema=AddCourseArgs,
        ),
        StructuredTool.from_function(
            name="mod_course",
            func=functools.partial(mod_course, json_config=json_config),
            description=(
                "Modify a course in the scheduler configuration."
                "if you are told to remove all items from a list field, pass an empty list for that field."
            ),
            return_direct=True,
            args_schema=ModCourseArgs,
        ),
        StructuredTool.from_function(
            name="add_room",
            func=functools.partial(add_room, json_config=json_config),
            description="Add a room to the scheduler configuration.",
            return_direct=True,
            args_schema=AddRoomArgs,
        ),
        StructuredTool.from_function(
            name="mod_room",
            func=functools.partial(mod_room, json_config=json_config),
            description="Modify a room in the scheduler configuration.",
            return_direct=True,
            args_schema=ModRoomArgs,
        ),
        StructuredTool.from_function(
            name="del_room",
            func=functools.partial(del_room, json_config=json_config),
            description="Delete a room from the scheduler configuration.",
            return_direct=True,
            args_schema=DelRoomArgs,
        ),
        StructuredTool.from_function(
            name="add_lab",
            func=functools.partial(add_lab, json_config=json_config),
            description="Add a lab to the scheduler configuration.",
            return_direct=True,
            args_schema=AddLabArgs,
        ),
        StructuredTool.from_function(
            name="mod_lab",
            func=functools.partial(mod_lab, json_config=json_config),
            description="Modify a lab in the scheduler configuration.",
            return_direct=True,
            args_schema=ModLabArgs,
        ),
        StructuredTool.from_function(
            name="del_lab",
            func=functools.partial(del_lab, json_config=json_config),
            description="Delete a lab from the scheduler configuration.",
            return_direct=True,
            args_schema=DelLabArgs,
        ),
        StructuredTool.from_function(
            name="show",
            func=make_show(json_config),
            description="Show the current scheduler configuration in a pretty-printed format.",
            return_direct=True,
        ),
    ]


class LangchainClient:
    """
    A client that uses Langchain's React agent to modify a scheduler configuration file.

    Attributes:
        __client: The Langchain React agent client.
    """

    def __init__(self, json_config: JsonConfig, api_key: str = "") -> None:
        """Initializes the LangchainClient with a React agent for modifying the configuration file."""
        load_dotenv()
        if not os.environ.get("OPENAI_API_KEY"):
            if api_key is None:
                raise ValueError(
                    "API key must be provided if OPENAI_API_KEY is not set in the environment."
                )
            os.environ["OPENAI_API_KEY"] = api_key
        model = init_chat_model("gpt-5-mini", model_provider="openai")
        tool_list = get_tool_list(json_config)
        initial_prompt = """
            Your name is Jarvis and you will only help users modify a configuration file if they call you by your name.
            Using the list of tools you will be able to add, modify, and delete faculty, rooms, labs, and courses from the configuration file.
        """
        self.__client = create_react_agent(model, tool_list, prompt=initial_prompt)

    def send_query(self, query: str) -> str:
        """Sends a query to the Langchain React agent and returns the response."""
        result = self.__client.invoke({"messages": [HumanMessage(content=query)]})
        messages = [m.content for m in result["messages"][1:]]
        return "\n".join(messages)
