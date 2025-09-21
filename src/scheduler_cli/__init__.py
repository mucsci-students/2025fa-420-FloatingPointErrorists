from .base_cli import cli
from .courses import Course
from.faculty import Faculty
from .room import Room
from .lab import Lab
from .json import JsonConfig

__all__ = ["cli", "Course", "Faculty", "Room", "Lab", "JsonConfig"]