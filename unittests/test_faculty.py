import json
from calendar import MONDAY
from scheduler_cli.faculty import Faculty
from src.scheduler_cli.json import JsonConfig

class TestFaculty:

    def test_add_faculty(self, json_config: JsonConfig):
        Faculty.add_faculty(
            json_config = json_config,
            name = "Dr. Test",
            maximum_credits = 9,
            minimum_credits = 3,
            unique_course_limit = 2,
            times = {MONDAY: ["9-3"]},
            course_preferences = {"CMSC 162": 5},
            room_preferences = {"Roddy 136": 3},
            lab_preferences = {"Mac Lab": 7}
        )
        faculty_added = json_config.config.faculty[0]
        assert faculty_added.name == "Dr. Test"
        assert faculty_added.maximum_credits == 9
        assert faculty_added.times == {'Monday': ["9-3"]}
        assert faculty_added.course_preferences == {"CMSC 162": 5}

    def test_mod_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.mod_faculty(
            json_config = json_config,
            name = "Dr. Test Mod",
            maximum_credits=7,
            minimum_credits=3,
            unique_course_limit=2,
            times={MONDAY: ["9-3"]},
            course_preferences={"CMSC 162": 5},
            room_preferences={"Roddy 140": 3},
            lab_preferences={"Mac Lab": 7}
        )
        faculty_mod = json_config.config.faculty[0]
        assert faculty_mod.name == "Dr. Test Mod"
        assert faculty_mod.maximum_credits == 7
        assert faculty_mod.room_preferences == {"Roddy 140": 3}

    def test_del_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.del_faculty(
            json_config = json_config,
            name = "Dr. Test"
        )
        assert len(json_config.config.faculty) == 0