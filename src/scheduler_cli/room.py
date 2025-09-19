from .json import JsonConfig
from typing import Any
"""
Module for handling Rooms and Labs in the config files
"""
class Room:
    @staticmethod
    def add_room(json_config: JsonConfig, newRoom: str) -> None:
        """Takes in a new room and adds it to the config"""
        json_config.scheduler_config.rooms.append(newRoom)
        json_config.scheduler_config.rooms.sort()

    @staticmethod
    def mod_room(json_config: JsonConfig, room: str, newRoom: str) -> None:
        """Takes in the name of an existing room and changes it to the new room"""
        json_config.scheduler_config.rooms[json_config.rooms.index(room)] = newRoom

    @staticmethod
    def del_room(json_config: JsonConfig, room: str) -> None:
        """Deletes a specified room from the config"""
        json_config.scheduler_config.rooms.remove(room)
