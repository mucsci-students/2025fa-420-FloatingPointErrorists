from .json_config import JsonConfig


class Room:
    """
    Module for handling Rooms in the config files
    """

    @staticmethod
    def add_room(json_config: JsonConfig, new_room: str) -> str:
        """Takes in a new room and adds it to the config"""
        if json_config.scheduler_config.rooms.count(new_room) == 0:
            json_config.scheduler_config.rooms.append(new_room)
            json_config.scheduler_config.rooms.sort()
        else:
            raise Room.RoomExistsError(f"Room {new_room} already exists.")
        return f"Room {new_room} successfully added."

    @staticmethod
    def mod_room(json_config: JsonConfig, room: str, new_room: str) -> str:
        """Takes in the name of an existing room and changes it to the new room"""
        if json_config.scheduler_config.rooms.count(new_room) == 1:
            raise Room.RoomExistsError(f"Room {new_room} already exists.")
        try:
            json_config.scheduler_config.rooms[
                json_config.scheduler_config.rooms.index(room)
            ] = new_room
            for course in json_config.scheduler_config.courses:
                if course.room.count(room) == 1:
                    course.room[course.room.index(room)] = new_room
                    course.room.sort()
            for faculty_member in json_config.scheduler_config.faculty:
                if room in faculty_member.room_preferences:
                    faculty_member.room_preferences[new_room] = (
                        faculty_member.room_preferences.pop(room)
                    )
            json_config.scheduler_config.rooms.sort()
        except ValueError:
            raise Room.RoomMissingError(f"Room {room} does not exist.")
        return f"Room {room} successfully modified to {new_room}."

    @staticmethod
    def del_room(json_config: JsonConfig, room: str) -> str:
        """Deletes a specified room from the config"""
        if json_config.scheduler_config.rooms.count(room) == 1:
            json_config.scheduler_config.rooms.remove(room)
            for course in json_config.scheduler_config.courses:
                if course.room.count(room) == 1:
                    course.room.remove(room)
            for faculty_member in json_config.scheduler_config.faculty:
                if room in faculty_member.room_preferences:
                    faculty_member.room_preferences.pop(room)
        else:
            raise Room.RoomMissingError(f"Room {room} does not exist.")
        return f"Room {room} successfully deleted."

    class RoomExistsError(Exception):
        # Exception for when a room already exists in the JSON
        pass

    class RoomMissingError(Exception):
        # Exception for when a room does not exist in the JSON
        pass
