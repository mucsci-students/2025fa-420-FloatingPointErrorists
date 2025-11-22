# File: unittests/test_courses.py
import sys
import importlib
import types
from pathlib import Path
from typing import Any

import pytest


# Minimal stand-ins matching the interface used by the module under test.
class DummyCourseConfig:
    def __init__(self, course_id, credits, room, lab, conflicts, faculty):
        self.course_id = course_id
        self.credits = credits
        self.room = room
        self.lab = lab
        self.conflicts = conflicts
        self.faculty = faculty


class DummyFaculty:
    def __init__(self, name, course_preferences=None):
        self.name = name
        self.course_preferences = (
            {} if course_preferences is None else dict(course_preferences)
        )
        # Other fields from JsonConfig.json() are not required by courses.py


class DummySchedulerConfig:
    def __init__(self, courses=None, faculty=None, rooms=None, labs=None):
        self.courses = [] if courses is None else list(courses)
        self.faculty = [] if faculty is None else list(faculty)
        self.rooms = [] if rooms is None else list(rooms)
        self.labs = [] if labs is None else list(labs)


class DummyJsonConfig:
    def __init__(self, scheduler_config):
        self.scheduler_config = scheduler_config


@pytest.fixture(autouse=True)
def import_courses_module(tmp_path, monkeypatch):
    """
    Ensure project's `src` is on sys.path and inject a fake 'scheduler' module
    exposing `CourseConfig` before importing the module under test so the module
    uses our DummyCourseConfig.
    """
    repo_root = Path(__file__).resolve().parents[1]
    src_dir = repo_root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    fake_sched: Any = types.ModuleType("scheduler")
    # use setattr to avoid static-analyzer `unresolved-attribute` on ModuleType
    setattr(fake_sched, "CourseConfig", DummyCourseConfig)
    # Put other scheduler names in place if other tests expect them
    monkeypatch.setitem(sys.modules, "scheduler", fake_sched)

    mod = importlib.import_module("scheduler_config_editor.model.courses")
    importlib.reload(mod)
    return mod


def test_add_course_appends_and_updates_faculty_preferences(import_courses_module):
    courses_mod = import_courses_module

    alice = DummyFaculty("Alice")
    bob = DummyFaculty("Bob")
    sched = DummySchedulerConfig(courses=[], faculty=[alice, bob], rooms=["R1"])
    json_cfg = DummyJsonConfig(sched)

    courses_mod.Course.add_course(
        json_config=json_cfg,
        course_id="CS101",
        course_credits=3,
        room=["R1"],
        lab=[],
        conflicts=[],
        faculty=["Alice"],
    )

    assert len(json_cfg.scheduler_config.courses) == 1
    created = json_cfg.scheduler_config.courses[0]
    assert created.course_id == "CS101"
    assert created.credits == 3
    assert created.room == ["R1"]
    assert created.conflicts == []
    assert created.faculty == ["Alice"]

    assert alice.course_preferences.get("CS101") == 5
    assert "CS101" not in bob.course_preferences

def test_add_course_missing_id(import_courses_module):
    courses_mod = import_courses_module
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=[])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id=None,
            course_credits=0,
            room=[],
            lab=[],
            conflicts=[],
            faculty=[],
        )
        assert False
    except ValueError:
        assert True

def test_add_course_invalid_credits(import_courses_module):
    courses_mod = import_courses_module
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=[])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=0,
            room=[],
            lab=[],
            conflicts=[],
            faculty=[],
        )
        assert False
    except ValueError:
        assert True

def test_add_course_missing_room(import_courses_module):
    courses_mod = import_courses_module
    
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=[])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=3,
            room=None,
            lab=[],
            conflicts=[],
            faculty=[],
        )
        assert False
    except ValueError:
        assert True
    
def test_add_course_invalid_room(import_courses_module):
    courses_mod = import_courses_module
    
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=[])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=3,
            room=["R1"],
            lab=[],
            conflicts=[],
            faculty=[],
        )
        assert False
    except ValueError:
        assert True

