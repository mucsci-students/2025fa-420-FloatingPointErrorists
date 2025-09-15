from .json import JsonConfig
from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig
from typing import Any

class courses: 
    def __init__(self, JsonConfig: JsonConfig):
        self._json_config = JsonConfig
        self._course_id = course_config.course_id
        self._credits = course_config.credits
        self._room = course_config.room
        self._lab = course_config.lab
        self._conflicts = course_config.conflicts
        self._faculty = course_config.faculty

    def get_course_id(self) -> str:
        return self._course_id

    def get_credits(self) -> int:
        return self._credits
    
    def get_room(self) -> list[str]:
        return self._room
    
    def get_lab(self) -> list[str]:
        return self._lab
    
    def get_conflicts(self) -> list[str]:
        return self._conflicts
    
    def get_faculty(self) -> list[str]:
        return self._faculty
    
    def del_course(self) -> None:
        self._config = None
        self._course_id = None
        self._credits = None
        self._room = None
        self._lab = None
        self._conflicts = None
        self._faculty = None


        