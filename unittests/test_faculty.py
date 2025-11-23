import os
from types import SimpleNamespace
from typing import cast

import pytest
from scheduler import TimeRange, CourseConfig

from scheduler_config_editor.model import Faculty, JsonConfig


@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))


class TestFaculty:
    def test_add_faculty(self, json_config: JsonConfig):
        Faculty.add_faculty(
            json_config=json_config,
            name="Dr. Test",
            maximum_credits=9,
            minimum_credits=3,
            unique_course_limit=2,
            times={"MON": ["09:00-15:00"]},
            course_preferences={"CMSC 162": 5},
            room_preferences={"Roddy 136": 3},
            lab_preferences={"Mac": 7},
        )
        faculty_added = json_config.scheduler_config.faculty[
            len(json_config.scheduler_config.faculty) - 1
        ]
        assert faculty_added.name == "Dr. Test"
        assert faculty_added.maximum_credits == 9
        assert faculty_added.times == {"MON": [TimeRange(start="09:00", end="15:00")]}
        assert faculty_added.course_preferences == {"CMSC 162": 5}

    def test_add_faculty_missing_name(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name=None,
                maximum_credits=9,
                minimum_credits=3,
                unique_course_limit=2,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"CMSC 162": 5},
                room_preferences={"Roddy 136": 3},
                lab_preferences={"Mac": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_invalid_credits(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name="Dr. Test",
                maximum_credits=3,
                minimum_credits=9,
                unique_course_limit=2,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"CMSC 162": 5},
                room_preferences={"Roddy 136": 3},
                lab_preferences={"Mac": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_invalid_course_limit(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name="Dr. Test",
                maximum_credits=9,
                minimum_credits=3,
                unique_course_limit=0,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"CMSC 162": 5},
                room_preferences={"Roddy 136": 3},
                lab_preferences={"Mac": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_invalid_course_pref(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name="Dr. Test",
                maximum_credits=9,
                minimum_credits=3,
                unique_course_limit=2,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"COURSE": 5},
                room_preferences={"Roddy 136": 3},
                lab_preferences={"Mac": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_invalid_room_pref(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name="Dr. Test",
                maximum_credits=9,
                minimum_credits=3,
                unique_course_limit=2,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"CMSC 162": 5},
                room_preferences={"ROOM": 3},
                lab_preferences={"Mac": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_invalid_lab_pref(self, json_config: JsonConfig):
        try:
            Faculty.add_faculty(
                json_config=json_config,
                name="Dr. Test",
                maximum_credits=9,
                minimum_credits=3,
                unique_course_limit=2,
                times={"MON": ["09:00-15:00"]},
                course_preferences={"CMSC 162": 5},
                room_preferences={"Roddy 136": 3},
                lab_preferences={"LAB": 7},
            )
            assert False
        except ValueError:
            assert True

    def test_add_faculty_defaults(self, json_config: JsonConfig):
        # omit optional args to exercise defaulting behavior
        Faculty.add_faculty(
            json_config=json_config,
            name="Defaulted",
            maximum_credits=1,
            minimum_credits=0,
            unique_course_limit=1,
            times={"MON": ["09:00-15:00"]},
        )
        f = next(
            f for f in json_config.scheduler_config.faculty if f.name == "Defaulted"
        )
        assert getattr(f, "course_preferences", {}) == {}
        assert getattr(f, "room_preferences", {}) == {}
        assert getattr(f, "lab_preferences", {}) == {}

    def test_mod_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.mod_faculty(
            json_config=json_config,
            old_name="Dr. Test",
            new_name="Dr. Test Mod",
            maximum_credits=7,
            minimum_credits=3,
            unique_course_limit=2,
            times={"MON": ["09:00-15:00"]},
            course_preferences={"CMSC 162": 5},
            room_preferences={"Roddy 140": 3},
            lab_preferences={"Mac": 7},
        )
        faculty_mod = json_config.scheduler_config.faculty[
            len(json_config.scheduler_config.faculty) - 1
        ]
        assert faculty_mod.name == "Dr. Test Mod"
        assert faculty_mod.maximum_credits == 7
        assert faculty_mod.room_preferences == {"Roddy 140": 3}

    def test_mod_faculty_raises_when_course_has_only_that_faculty(
        self, json_config: JsonConfig
    ):
        # add faculty and a course that references only that faculty -> should raise
        Faculty.add_faculty(
            json_config=json_config,
            name="SoloFaculty",
            maximum_credits=2,
            minimum_credits=0,
            unique_course_limit=1,
            times={"MON": ["09:00-15:00"]},
        )

        # create a minimal course-like object and cast it to CourseConfig for typing
        c = cast(CourseConfig, SimpleNamespace())
        c.course_id = "ONLY1"
        c.faculty = ["SoloFaculty"]
        c.credits = 3
        json_config.scheduler_config.courses.append(c)

        with pytest.raises(ValueError):
            Faculty.mod_faculty(
                json_config=json_config,
                old_name="SoloFaculty",
                new_name="SoloFacultyNew",
                maximum_credits=3,
                minimum_credits=0,
                unique_course_limit=1,
                times={},
                course_preferences={},  # empty -> triggers the error branch
                room_preferences={},
                lab_preferences={},
            )

    def test_mod_faculty_no_raise_when_course_in_course_preferences(
        self, json_config: JsonConfig
    ):
        Faculty.add_faculty(
            json_config=json_config,
            name="KeepPref",
            maximum_credits=3,
            minimum_credits=0,
            unique_course_limit=1,
            times={"MON": ["09:00-15:00"]},
        )

        # minimal course-like object typed as CourseConfig
        c = cast(CourseConfig, SimpleNamespace())
        c.course_id = "P1"
        c.faculty = ["KeepPref"]
        c.credits = 3
        json_config.scheduler_config.courses.append(c)

        # include the course id in course_preferences so the removal branch is skipped (no ValueError)
        Faculty.mod_faculty(
            json_config=json_config,
            old_name="KeepPref",
            new_name="KeepPrefNew",
            maximum_credits=4,
            minimum_credits=0,
            unique_course_limit=1,
            times={},
            course_preferences={"P1": 10},
            room_preferences={},
            lab_preferences={},
        )

        assert "KeepPrefNew" in json_config.scheduler_config.courses[-1].faculty
        assert "KeepPref" not in json_config.scheduler_config.courses[-1].faculty

    def test_del_faculty(self, json_config: JsonConfig):
        self.test_add_faculty(json_config)
        Faculty.del_faculty(json_config=json_config, name="Dr. Test")
        for i, _faculty in enumerate(json_config.scheduler_config.faculty):
            assert json_config.scheduler_config.faculty[i].name != "Dr. Test"

    def test_del_faculty_noop_when_not_found(self, json_config: JsonConfig):
        before = list(json_config.scheduler_config.faculty)
        Faculty.del_faculty(json_config=json_config, name="NotPresent")
        # no change when name not found
        assert [f.name for f in json_config.scheduler_config.faculty] == [
            f.name for f in before
        ]

    def test_del_faculty_course_reference_removed(self, json_config: JsonConfig):
        # add faculty and a course that references it
        Faculty.add_faculty(
            json_config=json_config,
            name="ToRemove",
            maximum_credits=4,
            minimum_credits=0,
            unique_course_limit=1,
            times={"MON": ["09:00-15:00"]},
        )

        # minimal course object cast to CourseConfig
        c1 = cast(CourseConfig, SimpleNamespace())
        c1.course_id = "A"
        c1.faculty = ["ToRemove"]
        c1.credits = 3
        json_config.scheduler_config.courses.extend([c1])

        Faculty.del_faculty(json_config=json_config, name="ToRemove")

        assert all(
            getattr(f, "name", None) != "ToRemove"
            for f in json_config.scheduler_config.faculty
        )
        assert "ToRemove" not in json_config.scheduler_config.courses[0].faculty

    def test_list_faculty(self, json_config: JsonConfig):
        output = Faculty.faculty_string(json_config)
        assert "Zoppetti" in output  # from dummy.json
        assert "Wertz" in output