def test_add_course_missing_faculty(import_courses_module):
    courses_mod = import_courses_module
    
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=["R1"])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=0,
            room=["R1"],
            lab=[],
            conflicts=[],
            faculty=None,
        )
        assert False
    except ValueError:
        assert True
    
def test_add_course_invalid_faculty(import_courses_module):
    courses_mod = import_courses_module
    
    sched = DummySchedulerConfig(courses=[], faculty=[], rooms=["R1"])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=0,
            room=["R1"],
            lab=[],
            conflicts=[],
            faculty=["Alice"],
        )
        assert False
    except ValueError:
        assert True

def test_add_course_invalid_lab(import_courses_module):
    courses_mod = import_courses_module
    
    alice = DummyFaculty("Alice")
    bob = DummyFaculty("Bob")
    sched = DummySchedulerConfig(courses=[], faculty=[alice, bob], rooms=["R1"])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=3,
            room=["R1"],
            lab=["TEST"],
            conflicts=[],
            faculty=["Alice"],
        )
        assert False
    except ValueError:
        assert True

def test_add_course_invalid_conflict(import_courses_module):
    courses_mod = import_courses_module
    
    alice = DummyFaculty("Alice")
    bob = DummyFaculty("Bob")
    sched = DummySchedulerConfig(courses=[], faculty=[alice, bob], rooms=["R1"])
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.add_course(
            json_config=json_cfg,
            course_id="CS101",
            course_credits=3,
            room=["R1"],
            lab=[],
            conflicts=["COURSE"],
            faculty=["Alice"],
        )
        assert False
    except ValueError:
        assert True

def test_mod_course_changes_id_updates_faculty_and_conflicts(import_courses_module):
    courses_mod = import_courses_module
    fac = DummyFaculty("DrX", course_preferences={"OLD101": 7})
    c_old = DummyCourseConfig(
        course_id="OLD101", credits=3, room=[], lab=[], conflicts=[], faculty=["DrX"]
    )
    c_other = DummyCourseConfig(
        course_id="OTHER", credits=2, room=[], lab=[], conflicts=["OLD101"], faculty=["DrX"]
    )
    sched = DummySchedulerConfig(
        courses=[c_old, c_other], faculty=[fac], rooms=["RmA"], labs=["LabA"]
    )
    json_cfg = DummyJsonConfig(sched)

    courses_mod.Course.mod_course(
        index=0,
        json_config=json_cfg,
        course_id="NEW101",
        course_credits=4,
        room=["RmA"],
        lab=["LabA"],
        conflicts=["OTHER"],
    )

    updated = json_cfg.scheduler_config.courses[0]
    assert updated.course_id == "NEW101"
    assert updated.credits == 4
    assert updated.room == ["RmA"]
    assert updated.lab == ["LabA"]
    assert updated.conflicts == ["OTHER"]

    assert "OLD101" not in fac.course_preferences
    assert fac.course_preferences.get("NEW101") == 7

    assert "OLD101" not in json_cfg.scheduler_config.courses[1].conflicts
    assert "NEW101" in json_cfg.scheduler_config.courses[1].conflicts


def test_mod_course_same_id_adds_new_faculty_preference(import_courses_module):
    courses_mod = import_courses_module

    c = DummyCourseConfig(
        course_id="MATH1", credits=3, room=[], lab=[], conflicts=[], faculty=[]
    )
    existing_fac = DummyFaculty("Known", course_preferences={"MATH1": 8})
    new_fac = DummyFaculty("Newbie")
    sched = DummySchedulerConfig(
        courses=[c], faculty=[existing_fac, new_fac], rooms=["R2"]
    )
    json_cfg = DummyJsonConfig(sched)

    courses_mod.Course.mod_course(
        index=0,
        json_config=json_cfg,
        course_id="MATH1",
        course_credits=5,
        room=["R2"],
        lab=[],
        conflicts=[],
        faculty=["Newbie", "Known"],
    )

    assert existing_fac.course_preferences.get("MATH1") == 8
    assert new_fac.course_preferences.get("MATH1") == 5

    updated = json_cfg.scheduler_config.courses[0]
    assert updated.credits == 5
    assert updated.room == ["R2"]

