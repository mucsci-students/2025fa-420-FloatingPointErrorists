from .json import JsonConfig
from scheduler import CourseConfig

class Course:
    """
        This class allows the user to create, modify and delete courses from the JsonConfig
    """

    @staticmethod
    def add_course(json_config: JsonConfig, course_id: str, course_credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
        """adds a new course to the config file"""
        course_config = CourseConfig(
            course_id=course_id,
            credits=course_credits,
            room=room,
            lab=lab,
            conflicts=conflicts,
            faculty=faculty
        )
        json_config.scheduler_config.courses.append(course_config)

    @staticmethod
    def mod_course(index: int, json_config: JsonConfig, course_id: str, course_credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
        """modifies a current course and updates their information"""
        course_config = CourseConfig(
            course_id=course_id,
            credits=course_credits,
            room=room,
            lab=lab,
            conflicts=conflicts,
            faculty=faculty
        )
        json_config.scheduler_config.courses[index] = course_config

    @staticmethod
    def del_course(index: int, json_config:JsonConfig) -> None:
        """finds the course within the scheduler and removes it"""
        json_config.scheduler_config.courses.pop(index)

    @staticmethod
    def courses_string(json_config: JsonConfig) -> str:
        course_list = json_config.scheduler_config.courses
        courses = []
        for i, course in enumerate(course_list):
            courses.append(f"{i}: {course.course_id}, Credits: {course.credits}, Rooms: {course.room}, Labs: {course.lab}, Conflicts: {course.conflicts}, Faculty: {course.faculty}")
        return "\n".join(courses)
