from .json import JsonConfig

class Room:
    """
    Module for handling Rooms in the config files
    """
    @staticmethod
    def add_room(json_config: JsonConfig, new_room: str) -> None:
        """Takes in a new room and adds it to the config"""
        if json_config.scheduler_config.rooms.count(new_room) == 0:
            json_config.scheduler_config.rooms.append(new_room)
            json_config.scheduler_config.rooms.sort()
        else:
            raise ValueError(f"Room {new_room} already exists.")

    @staticmethod
    def mod_room(json_config: JsonConfig, room: str, new_room: str) -> None:
        """Takes in the name of an existing room and changes it to the new room"""
        json_config.scheduler_config.rooms[json_config.scheduler_config.rooms.index(room)] = new_room
        for course in json_config.scheduler_config.courses:
            if course.room.count(room) == 1:
                course.room[course.room.index(room)] = new_room
                course.room.sort()
        for faculty_member in json_config.scheduler_config.faculty:
            if room in faculty_member.room_preferences:
                faculty_member.room_preferences[new_room] = faculty_member.room_preferences.pop(room)
        json_config.scheduler_config.rooms.sort()

    @staticmethod
    def del_room(json_config: JsonConfig, room: str) -> None:
        """Deletes a specified room from the config"""
        json_config.scheduler_config.rooms.remove(room)
        for course in json_config.scheduler_config.courses:
            if course.room.count(room) == 1:
                course.room.remove(room)
        for faculty_member in json_config.scheduler_config.faculty:
            if room in faculty_member.room_preferences:
                faculty_member.room_preferences.pop(room)
