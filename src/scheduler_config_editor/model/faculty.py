from _ast import Gt
from typing import Dict, List, Annotated
from .json import JsonConfig
from scheduler import FacultyConfig


class Faculty:
    """
    This class allows the user to create, modify and delete faculty from the JsonConfig
    """

    @staticmethod
    def add_faculty(json_config: JsonConfig, name: str, maximum_credits: int, minimum_credits: int,
                    unique_course_limit: Annotated[int, Gt()],
                    times: Dict[str, List[str]] = {}, course_preferences: Dict[str, int] = {},
                    room_preferences: Dict[str, int] = {}, lab_preferences: Dict[str, int] = {}) -> None:
        """adds a new faculty member to the config file"""
        faculty_config = FacultyConfig(
            name=name,
            maximum_credits=maximum_credits,
            minimum_credits=minimum_credits,
            unique_course_limit=unique_course_limit,
            times=times,
            course_preferences=course_preferences,
            room_preferences=room_preferences,
            lab_preferences=lab_preferences
        )
        """adds the new faculty config to the scheduler config"""
        json_config.scheduler_config.faculty.append(faculty_config)

    @staticmethod
    def mod_faculty(json_config: JsonConfig, old_name: str,  new_name: str, maximum_credits: int, minimum_credits: int,
                    unique_course_limit: Annotated[int, Gt()],
                    times: Dict[str, List[str]] = {}, course_preferences: Dict[str, int] = {},
                    room_preferences: Dict[str, int] = {}, lab_preferences: Dict[str, int] = {}) -> None:
        """modifies a current faculty member and updates their information"""
        faculty_config = FacultyConfig(
            name=new_name,
            maximum_credits=maximum_credits,
            minimum_credits=minimum_credits,
            unique_course_limit=unique_course_limit,
            times=times,
            course_preferences=course_preferences,
            room_preferences=room_preferences,
            lab_preferences=lab_preferences
        )
        for course in json_config.scheduler_config.courses:
            if old_name in course.faculty and course.course_id not in course_preferences:
                if len(course.faculty) == 1:
                    raise ValueError(f"Cannot remove {course.course_id} from course preferences as {old_name} is the only faculty assigned to it.")
                course.faculty.remove(old_name)
        """finds the faculty within the scheduler and replaces it with the updated one"""
        for i, faculty in enumerate(json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == old_name:
                json_config.scheduler_config.faculty[i] = faculty_config
        for i, courses in enumerate(json_config.scheduler_config.courses):
                for f, faculty in enumerate(json_config.scheduler_config.courses[i].faculty):
                    if json_config.scheduler_config.courses[i].faculty[f] == old_name:
                        json_config.scheduler_config.courses[i].faculty[f] = new_name
                        break

    @staticmethod
    def del_faculty(json_config: JsonConfig, name: str) -> None:
        """finds the faculty within the scheduler and removes it"""
        for i, faculty in enumerate(json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == name:
                del json_config.scheduler_config.faculty[i]
        for i, courses in enumerate(json_config.scheduler_config.courses):
                if name in json_config.scheduler_config.courses[i].faculty:
                    json_config.scheduler_config.courses[i].faculty.remove(name)
                    break