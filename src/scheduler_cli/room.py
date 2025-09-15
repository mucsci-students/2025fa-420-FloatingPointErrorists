from .json import JsonConfig
from typing import Any
"""
Module for handling Rooms and Labs in the config files
"""
class Room:
    def __init__(self, config: Any, room: list[str]) -> None:
        self._config = config
        self._room = room

    def get_room(self) -> list[str]:
        return self._room
    
    def add_room(self, newRoom: str):
        self._room.append(newRoom)

    #def set_room(self, )

    #def del_room(self):
