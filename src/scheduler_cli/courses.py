from .json import JsonConfig
from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig, CourseConfig
from typing import Any


def add_course(json_config: JsonConfig, course_id: str, credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:

    course_config = CourseConfig(
        course_id=course_id,
        credits=credits,
        room=room,
        lab=lab,
        conflicts=conflicts,
        faculty=faculty
    )
    json_config.config.courses.append(course_config)

def mod_course(json_config: JsonConfig, course_id: str, credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
    course_config = CourseConfig(
        course_id=course_id,
        credits=credits,
        room=room,
        lab=lab,
        conflicts=conflicts,
        faculty=faculty
    )
    course_index: int = json_config.config.courses.index(course_config)
    json_config.config.courses.__setitem__(course_index, course_config)


    
def del_course(json_config: JsonConfig, course_id: str, credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
    course_config = CourseConfig(
        course_id=course_id,
        credits=credits,
        room=room,
        lab=lab,
        conflicts=conflicts,
        faculty=faculty
    )

    json_config.config.courses.remove(course_config)


    
