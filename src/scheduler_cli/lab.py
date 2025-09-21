from .json import JsonConfig

class Lab:
    """
    Module for handling Labs in the config files
    """
    @staticmethod
    def add_lab(json_config: JsonConfig, new_lab: str) -> None:
        """Takes in a new lab and adds it to the config"""
        json_config.scheduler_config.labs.append(new_lab)
        json_config.scheduler_config.labs.sort()

    @staticmethod
    def mod_lab(json_config: JsonConfig, lab: str, new_lab: str) -> None:
        """Takes in the name of an existing lab and changes it to the new lab"""
        json_config.scheduler_config.labs[json_config.scheduler_config.labs.index(lab)] = new_lab

    @staticmethod
    def del_lab(json_config: JsonConfig, lab: str) -> None:
        """Deletes a specified lab from the config"""
        json_config.scheduler_config.labs.remove(lab)
