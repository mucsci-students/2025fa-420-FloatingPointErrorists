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

def test_add_faculty(json_config: JsonConfig, client: LangchainClient) -> None:
    response = client.send_query("Jarvis, add a faculty named Dr. Test with maximum credits 9 and minimum credits 3, unique course limit 2, available times on MON from 09:00 to 15:00.")
    faculty_added = json_config.scheduler_config.faculty[
        len(json_config.scheduler_config.faculty) - 1
    ]
    assert response == "\nFaculty member Dr. Test added successfully."
    assert faculty_added.name == "Dr. Test"
    assert faculty_added.maximum_credits == 9
    assert faculty_added.minimum_credits == 3
    assert faculty_added.unique_course_limit == 2
    assert faculty_added.times == {"MON": [TimeRange(start='09:00', end='15:00')], "TUE": [], "WED": [], "THU": [], "FRI": []}

def test_langchain_client_initialization(json_config: JsonConfig) -> None:
    langchain_client = LangchainClient(json_config, "test_key")
    assert os.environ["OPENAI_API_KEY"] == "test_key"