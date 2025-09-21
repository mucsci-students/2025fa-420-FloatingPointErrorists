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
    def mod_faculty(json_config: JsonConfig, name: str, maximum_credits: int, minimum_credits: int,
                    unique_course_limit: Annotated[int, Gt()],
                    times: Dict[str, List[str]] = {}, course_preferences: Dict[str, int] = {},
                    room_preferences: Dict[str, int] = {}, lab_preferences: Dict[str, int] = {}) -> None:
        """modifies a current faculty member and updates their information"""
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
        """finds the faculty within the scheduler and replaces it with the updated one"""
        for i, faculty in enumerate(json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == name:
                json_config.scheduler_config.faculty[i] = faculty_config
                break

    @staticmethod
    def del_faculty(json_config: JsonConfig, name: str) -> None:
        """finds the faculty within the scheduler and removes it"""
        for i, faculty in enumerate(json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == name:
                del json_config.scheduler_config.faculty[i]
                break