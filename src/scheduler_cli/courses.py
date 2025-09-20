from .json import JsonConfig
from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig, CourseConfig
from typing import Any
    
@staticmethod
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

def mod_course(index: int, json_config: JsonConfig, course_id: str, credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
    course_config = CourseConfig(
        course_id=course_id,
        credits=credits,
        room=room,
        lab=lab,
        conflicts=conflicts,
        faculty=faculty
    )
    for i, faculty in enumerate(json_config.config.courses):
        if json_config.config.faculty[i].name == index:
            json_config.config.faculty[i] = course_config
            break


@staticmethod    
def del_course(index: int, json_config:JsonConfig) -> None:
    config_to_delete = json_config.config.courses.__getitem__(index)
    json_config.config.courses.remove(config_to_delete)


    
