import os
import pytest
from scheduler_cli import Course, JsonConfig

@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "base.json"))

def test_add_course(json_config: JsonConfig) -> None:
    Course.add_course(json_config, "TEST COURSE", 3, [], [], [], [])
    assert len(json_config.scheduler_config.courses) == 1
    assert json_config.scheduler_config.courses[0].course_id == "TEST COURSE"
    assert json_config.scheduler_config.courses[0].credits == 3

def test_del_course(json_config: JsonConfig) -> None:
    test_add_course(json_config)
    Course.del_course(0, json_config)
    assert len(json_config.scheduler_config.courses) == 0

def test_mod_course(json_config: JsonConfig) -> None:
    test_add_course(json_config)
    Course.mod_course(0, json_config, "MODIFIED COURSE", 4, [], [], [], [])
    assert json_config.scheduler_config.courses[0].course_id == "MODIFIED COURSE"
    assert json_config.scheduler_config.courses[0].credits == 4