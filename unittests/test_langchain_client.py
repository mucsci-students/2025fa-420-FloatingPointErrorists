import os

import pytest
from scheduler import TimeRange

from scheduler_config_editor.model import LangchainClient, JsonConfig

"""
    Tests for the module src/scheduler_config_editor/model/langchain_client.py
"""


@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))


@pytest.fixture()
def client(json_config: JsonConfig):
    yield LangchainClient(json_config)


def test_add_course(json_config: JsonConfig, client: LangchainClient) -> None:
    client.send_query(
        "Jarvis, add a course with id: CMSC 455, credits: 4, room: Roddy 136, faculty: Hogg "
    )
    course = json_config.scheduler_config.courses[-1]
    assert course.course_id == "CMSC 455"
    assert course.faculty[0] == "Hogg"
    assert course.credits == 4
    assert course.room[0] == "Roddy 136"


def test_langchain_client_initialization(json_config: JsonConfig) -> None:
    langchain_client = LangchainClient(json_config, "test_key")
    assert os.environ["OPENAI_API_KEY"] == "test_key"
