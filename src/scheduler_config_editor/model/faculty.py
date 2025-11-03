from _ast import Gt
from typing import Annotated, Optional, cast

from scheduler import Day, FacultyConfig, TimeRange

from .json import JsonConfig


class Faculty:
    """
    This class allows the user to create, modify and delete faculty from the JsonConfig
    """

    @staticmethod
    def check_values(
        json_config: JsonConfig,
        name: str,
        maximum_credits: int,
        minimum_credits: int,
        unique_course_limit: int,
        course_preferences: Optional[dict[str, int]] = None,
        room_preferences: Optional[dict[str, int]] = None,
        lab_preferences: Optional[dict[str, int]] = None,
    ) -> None:
        if not name:
            raise ValueError("Faculty name cannot be empty.")
        if (
            maximum_credits < 0
            or minimum_credits < 0
            or maximum_credits < minimum_credits
        ):
            raise ValueError("Invalid credit limits for faculty member.")
        if unique_course_limit <= 0:
            raise ValueError("Unique course limit must be greater than 0.")
        if course_preferences is not None:
            for course in course_preferences:
                if course not in [
                    c.course_id for c in json_config.scheduler_config.courses
                ]:
                    raise ValueError(
                        f"Course {course} does not exist in the configuration."
                    )
        if room_preferences is not None:
            for room in room_preferences:
                if room not in json_config.scheduler_config.rooms:
                    raise ValueError(
                        f"Room {room} does not exist in the configuration."
                    )
        if lab_preferences is not None:
            for lab in lab_preferences:
                if lab not in json_config.scheduler_config.labs:
                    raise ValueError(f"Lab {lab} does not exist in the configuration.")

    @staticmethod
    def add_faculty(
        json_config: JsonConfig,
        name: str,
        maximum_credits: int,
        minimum_credits: int,
        unique_course_limit: Annotated[int, Gt()],
        times: dict[str, list[str]],
        course_preferences: Optional[dict[str, int]] = None,
        room_preferences: Optional[dict[str, int]] = None,
        lab_preferences: Optional[dict[str, int]] = None,
    ) -> str:
        """adds a new faculty member to the config file"""
        if lab_preferences is None:
            lab_preferences = {}
        if room_preferences is None:
            room_preferences = {}
        if course_preferences is None:
            course_preferences = {}
        Faculty.check_values(
            json_config,
            name,
            maximum_credits,
            minimum_credits,
            unique_course_limit,
            course_preferences,
            room_preferences,
            lab_preferences,
        )
        times_casted = cast(dict[Day, list[TimeRange]], times)
        faculty_config = FacultyConfig(
            name=name,
            maximum_credits=maximum_credits,
            minimum_credits=minimum_credits,
            unique_course_limit=unique_course_limit,
            times=times_casted,
            course_preferences=course_preferences,
            room_preferences=room_preferences,
            lab_preferences=lab_preferences,
        )
        """adds the new faculty config to the scheduler config"""
        json_config.scheduler_config.faculty.append(faculty_config)
        return f"Faculty member {name} added successfully."

    @staticmethod
    def mod_faculty(
        json_config: JsonConfig,
        old_name: str,
        new_name: Optional[str] = None,
        maximum_credits: Optional[int] = None,
        minimum_credits: Optional[int] = None,
        unique_course_limit: Optional[int] = None,
        times: Optional[dict[str, list[str]]] = None,
        course_preferences: Optional[dict[str, int]] = None,
        room_preferences: Optional[dict[str, int]] = None,
        lab_preferences: Optional[dict[str, int]] = None,
    ) -> str:
        """modifies a current faculty member and updates their information"""
        found = False
        for i, _faculty in enumerate(json_config.scheduler_config.faculty):
            """finds the faculty within the scheduler and replaces it with the updated one"""
            if json_config.scheduler_config.faculty[i].name == old_name:
                new_faculty = FacultyConfig(
                    name=new_name if new_name is not None else old_name,
                    maximum_credits=maximum_credits
                    if maximum_credits is not None
                    else _faculty.maximum_credits,
                    minimum_credits=minimum_credits
                    if minimum_credits is not None
                    else _faculty.minimum_credits,
                    unique_course_limit=unique_course_limit
                    if unique_course_limit is not None
                    else _faculty.unique_course_limit,
                    times=cast(dict[Day, list[TimeRange]], times)
                    if times is not None
                    else _faculty.times,
                    course_preferences=course_preferences
                    if course_preferences is not None
                    else _faculty.course_preferences,
                    room_preferences=room_preferences
                    if room_preferences is not None
                    else _faculty.room_preferences,
                    lab_preferences=lab_preferences
                    if lab_preferences is not None
                    else _faculty.lab_preferences,
                )
                Faculty.check_values(
                    json_config,
                    new_faculty.name,
                    new_faculty.maximum_credits,
                    new_faculty.minimum_credits,
                    new_faculty.unique_course_limit,
                    new_faculty.course_preferences,
                    new_faculty.room_preferences,
                    new_faculty.lab_preferences,
                )
                json_config.scheduler_config.faculty[i] = new_faculty
                found = True
        for course in json_config.scheduler_config.courses:
            if (old_name in course.faculty) and (
                course_preferences is None or course.course_id not in course_preferences
            ):
                if len(course.faculty) == 1:
                    raise ValueError(
                        f"Cannot remove {course.course_id} from course preferences as {old_name} is the only faculty who can teach it."
                    )
                course.faculty.remove(old_name)
        for i, _courses in enumerate(json_config.scheduler_config.courses):
            for f, _faculty in enumerate(
                json_config.scheduler_config.courses[i].faculty
            ):
                if json_config.scheduler_config.courses[i].faculty[f] == old_name:
                    json_config.scheduler_config.courses[i].faculty[f] = (
                        new_name if new_name else old_name
                    )
                    break
        return (
            f"Faculty member {old_name} updated successfully."
            if found
            else f"Faculty member {old_name} not found."
        )

    @staticmethod
    def del_faculty(json_config: JsonConfig, name: str) -> str:
        """finds the faculty within the scheduler and removes it"""
        found = False
        for i, _faculty in enumerate(json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == name:
                del json_config.scheduler_config.faculty[i]
                found = True
                break
        for i, _courses in enumerate(json_config.scheduler_config.courses):
            if name in json_config.scheduler_config.courses[i].faculty:
                json_config.scheduler_config.courses[i].faculty.remove(name)
                break
        return (
            f"Faculty member {name} deleted successfully."
            if found
            else f"Faculty member {name} not found."
        )
