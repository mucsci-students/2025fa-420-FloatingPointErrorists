import json
from typing import Any

"""
Module for handling JSON configuration files.

It has a class JsonConfig that can load, save, and represent JSON configurations (for now).

It has fields for the file path and the configuration data itself.
"""
class JsonConfig:
    def __init__(self, file_path: str) -> None:
        self.__file_path: str = file_path
        with open(file_path, "r") as file:
            self.__config = json.load(file)

    def get_config(self) -> Any:
        return self.__config

    def get_file_path(self) -> str:
        return self.__file_path

    def save(self) -> None:
        with open(self.__file_path, "w") as file:
            json.dump(self.__config, file, indent=4)

    def __str__(self) -> str:
        cfg = self.__config["config"]
        lines = ["Rooms:"]
        for room in cfg.get("rooms", []):
            lines.append(f"  - {room}")
        lines.append("\nLabs:")
        for lab in cfg.get("labs", []):
            lines.append(f"  - {lab}")
        lines.append("\nCourses:")
        for course in cfg.get("courses", []):
            lines.append(f"  - {course['course_id']} ({course['credits']} credits)")
            lines.append(f"\tRooms: {', '.join(course['room'])}")
            if course["lab"]:
                lines.append(f"\tLabs: {', '.join(course['lab'])}")
            if course["conflicts"]:
                lines.append(f"\tConflicts: {', '.join(course['conflicts'])}")
            if course["faculty"]:
                lines.append(f"\tFaculty: {', '.join(course['faculty'])}")
        lines.append("\nFaculty:")
        for faculty in cfg.get("faculty", []):
            lines.append(f"  - {faculty['name']}")
            lines.append(f"\tCredits: {faculty['minimum_credits']}-{faculty['maximum_credits']}")
            lines.append(f"\tUnique course limit: {faculty['unique_course_limit']}")
            lines.append(f"\tTimes:")
            for day, times in faculty["times"].items():
                if times:
                    lines.append(f"\t{day}: {', '.join(times)}")
            if faculty["course_preferences"]:
                lines.append(f"\tCourse preferences: {faculty['course_preferences']}")
            if faculty["room_preferences"]:
                lines.append(f"\tRoom preferences: {faculty['room_preferences']}")
            if faculty["lab_preferences"]:
                lines.append(f"\tLab preferences: {faculty['lab_preferences']}")
        return "\n".join(lines)