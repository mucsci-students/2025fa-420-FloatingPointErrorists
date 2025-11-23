from .json_config import JsonConfig


class Lab:
    """
    Module for handling Labs in the config files
    """

    @staticmethod
    def add_lab(json_config: JsonConfig, new_lab: str) -> str:
        """Takes in a new lab and adds it to the config"""
        if json_config.scheduler_config.labs.count(new_lab) == 0:
            json_config.scheduler_config.labs.append(new_lab)
            json_config.scheduler_config.labs.sort()
        else:
            raise Lab.LabExistsError(f"Lab {new_lab} already exists.")
        return f"Lab {new_lab} successfully added."

    @staticmethod
    def mod_lab(json_config: JsonConfig, lab: str, new_lab: str) -> str:
        """Takes in the name of an existing lab and changes it to the new lab"""
        if json_config.scheduler_config.labs.count(new_lab) == 1:
            raise Lab.LabExistsError(f"Lab {new_lab} already exists.")
        try:
            json_config.scheduler_config.labs[
                json_config.scheduler_config.labs.index(lab)
            ] = new_lab
            for course in json_config.scheduler_config.courses:
                if course.lab.count(lab) == 1:
                    course.lab[course.lab.index(lab)] = new_lab
                    course.lab.sort()
            for faculty_member in json_config.scheduler_config.faculty:
                if lab in faculty_member.lab_preferences:
                    faculty_member.lab_preferences[new_lab] = (
                        faculty_member.lab_preferences.pop(lab)
                    )
            json_config.scheduler_config.labs.sort()
        except ValueError:
            raise Lab.LabMissingError(f"Lab {lab} does not exist.")
        return f"Lab {lab} successfully modified to {new_lab}."

    @staticmethod
    def del_lab(json_config: JsonConfig, lab: str) -> str:
        """Deletes a specified lab from the config"""
        if json_config.scheduler_config.labs.count(lab) == 1:
            json_config.scheduler_config.labs.remove(lab)
            for course in json_config.scheduler_config.courses:
                if course.lab.count(lab) == 1:
                    course.lab.remove(lab)
            for faculty_member in json_config.scheduler_config.faculty:
                if lab in faculty_member.lab_preferences:
                    faculty_member.lab_preferences.pop(lab)
        else:
            raise Lab.LabMissingError(f"Lab {lab} does not exist.")
        return f"Lab {lab} successfully deleted."

    class LabExistsError(Exception):
        # Exception for when a lab already exists in the JSON
        pass

    class LabMissingError(Exception):
        # Exception for when a lab does not exist in the JSON
        pass
