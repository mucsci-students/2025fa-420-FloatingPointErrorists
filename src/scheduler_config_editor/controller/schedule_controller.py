from scheduler_config_editor.model.schedule_handler import ScheduleHandler
from scheduler_config_editor.model.run_scheduler import write_as_csv, write_as_json
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QScrollArea, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from scheduler.models import CourseInstance

from scheduler_config_editor.model import ScheduleWriter
from scheduler_config_editor.model import ScheduleHandler


class SchedulerController:
    def __init__(self) -> None:
        self.cur_schedules = ScheduleHandler()
        self.cur_tables = QVBoxLayout()
        self.cur_table = QTableWidget()
        self.index = 0
        self.length = 0
        # 0 = courses, 1 = faulty, 2 = rooms
        self.mode = 0

    def reset_index(self) -> None:
        self.index = 0

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

    def set_tables(self) -> None:
        self.cur_table = QTableWidget()

        if self.mode == 0:
            self.cur_table.setColumnCount(5)
            self.cur_table.setHorizontalHeaderLabels(
                ["Course", "Faculty", "Room", "Lab", "Times"]
            )
            data = ScheduleHandler.schedule_rows(
                self.cur_schedules.schedules[self.index]
            )

            self.pop_add_cur_table(data)


        elif self.mode == 1:
            self.cur_table.setColumnCount(7)
            self.cur_table.setHorizontalHeaderLabels(
                [
                    "Course",
                    "Room (Lab)",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ]
            )
            dataList = ScheduleHandler.faculty_schedule_rows(
                self.cur_schedules.schedules[self.index]
            )
            for dataset in dataList:
                match dataset:
                    case (fac_name, data):

                        temp_fac_name = QLabel()
                        temp_fac_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        temp_fac_name.setText(fac_name)
                        self.cur_tables.addWidget(temp_fac_name)

                        self.pop_add_cur_table(data)

        else:
            self.cur_table.setColumnCount(7)
            self.cur_table.setHorizontalHeaderLabels(
                [
                    "Course",
                    "Faculty",
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                ]
            )
            dataList = ScheduleHandler.room_schedule_rows(
                self.cur_schedules.schedules[self.index]
            )
            for dataset in dataList:
                match dataset:
                    case (room_name, data):

                        temp_room_name = QLabel()
                        temp_room_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        temp_room_name.setText(room_name)
                        self.cur_tables.addWidget(temp_room_name)

                        self.pop_add_cur_table(data)

    def pop_add_cur_table(self, data) -> None:
        self.cur_table = QTableWidget()

        for row_data in data:
            self.add_row(row_data)

        self.cur_tables.addWidget(self.cur_table)

        self.cur_table.resizeColumnsToContents()
        self.cur_table.resizeRowsToContents()


    def add_row(self, rowdata: list[str]) -> None:
        row_position = self.cur_table.rowCount()
        self.cur_table.insertRow(row_position)

        for column, value in enumerate(rowdata):
            item = QTableWidgetItem(value)
            self.cur_table.setItem(row_position, column, item)

    @staticmethod
    def save_as_json(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_json(my_schedules, name)

    @staticmethod
    def save_as_csv(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_csv(my_schedules, name)
