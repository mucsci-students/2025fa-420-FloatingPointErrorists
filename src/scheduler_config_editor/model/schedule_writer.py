import os
from scheduler.models import CourseInstance
from scheduler.writers import CSVWriter, JSONWriter


class ScheduleWriter:
    # write a schedule in json format to data folder
    @staticmethod
    def write_as_json(slist: list[list["CourseInstance"]], name: str) -> None:
        # make new file
        path = os.path.join("schedules", f"{name}.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, "w")
        # writing for json
        with JSONWriter(path) as writer:
            for schedule in slist:
                writer.add_schedule(schedule)
        file.close()

    # write a schedule in json format to data folder
    @staticmethod
    def write_as_csv(slist: list[list["CourseInstance"]], name: str) -> None:
        # make new file
        path = os.path.join("schedules", f"{name}.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, "w")
        # writing for csv
        with CSVWriter(path) as writer:
            for schedule in slist:
                writer.add_schedule(schedule)
        file.close()
