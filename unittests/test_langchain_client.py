import os

import pytest

from scheduler_config_editor.model import LangchainClient, JsonConfig, Room, Lab, Faculty, Course

"""
    Tests for the module src/scheduler_config_editor/model/langchain_client.py
"""


@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))


@pytest.fixture()
def client(json_config: JsonConfig):
    yield LangchainClient(json_config)

def test_add_room(json_config: JsonConfig, client: LangchainClient) -> None:
    client.send_query(
        "Jarvis, add a room with the name: Test Room"
    )
    assert json_config.scheduler_config.rooms.count("Test Room") == 1

def test_add_room_dupe(json_config: JsonConfig, client: LangchainClient) -> None:
    Room.add_room(json_config, "Test Room")
    response = client.send_query(
        "Jarvis, add a room with the name: Test Room"
    )
    assert json_config.scheduler_config.rooms.count("Test Room") == 1
    assert response.endswith("already exists.")

def test_mod_room(json_config: JsonConfig, client: LangchainClient) -> None:
    Room.add_room(json_config, "Test Room")
    client.send_query(
        "Jarvis, change the room with the name Test Room, to the new name: New Room"
    )
    assert json_config.scheduler_config.rooms.count("New Room") == 1

def test_mod_room_ne(json_config: JsonConfig, client: LangchainClient) -> None:
    response = client.send_query(
        "Jarvis, change the room with the name Test Room, to the new name: New Room"
    )
    assert json_config.scheduler_config.rooms.count("Test Room") == 0
    assert json_config.scheduler_config.rooms.count("New Room") == 0
    assert response.endswith("does not exist.")

def test_del_room(json_config: JsonConfig, client: LangchainClient) -> None:
    Room.add_room(json_config, "Test Room")
    client.send_query(
        "Jarvis, remove the room with the name: Test Room"
    )
    assert json_config.scheduler_config.rooms.count("Test Room") == 0

def test_del_room_ne(json_config: JsonConfig, client: LangchainClient) -> None:
    response = client.send_query(
        "Jarvis, remove the room with the name: Test Room"
    )
    assert response.endswith("does not exist.")

def test_add_lab(json_config: JsonConfig, client: LangchainClient) -> None:
    client.send_query(
        "Jarvis, add a lab with the name: Research Lab"
    )
    assert json_config.scheduler_config.labs.count("Research Lab") == 1

def test_add_lab_dupe(json_config: JsonConfig, client: LangchainClient) -> None:
    Lab.add_lab(json_config, "Research Lab")
    response = client.send_query(
        "Jarvis, add a lab with the name: Research Lab"
    )
    assert json_config.scheduler_config.labs.count("Research Lab") == 1
    assert response.endswith("already exists.")

def test_mod_lab(json_config: JsonConfig, client: LangchainClient) -> None:
    Lab.add_lab(json_config, "Test Lab")
    client.send_query(
        "Jarvis, change the lab with the name Test Lab, to the new name: Research Lab"
    )
    assert json_config.scheduler_config.labs.count("Research Lab") == 1

def test_mod_lab_ne(json_config: JsonConfig, client: LangchainClient) -> None:
    response = client.send_query(
        "Jarvis, change the lab with the name Test Lab, to the new name: Research Lab"
    )
    assert json_config.scheduler_config.labs.count("Test Lab") == 0
    assert json_config.scheduler_config.labs.count("Research Lab") == 0
    assert response.endswith("does not exist.")

def test_del_lab(json_config: JsonConfig, client: LangchainClient) -> None:
    Lab.add_lab(json_config, "Research Lab")
    client.send_query(
        "Jarvis, remove the lab with the name: Research Lab"
    )
    assert json_config.scheduler_config.labs.count("Research Lab") == 0

def test_del_lab_ne(json_config: JsonConfig, client: LangchainClient) -> None:
    response = client.send_query(
        "Jarvis, remove the lab with the name: Research Lab"
    )
    assert response.endswith("does not exist.")

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
    LangchainClient(json_config, "test_key")
    assert os.environ["OPENAI_API_KEY"] == "test_key"
