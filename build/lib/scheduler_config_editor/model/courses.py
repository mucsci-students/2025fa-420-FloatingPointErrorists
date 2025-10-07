from scheduler_config_editor.model.json import JsonConfig
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
        for faculty_member in json_config.scheduler_config.faculty:
            if faculty_member.name in faculty:
                faculty_member.course_preferences[course_id] = 5 # default preference score
        json_config.scheduler_config.courses.append(course_config)

    @staticmethod
    def mod_course(index: int, json_config: JsonConfig, course_id: str, course_credits: int, room: list[str], lab: list[str], conflicts: list[str], faculty: list[str]) -> None:
        """modifies a current course and updates their information"""
        old_course_id = json_config.scheduler_config.courses[index].course_id
        if old_course_id != course_id:
            """ Update references in faculty and conflicts if the course ID has changed """
            for faculty_member in json_config.scheduler_config.faculty:
                if old_course_id in faculty_member.course_preferences:
                    faculty_member.course_preferences[course_id] = faculty_member.course_preferences.pop(old_course_id)
            for other_course in json_config.scheduler_config.courses:
                if old_course_id in other_course.conflicts:
                    other_course.conflicts.remove(old_course_id)
                    other_course.conflicts.append(course_id)
        for faculty_member in json_config.scheduler_config.faculty:
            if faculty_member.name in faculty and course_id not in faculty_member.course_preferences:
                faculty_member.course_preferences[course_id] = 5  # default preference score
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
    def del_course(index: int, json_config: JsonConfig) -> None:
        """finds the course within the scheduler and removes it"""
        course = json_config.scheduler_config.courses.pop(index)
        for faculty in json_config.scheduler_config.faculty:
            if course.course_id in faculty.course_preferences:
                faculty.course_preferences.pop(course.course_id)
        for other_course in json_config.scheduler_config.courses:
            if course.course_id in other_course.conflicts:
                other_course.conflicts.remove(course.course_id)

    @staticmethod
    def courses_string(json_config: JsonConfig) -> str:
        course_list = json_config.scheduler_config.courses
        courses = []
        for i, course in enumerate(course_list):
            courses.append(f"{i}: {course.course_id}, Credits: {course.credits}, Rooms: {course.room}, Labs: {course.lab}, Conflicts: {course.conflicts}, Faculty: {course.faculty}")
        return "\n".join(courses)
