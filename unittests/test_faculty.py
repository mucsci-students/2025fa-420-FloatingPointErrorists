import os
import json
import pytest
from scheduler import TimeRange
from scheduler_cli.faculty import Faculty
from scheduler_cli.json import JsonConfig

@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))

class TestFaculty:

    def test_add_faculty(self, json_config: JsonConfig):
        Faculty.add_faculty(
            json_config = json_config,
            name = "Dr. Test",
            maximum_credits = 9,
            minimum_credits = 3,
            unique_course_limit = 2,
            times = {"MON": ["09:00-15:00"]},
            course_preferences = {"CMSC 162": 5},
            room_preferences = {"Roddy 136": 3},
            lab_preferences = {"Mac Lab": 7}
        )
        faculty_added = json_config.scheduler_config.faculty[len(json_config.scheduler_config.faculty) - 1]
        assert faculty_added.name == "Dr. Test"
        assert faculty_added.maximum_credits == 9
        assert faculty_added.times == {'MON': [TimeRange(start="09:00", end="15:00")]}
        assert faculty_added.course_preferences == {"CMSC 162": 5}

    def test_mod_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.mod_faculty(
            json_config = json_config,
            old_name = "Dr. Test",
            new_name = "Dr. Test Mod",
            maximum_credits=7,
            minimum_credits=3,
            unique_course_limit=2,
            times={"MON": ["09:00-15:00"]},
            course_preferences={"CMSC 162": 5},
            room_preferences={"Roddy 140": 3},
            lab_preferences={"Mac Lab": 7}
        )
        faculty_mod = json_config.scheduler_config.faculty[len(json_config.scheduler_config.faculty) - 1]
        assert faculty_mod.name == "Dr. Test Mod"
        assert faculty_mod.maximum_credits == 7
        assert faculty_mod.room_preferences == {"Roddy 140": 3}

    def test_del_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.del_faculty(
            json_config = json_config,
            name = "Dr. Test"
        )
        for i, faculty in enumerate(json_config.scheduler_config.faculty):
            assert json_config.scheduler_config.faculty[i].name != "Dr. Test"
