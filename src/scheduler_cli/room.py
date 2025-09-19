from .json import JsonConfig
from typing import Any
"""
Module for handling Rooms and Labs in the config files
"""
class Room:
    def add_room(json_config: JsonConfig, newRoom: str) -> None:
        json_config.rooms.append(newRoom)
        json_config.rooms.sort()

    def mod_room(json_config: JsonConfig, room: str, newRoom: str):
        json_config.rooms[json_config.rooms.index(room)] = newRoom


    def del_room(json_config: JsonConfig, room: str):
        json_config.rooms.remove(room)
