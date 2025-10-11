from .json import JsonConfig

class Lab:
    """
    Module for handling Labs in the config files
    """
    @staticmethod
    def add_lab(json_config: JsonConfig, new_lab: str) -> None:
        """Takes in a new lab and adds it to the config"""
        if json_config.scheduler_config.labs.count(new_lab) == 0:
            json_config.scheduler_config.labs.append(new_lab)
            json_config.scheduler_config.labs.sort()
        else:
            raise ValueError(f"Lab {new_lab} already exists.")

    @staticmethod
    def mod_lab(json_config: JsonConfig, lab: str, new_lab: str) -> None:
        """Takes in the name of an existing lab and changes it to the new lab"""
        json_config.scheduler_config.labs[json_config.scheduler_config.labs.index(lab)] = new_lab
        for course in json_config.scheduler_config.courses:
            if course.lab.count(lab) == 1:
                course.lab[course.lab.index(lab)] = new_lab
                course.lab.sort()
        for faculty_member in json_config.scheduler_config.faculty:
            if lab in faculty_member.lab_preferences:
                faculty_member.lab_preferences[new_lab] = faculty_member.labs_preferences.pop(lab)
        json_config.scheduler_config.labs.sort()

    @staticmethod
    def del_lab(json_config: JsonConfig, lab: str) -> None:
        """Deletes a specified lab from the config"""
        json_config.scheduler_config.labs.remove(lab)
        for course in json_config.scheduler_config.courses:
            if course.lab.count(lab) == 1:
                course.lab.remove(lab)
        for faculty_member in json_config.scheduler_config.faculty:
            if lab in faculty_member.lab_preferences:
                faculty_member.lab_preferences.pop(lab)
