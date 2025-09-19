from .json import JsonConfig
from typing import Any
"""
Module for handling Rooms and Labs in the config files
"""
class Room:
    @staticmethod
    def add_room(json_config: JsonConfig, newRoom: str) -> None:
        json_config.rooms.append(newRoom)
        json_config.rooms.sort()

    @staticmethod
    def mod_room(json_config: JsonConfig, room: str, newRoom: str):
        json_config.rooms[json_config.rooms.index(room)] = newRoom

    @staticmethod
    def del_room(json_config: JsonConfig, room: str):
        json_config.rooms.remove(room)