def test_mod_course_out_of_bounds(import_courses_module):
    courses_mod = import_courses_module
    # fac = DummyFaculty("DrX", course_preferences={"OLD101": 7})
    # c_old = DummyCourseConfig(
    #     course_id="OLD101", credits=3, room=[], lab=[], conflicts=[], faculty=["DrX"]
    # )
    # c_other = DummyCourseConfig(
    #     course_id="OTHER", credits=2, room=[], lab=[], conflicts=["OLD101"], faculty=["DrX"]
    # )
    sched = DummySchedulerConfig(
        courses=[], faculty=[], rooms=[], labs=[]
    )
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.mod_course(
            index=1,
            json_config=json_cfg,
            course_id="NEW101",
            course_credits=4,
            room=["RmA"],
            lab=["LabA"],
            conflicts=["OTHER"],
        )
        assert False
    except IndexError:
        assert True


def test_del_course_removes_and_cleans_references(import_courses_module):
    courses_mod = import_courses_module

    to_delete = DummyCourseConfig(
        course_id="DELME", credits=1, room=[], lab=[], conflicts=[], faculty=[]
    )
    other = DummyCourseConfig(
        course_id="C2", credits=2, room=[], lab=[], conflicts=["DELME"], faculty=[]
    )
    fac = DummyFaculty("ProfY", course_preferences={"DELME": 4, "C2": 6})
    sched = DummySchedulerConfig(courses=[to_delete, other], faculty=[fac])
    json_cfg = DummyJsonConfig(sched)

    courses_mod.Course.del_course(index=0, json_config=json_cfg)

    assert all(c.course_id != "DELME" for c in json_cfg.scheduler_config.courses)
    assert "DELME" not in fac.course_preferences
    assert "DELME" not in json_cfg.scheduler_config.courses[0].conflicts

def test_del_course_out_of_bounds(import_courses_module):
    courses_mod = import_courses_module
    # fac = DummyFaculty("DrX", course_preferences={"OLD101": 7})
    # c_old = DummyCourseConfig(
    #     course_id="OLD101", credits=3, room=[], lab=[], conflicts=[], faculty=["DrX"]
    # )
    # c_other = DummyCourseConfig(
    #     course_id="OTHER", credits=2, room=[], lab=[], conflicts=["OLD101"], faculty=["DrX"]
    # )
    sched = DummySchedulerConfig(
        courses=[], faculty=[], rooms=[], labs=[]
    )
    json_cfg = DummyJsonConfig(sched)

    try:
        courses_mod.Course.del_course(index=1, json_config=json_cfg)
        assert False
    except IndexError:
        assert True


def test_courses_string_formats_list(import_courses_module):
    courses_mod = import_courses_module

    c1 = DummyCourseConfig(
        course_id="A1", credits=1, room=["R1"], lab=[], conflicts=["C2"], faculty=["F1"]
    )
    c2 = DummyCourseConfig(
        course_id="B2",
        credits=2,
        room=["R2"],
        lab=["L2"],
        conflicts=[],
        faculty=["F2", "F3"],
    )
    sched = DummySchedulerConfig(
        courses=[c1, c2], faculty=[], rooms=["R1", "R2"], labs=["L2"]
    )
    json_cfg = DummyJsonConfig(sched)

    s = courses_mod.Course.courses_string(json_cfg)
    assert "0: A1" in s
    assert "1: B2" in s
    assert "Credits: 1" in s
    assert "Rooms: ['R2']" in s
    assert "Labs: ['L2']" in s
    assert "Conflicts: ['C2']" in s
    assert "Faculty: ['F2', 'F3']" in s
