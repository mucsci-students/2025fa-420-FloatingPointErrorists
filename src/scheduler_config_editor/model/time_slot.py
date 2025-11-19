from scheduler import TimeSlotConfig, TimeBlock, ClassPattern, Meeting
from scheduler_config_editor.model import JsonConfig


class TimeSlot:
    """
    This class allows the user to create, modify and delete a time slots from the JsonConfig
    """

    @staticmethod
    def check_values(json_config: JsonConfig, times: dict[str, list[TimeBlock]], classes: list[ClassPattern], max_time_gap: int, min_time_overlap: int) -> None:
        """ Checks that the provided values are valid """
        if not times:
            raise ValueError("Times cannot be empty.")
        if not classes:
            raise ValueError("Classes cannot be empty.")
        if max_time_gap < 0:
            raise ValueError("The maximum time gap must be greater than or equal to 0.")
        if min_time_overlap <= 0:
            raise ValueError("The minimum time overlap must be greater than 0.")



    @staticmethod
    def add_time_slot(json_config: JsonConfig, times: dict[str, list[TimeBlock]], classes: list[ClassPattern], max_time_gap: int=30, min_time_overlap: int=45) -> str:
        """ Adds a time slot to the config """
        TimeSlot.check_values(json_config, times, classes, max_time_gap, min_time_overlap)

        # Converting times into a dict of time blocks

        time_slot_config = TimeSlotConfig(times=times, classes=classes, max_time_gap=max_time_gap, min_time_overlap=min_time_overlap)
        json_config.time_slot_config.append(time_slot_config)
        return "Time slot added successfully."

    @staticmethod
    def mod_time_slot(index: int, json_config: JsonConfig, times: dict[str, list[TimeBlock]], classes: list[ClassPattern], max_time_gap: int=30, min_time_overlap: int=45) -> str:
        """ Finds time slot in config and replaces it with the updated one """
        if index < 0 or index >= len(json_config.time_slot_config):
            raise IndexError("Time Slot index out of range.")
        old_time_slot = json_config.time_slot_config[index]
        time_slot = TimeSlotConfig(
            times=times if times is not None else old_time_slot.times,
            classes=classes if classes is not None else old_time_slot.classes,
            max_time_gap=max_time_gap if max_time_gap is not None else old_time_slot.max_time_gap,
            min_time_overlap=min_time_overlap if min_time_overlap is not None else old_time_slot.min_time_overlap,
        )
        TimeSlot.check_values(
            json_config,
            time_slot.times,
            time_slot.classes,
            time_slot.max_time_gap,
            time_slot.min_time_overlap,
        )

        json_config.time_slot_config[index] = time_slot
        return ("Time slot updated successfully.")

    @staticmethod
    def del_time_slot(json_config: JsonConfig, index:int) -> str:
        """ Deletes a time slot from the config """
        if index < 0 or index >= len(json_config.time_slot_config):
            return "Time slot index out of range."

        del json_config.time_slot_config[index]
        return "Time slot deleted successfully."