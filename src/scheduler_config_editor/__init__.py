from cli.base_cli import cli
from model.courses import Course
from model.faculty import Faculty
from model.room import Room
from model.lab import Lab
from model.json import JsonConfig

__all__ = ["cli", "Course", "Faculty", "Room", "Lab", "JsonConfig"]