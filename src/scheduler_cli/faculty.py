from _ast import Gt
from calendar import Day
from typing import Dict, List, Annotated
from .json import JsonConfig
from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig, FacultyConfig

"""
This class allows the user to create, modify and delete faculty from the JsonConfig
"""


class Faculty:
    """adds a new faculty member to the config file"""

    @staticmethod
    def add_faculty(json_config: JsonConfig, name: str, maximum_credits: int, minimum_credits: int,
                    unique_course_limit: Annotated[int, Gt(0)],
                    times: Dict[Day, List[str]] = None, course_preferences: Dict[str, int] = None,
                    room_preferences: Dict[str, int] = None, lab_preferences: Dict[str, int] = None):
        """creates a new faculty config file"""
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
        json_config.config.faculty.append(faculty_config)

    """modifies a current faculty member and updates their information"""

    @staticmethod
    def mod_faculty(json_config: JsonConfig, name: str, maximum_credits: int, minimum_credits: int,
                    unique_course_limit: Annotated[int, Gt(0)],
                    times: Dict[Day, List[str]] = None, course_preferences: Dict[str, int] = None,
                    room_preferences: Dict[str, int] = None, lab_preferences: Dict[str, int] = None):
        """creates a new faculty config file with updated faculty info"""
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
        for i, faculty in enumerate(json_config.config.faculty):
            if json_config.config.faculty[i].name == name:
                json_config.config.faculty[i] = faculty_config
                break

    """deletes a faculty member from the scheduler config"""

    @staticmethod
    def del_faculty(json_config: JsonConfig, name: str):
        """finds the faculty within the scheduler and removes it"""
        for i, faculty in enumerate(json_config.config.faculty):
            if json_config.config.faculty[i].name == name:
                del json_config.config.faculty[i]
                break

    """Getters for each attribute of a faculty member"""

    def getName(json_config: JsonConfig, index):
        return json_config.config.faculty[index].name

    def getMaximum_credits(json_config: JsonConfig, index):
        return json_config.config.faculty[index].maximum_credits

    def getMinimum_credits(json_config: JsonConfig, index):
        return json_config.config.faculty[index].minimum_credits

    def getUnique_course_limit(json_config: JsonConfig, index):
        return json_config.config.faculty[index].unique_course_limit

    def getTimes(json_config: JsonConfig, index):
        return json_config.config.faculty[index].times

    def getCourse_preferences(json_config: JsonConfig, index):
        return json_config.config.faculty[index].course_preferences

    def getRoom_preferences(json_config: JsonConfig, index):
        return json_config.config.faculty[index].room_preferences

    def getLab_preferences(json_config: JsonConfig, index):
        return json_config.config.faculty[index].lab_preferences

    """Setters for each attribute of a faculty member"""

    def setName(json_config: JsonConfig, index, newName: str):
        if not isinstance(newName, str):
            raise TypeError("Name must be a string")
        json_config.config.faculty[index].name = newName

    def setMaximumCredits(json_config: JsonConfig, index, newMaximumCredits: int):
        if not isinstance(newMaximumCredits, int) or newMaximumCredits < 0:
            raise TypeError("Maximum Credits must be a positive integer")
        json_config.config.faculty[index].maximum_credits = newMaximumCredits

    def setMinimumCredits(json_config: JsonConfig, index, newMinimumCredits: int):
        if not isinstance(newMinimumCredits, int) or newMinimumCredits < 0:
            raise TypeError("Minimum Credits must be a positive integer")
        json_config.config.faculty[index].minimum_credits = newMinimumCredits

    def setUniqueCourseLimit(json_config: JsonConfig, index, newUniqueCourseLimit: int):
        if not isinstance(newUniqueCourseLimit, int) or newUniqueCourseLimit < 0:
            raise TypeError("Unique Course Limit must be a positive integer")
        json_config.config.faculty[index].unique_course_limit = newUniqueCourseLimit

    def setTimes(json_config: JsonConfig, index, newTimes: Dict[str, List[str]]):
        if not isinstance(newTimes, dict):
            raise TypeError("Times must be a dictionary")
        json_config.config.faculty[index].times = newTimes

    def setCoursePreferences(json_config: JsonConfig, index, newCoursePreferences: Dict[str, int]):
        if not isinstance(newCoursePreferences, dict):
            raise TypeError("Course Preferences must be a dictionary")
        json_config.config.faculty[index].course_preferences = newCoursePreferences

    def setRoomPreferences(json_config: JsonConfig, index, newRoomPreferences: Dict[str, int]):
        if not isinstance(newRoomPreferences, dict):
            raise TypeError("Room Preferences must be a dictionary")
        json_config.config.faculty[index].room_preferences = newRoomPreferences

    def setLabPreferences(json_config: JsonConfig, index, newLabPreferences: Dict[str, int]):
        if not isinstance(newLabPreferences, dict):
            raise TypeError("Lab Preferences must be a dictionary")
        json_config.config.faculty[index].lab_preferences = newLabPreferences


