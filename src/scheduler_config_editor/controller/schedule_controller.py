from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from scheduler.models import CourseInstance

from scheduler_config_editor.model import ScheduleWriter
from scheduler_config_editor.model import ScheduleHandler


class SchedulerController:
    def __init__(self) -> None:
        self.cur_schedules = ScheduleHandler()

        self.cur_widgets = QWidget()
        self.cur_wid_layout = QVBoxLayout(self.cur_widgets)
        # seperate variable for popout window
        self.popup_widget = QWidget()
        self.popup_widget_layout = QVBoxLayout(self.popup_widget)

        self.cur_table = QTableWidget()
        self.popup_table = QTableWidget()
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
        self.cur_widgets = QWidget()
        self.cur_wid_layout = QVBoxLayout(self.cur_widgets)
        self.popup_widget = QWidget()
        self.popup_widget_layout = QVBoxLayout(self.popup_widget)

        if self.mode == 0:
            self.cur_table = QTableWidget()
            self.popup_table = QTableWidget()

            data = ScheduleHandler.schedule_rows(
                self.cur_schedules.schedules[self.index]
            )

            self.cur_table.setColumnCount(5)
            self.cur_table.setHorizontalHeaderLabels(
                ["Course", "Faculty", "Room", "Lab", "Times"]
            )
            self.popup_table.setColumnCount(5)
            self.popup_table.setHorizontalHeaderLabels(
                ["Course", "Faculty", "Room", "Lab", "Times"]
            )

            self.pop_add_cur_table(data)

        elif self.mode == 1:
            dataList = ScheduleHandler.faculty_schedule_rows(
                self.cur_schedules.schedules[self.index]
            )

            for dataset in dataList:
                match dataset:
                    case (fac_name, data):
                        temp_fac_name = QLabel()
                        temp_fac_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        temp_fac_name.setText(fac_name)
                        pop_temp_fac_name = QLabel()
                        pop_temp_fac_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        pop_temp_fac_name.setText(fac_name)

                        self.cur_wid_layout.addWidget(temp_fac_name)
                        self.popup_widget_layout.addWidget(pop_temp_fac_name)

                        self.cur_table = QTableWidget()
                        self.popup_table = QTableWidget()

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
                        self.popup_table.setColumnCount(7)
                        self.popup_table.setHorizontalHeaderLabels(
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

                        self.pop_add_cur_table(data)

        else:
            dataList = ScheduleHandler.room_schedule_rows(
                self.cur_schedules.schedules[self.index]
            )
            for dataset in dataList:
                match dataset:
                    case (room_name, data):
                        temp_room_name = QLabel()
                        temp_room_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        temp_room_name.setText(room_name)
                        pop_temp_room_name = QLabel()
                        pop_temp_room_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                        pop_temp_room_name.setText(room_name)

                        self.cur_wid_layout.addWidget(temp_room_name)
                        self.popup_widget_layout.addWidget(pop_temp_room_name)

                        self.cur_table = QTableWidget()
                        self.popup_table = QTableWidget()

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
                        self.popup_table.setColumnCount(7)
                        self.popup_table.setHorizontalHeaderLabels(
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

                        self.pop_add_cur_table(data)

    def pop_add_cur_table(self, data: list[list[str]]) -> None:
        for row_data in data:
            self.add_row(row_data)

        self.cur_table.resizeColumnsToContents()
        self.cur_table.resizeRowsToContents()
        self.popup_table.resizeColumnsToContents()
        self.popup_table.resizeRowsToContents()

        total_height = 0
        hor_header = self.cur_table.horizontalHeader()
        if hor_header is not None:
            total_height += hor_header.height()
        for i in range(self.cur_table.rowCount()):
            total_height += self.cur_table.rowHeight(i)
        total_height += self.cur_table.frameWidth() * 2

        total_width = 0
        for i in range(self.cur_table.columnCount()):
            total_width += self.cur_table.columnWidth(i)
        total_width += self.cur_table.frameWidth() * 2

        # get the width of the stupid vertical index thats not considered a vertical header
        digits = len(str(self.cur_table.model().rowCount()))
        metrics = QFontMetrics(self.cur_table.font())
        total_width += (
            metrics.horizontalAdvance("9" * digits) + 10
        )  # 10 is width of whitespace 5 behind, 5 in front

        self.cur_table.setFixedHeight(total_height)
        self.cur_table.setFixedWidth(total_width)
        self.popup_table.setFixedHeight(total_height)
        self.popup_table.setFixedWidth(total_width)

        self.cur_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self.cur_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self.popup_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self.popup_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self.cur_table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.popup_table.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )

        self.cur_wid_layout.addWidget(self.cur_table)
        self.popup_widget_layout.addWidget(self.popup_table)

    def add_row(self, rowdata: list[str]) -> None:
        row_position = self.cur_table.rowCount()
        self.cur_table.insertRow(row_position)
        self.popup_table.insertRow(row_position)

        for column, value in enumerate(rowdata):
            item = QTableWidgetItem(value)
            pop_item = QTableWidgetItem(value)
            self.cur_table.setItem(row_position, column, item)
            self.popup_table.setItem(row_position, column, pop_item)

    @staticmethod
    def save_as_json(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_json(my_schedules, name)

    @staticmethod
    def save_as_csv(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_csv(my_schedules, name)
