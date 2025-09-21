from .json import JsonConfig

class Room:
    """
    Module for handling Rooms in the config files
    """
    @staticmethod
    def add_room(json_config: JsonConfig, new_room: str) -> None:
        """Takes in a new room and adds it to the config"""
        json_config.scheduler_config.rooms.append(new_room)
        json_config.scheduler_config.rooms.sort()

    @staticmethod
    def mod_room(json_config: JsonConfig, room: str, new_room: str) -> None:
        """Takes in the name of an existing room and changes it to the new room"""
        json_config.scheduler_config.rooms[json_config.scheduler_config.rooms.index(room)] = new_room

    @staticmethod
    def del_room(json_config: JsonConfig, room: str) -> None:
        """Deletes a specified room from the config"""
        json_config.scheduler_config.rooms.remove(room)
