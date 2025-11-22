from typing import Optional

from scheduler import CourseConfig

from .json import JsonConfig


class Course:
    """
    This class allows the user to create, modify and delete courses from the JsonConfig
    """

    @staticmethod
    def check_values(
        json_config: JsonConfig,
        course_id: str,
        course_credits: int,
        room: Optional[list[str]] = None,
        faculty: Optional[list[str]] = None,
        lab: Optional[list[str]] = None,
        conflicts: Optional[list[str]] = None,
    ) -> None:
        """checks that the values provided are valid"""
        if not course_id:
            raise ValueError("Course ID cannot be empty.")
        if course_credits <= 0:
            raise ValueError("Course credits must be greater than 0.")
        if room is not None:
            if not room:
                raise ValueError("At least one room must be assigned to a course.")
            for r in room:
                if r not in json_config.scheduler_config.rooms:
                    raise ValueError(f"Room {r} does not exist in the configuration.")
        if faculty is not None:
            if not faculty:
                raise ValueError(
                    "At least one faculty member must be assigned to a course."
                )
            for f in faculty:
                if f not in [fac.name for fac in json_config.scheduler_config.faculty]:
                    raise ValueError(
                        f"Faculty {f} does not exist in the configuration."
                    )
        if conflicts is not None:
            for c in conflicts:
                if c not in [
                    course.course_id for course in json_config.scheduler_config.courses
                ]:
                    raise ValueError(
                        f"Conflict course {c} does not exist in the configuration."
                    )
        if lab is not None:
            for lab_name in lab:
                if lab_name not in json_config.scheduler_config.labs:
                    raise ValueError(
                        f"Lab {lab_name} does not exist in the configuration."
                    )

    @staticmethod
    def add_course(
        json_config: JsonConfig,
        course_id: str,
        course_credits: int,
        room: list[str],
        faculty: list[str],
        lab: Optional[list[str]] = None,
        conflicts: Optional[list[str]] = None,
    ) -> str:
        """adds a new course to the config file"""
        Course.check_values(
            json_config, course_id, course_credits, room, faculty, lab, conflicts
        )
        if lab is None:
            lab = []
        if conflicts is None:
            conflicts = []
        course_config = CourseConfig(
            course_id=course_id,
            credits=course_credits,
            room=room,
            lab=lab,
            conflicts=conflicts,
            faculty=faculty,
        )
        for faculty_member in json_config.scheduler_config.faculty:
            if faculty_member.name in faculty:
                faculty_member.course_preferences[course_id] = (
                    5  # default preference score
                )
        json_config.scheduler_config.courses.append(course_config)
        return f"Course {course_id} successfully added."

    @staticmethod
    def mod_course(
        index: int,
        json_config: JsonConfig,
        course_id: Optional[str] = None,
        course_credits: Optional[int] = None,
        room: Optional[list[str]] = None,
        lab: Optional[list[str]] = None,
        conflicts: Optional[list[str]] = None,
        faculty: Optional[list[str]] = None,
    ) -> str:
        """modifies a current course and updates their information"""
        if index < 0 or index >= len(json_config.scheduler_config.courses):
            raise IndexError("Course index out of range.")
        old_course = json_config.scheduler_config.courses[index]
        course_config = CourseConfig(
            course_id=course_id if course_id is not None else old_course.course_id,
            credits=course_credits
            if course_credits is not None
            else old_course.credits,
            room=room if room is not None else old_course.room,
            lab=lab if lab is not None else old_course.lab,
            conflicts=conflicts if conflicts is not None else old_course.conflicts,
            faculty=faculty if faculty is not None else old_course.faculty,
        )
        Course.check_values(
            json_config,
            course_config.course_id,
            course_config.credits,
            course_config.room,
            course_config.faculty,
            course_config.lab,
            course_config.conflicts,
        )
        old_course_id = old_course.course_id
        course_id = course_config.course_id
        if old_course_id != course_config.course_id:
            """ Update references in faculty and conflicts if the course ID has changed """
            for faculty_member in json_config.scheduler_config.faculty:
                if old_course_id in faculty_member.course_preferences:
                    faculty_member.course_preferences[course_id] = (
                        faculty_member.course_preferences.pop(old_course_id)
                    )
            for other_course in json_config.scheduler_config.courses:
                if old_course_id in other_course.conflicts:
                    other_course.conflicts.remove(old_course_id)
                    other_course.conflicts.append(course_id)
        for faculty_member in json_config.scheduler_config.faculty:
            if (
                faculty_member.name in course_config.faculty
                and course_id not in faculty_member.course_preferences
            ):
                faculty_member.course_preferences[course_id] = (
                    5  # default preference score
                )
        json_config.scheduler_config.courses[index] = course_config
        return f"Course number {index} successfully modified."

    @staticmethod
    def del_course(index: int, json_config: JsonConfig) -> str:
        """finds the course within the scheduler and removes it"""
        if index < 0 or index >= len(json_config.scheduler_config.courses):
            raise IndexError("Course index out of range.")
        course = json_config.scheduler_config.courses.pop(index)
        for faculty in json_config.scheduler_config.faculty:
            if course.course_id in faculty.course_preferences:
                faculty.course_preferences.pop(course.course_id)
        for other_course in json_config.scheduler_config.courses:
            if course.course_id in other_course.conflicts:
                other_course.conflicts.remove(course.course_id)
        return f"Course number {index} successfully deleted."

    @staticmethod
    def courses_string(json_config: JsonConfig) -> str:
        course_list = json_config.scheduler_config.courses
        courses = []
        for i, course in enumerate(course_list):
            courses.append(
                f"{i}: {course.course_id}, Credits: {course.credits}, Rooms: {course.room}, Labs: {course.lab}, Conflicts: {course.conflicts}, Faculty: {course.faculty}"
            )
        return "\n".join(courses)
