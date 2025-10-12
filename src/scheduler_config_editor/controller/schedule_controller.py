from scheduler_config_editor.model.schedule_handler import ScheduleHandler
from scheduler_config_editor.model.run_scheduler import write_as_csv, write_as_json
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from scheduler.models import CourseInstance

class SchedulerController:

    def __init__ (self) -> None:
        self.cur_schedules = ScheduleHandler()
        self.cur_table = QTableWidget()
        self.index = 0
        self.length = 0
        # 0 = courses, 1 = faulty, 2 = rooms
        self.mode = 0
    
    def next_schedule(self) -> None:
        if self.index < self.length - 1:
            self.index = self.index + 1
        else:
            self.index = 0

    def previous_schedule(self) -> None:
        if self.index > 0:
            self.index = self.index - 1
        else:
            self.index = self.length - 1

    def set_table(self) -> None:
        self.cur_table = QTableWidget()
        
        if self.mode == 0:
            self.cur_table.setColumnCount(5)
            self.cur_table.setHorizontalHeaderLabels(["Course", "Faculty", "Room", "Lab", "Times"])
            data = ScheduleHandler.schedule_rows(self.cur_schedules.schedules[self.index])
            
        elif self.mode == 1:
            self.cur_table.setColumnCount(8)
            self.cur_table.setHorizontalHeaderLabels(["Faculty", "Course", "Room (Lab)", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            data = ScheduleHandler.faculty_schedule_rows(self.cur_schedules.schedules[self.index])

        else:
            self.cur_table.setColumnCount(8)
            self.cur_table.setHorizontalHeaderLabels(["Room", "Course", "Faculty", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            data = ScheduleHandler.room_schedule_rows(self.cur_schedules.schedules[self.index])

        for row_data in data:
            self.add_row(row_data)

    def add_row(self, rowdata: list[str]) -> None:
        row_position = self.cur_table.rowCount()
        self.cur_table.insertRow(row_position)

        for column, value in enumerate(rowdata):
            item = QTableWidgetItem(value)
            self.cur_table.setItem(row_position, column, item)


    @staticmethod
    def save_as_json(my_schedules: list[list[CourseInstance]], name: str) -> None:
        write_as_json(my_schedules, name)
    
    @staticmethod
    def save_as_csv(my_schedules: list[list[CourseInstance]], name: str) -> None:
        write_as_csv(my_schedules, name)