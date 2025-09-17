from .json import JsonConfig
from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig, CourseConfig
from typing import Any

class courses: 

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

    

    