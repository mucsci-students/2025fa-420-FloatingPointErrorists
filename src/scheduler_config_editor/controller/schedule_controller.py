from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QHeaderView,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from scheduler.models import CourseInstance

from scheduler_config_editor.model import ScheduleWriter, PdfWriter, PdfMode
from scheduler_config_editor.model import ScheduleHandler, INDEX_TO_DAY

# colors for classes
# (background, text)
colors = [
    ("#0066ff", "#ffffff"),  # 50% light
    ("#66a3ff", "#000000"),  # 70% light
    ("#002966", "#ffffff"),  # 20% light
    ("#0052cc", "#ffffff"),  # 40% light
    ("#33adff", "#000000"),  # 60% light
    ("#005c99", "#ffffff"),  # 30% light
    ("#99c2ff", "#000000"),  # 80% light
    ("#001433", "#ffffff"),  # 10% light
    ("#b3d1ff", "#000000"),  # 90% light
    ("#000000", "#ffffff"),  # 00% light
]


class SchedulerController:
    def __init__(self) -> None:
        self.cur_schedules = ScheduleHandler()

        self.cur_widgets = QWidget()
        self.cur_wid_layout = QVBoxLayout(self.cur_widgets)
        # seperate variable for popout window
        self.popup_widget = QWidget()
        self.popup_widget_layout = QVBoxLayout(self.popup_widget)

        # graphical variables
        self.graph_widget = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.popup_graph_widget = QWidget()
        self.popup_graph_layout = QVBoxLayout(self.popup_graph_widget)

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

    def graph_schedule(self):
        self.graph_widget = QWidget()
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.graph_layout.setSpacing(0)
        self.popup_graph_widget = QWidget()
        self.popup_graph_layout = QVBoxLayout(self.popup_graph_widget)
        self.popup_graph_layout.setSpacing(0)

        if self.mode == 1:
            graphList = ScheduleHandler.faculty_schedule_columns(
                self.cur_schedules.schedules[self.index]
            )
        else:
            graphList = ScheduleHandler.room_schedule_columns(
                self.cur_schedules.schedules[self.index]
            )

        for graph in graphList:
            match graph:
                case (graph_name, week):
                    # Create OverHeader Fac Name
                    cur_graph_name = QLabel(graph_name)
                    cur_graph_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                    cur_graph_name.setStyleSheet("font-weight: bold; font-size: 32px")
                    self.graph_layout.addWidget(cur_graph_name)
                    popup_graph_name = QLabel(graph_name)
                    popup_graph_name.setAlignment(Qt.AlignmentFlag.AlignTop)
                    popup_graph_name.setStyleSheet("font-weight: bold; font-size: 32px")
                    self.popup_graph_layout.addWidget(popup_graph_name)

                    # MAIN TABLE
                    schedule = QHBoxLayout()
                    popup_shedule = QHBoxLayout()

                    # 1st column time index
                    time_index = QVBoxLayout()
                    popup_time_index = QVBoxLayout()

                    # empty first box
                    toptimelabel = QLabel()
                    toptimelabel.setStyleSheet("border: 1px solid black")
                    toptimelabel.setFixedHeight(50)
                    time_index.addWidget(toptimelabel)
                    popup_toptimelabel = QLabel()
                    popup_toptimelabel.setStyleSheet("border: 1px solid black")
                    popup_toptimelabel.setFixedHeight(50)
                    popup_time_index.addWidget(popup_toptimelabel)

                    # find earliest start time and latest end time
                    earliest_start = None
                    latest_end = None
                    while earliest_start is None:
                        for day in week:
                            for course in day:
                                earliest_start = course.time[0]
                                latest_end = course.time[1]
                                if earliest_start is not None:
                                    break

                    for day in week:
                        for course in day:
                            if course.time[0] < earliest_start or earliest_start == 0:
                                earliest_start = course.time[0]
                            if course.time[1] > latest_end:
                                latest_end = course.time[1]

                    # round to nearest hour
                    if earliest_start % 60 != 0:
                        earliest_start -= earliest_start % 60
                    if latest_end % 60 != 0:
                        latest_end += 60 - (latest_end % 60)
                    else:
                        latest_end += 60

                    # 8am-7pm
                    for i in range(earliest_start // 60, latest_end // 60):
                        time_label = QLabel(
                            self.convert_to_timestr(self.convert_to_minutes(i * 100))
                        )
                        popup_timelabel = QLabel(
                            self.convert_to_timestr(self.convert_to_minutes(i * 100))
                        )

                        time_label.setStyleSheet("border: 1px solid black")
                        time_label.setMinimumHeight(100)
                        time_label.setAlignment(Qt.AlignmentFlag.AlignTop)
                        time_index.addWidget(time_label)

                        popup_timelabel.setStyleSheet("border: 1px solid black")
                        popup_timelabel.setMinimumHeight(100)
                        popup_timelabel.setAlignment(Qt.AlignmentFlag.AlignTop)
                        popup_time_index.addWidget(popup_timelabel)

                    schedule.addLayout(time_index)
                    popup_shedule.addLayout(popup_time_index)

                    color_index = 0

                    found_classes = []

                    # start day column
                    for idx, day in enumerate(week):
                        day_and_courses = QVBoxLayout()
                        popup_day_and_courses = QVBoxLayout()

                        # add day header
                        day_label = QLabel(INDEX_TO_DAY[idx + 1])
                        day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        day_label.setMinimumWidth(125)
                        day_label.setFixedHeight(50)
                        day_label.setStyleSheet("border: 1px solid black")
                        day_and_courses.addWidget(day_label)

                        popup_daylabel = QLabel(INDEX_TO_DAY[idx + 1])
                        popup_daylabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        popup_daylabel.setMinimumWidth(125)
                        popup_daylabel.setFixedHeight(50)
                        popup_daylabel.setStyleSheet("border: 1px solid black")
                        popup_day_and_courses.addWidget(popup_daylabel)

                        day_cousrse_spaceing = QHBoxLayout()
                        day_cousrse_spaceing.addStretch(1)
                        popup_coursespaceing = QHBoxLayout()
                        popup_coursespaceing.addStretch(1)

                        # keep track of time for stretch sizeing
                        cur_time = earliest_start

                        day_column = QVBoxLayout()
                        popup_daycolumn = QVBoxLayout()
                        # add each course
                        for courses in day:
                            # empty space before course
                            day_column.addStretch(courses.time[0] - cur_time)
                            popup_daycolumn.addStretch(courses.time[0] - cur_time)

                            # adding courses
                            content = ""
                            # faculty
                            if self.mode == 1:
                                content = f"{courses.name}\n{courses.room}\n{self.convert_to_timestr(courses.time[0])} to {self.convert_to_timestr(courses.time[1])}"
                            else:
                                content = f"{courses.name}\n{courses.faculty}\n{self.convert_to_timestr(courses.time[0])} to {self.convert_to_timestr(courses.time[1])}"
                            day_class = QLabel(content)
                            popup_day_class = QLabel(content)

                            # color code courses
                            course_color_index = color_index
                            if courses.name not in found_classes:
                                found_classes.append(courses.name)
                                color_index += 1
                                color_index %= 10
                            else:
                                course_color_index = (
                                    found_classes.index(courses.name) % 10
                                )
                                # print(course_color_index)
                            # print(course_color_index)
                            match colors[course_color_index]:
                                case (background, text):
                                    day_class.setStyleSheet(
                                        f"background-color: {background}; color: {text}; border: 1px solid black; border-radius: 5px"
                                    )
                                    popup_day_class.setStyleSheet(
                                        f"background-color: {background}; color: {text}; border: 1px solid black; border-radius: 5px"
                                    )

                            day_column.addWidget(
                                day_class, stretch=(courses.time[1] - courses.time[0])
                            )
                            popup_daycolumn.addWidget(
                                popup_day_class,
                                stretch=(courses.time[1] - courses.time[0]),
                            )

                            # update time
                            cur_time = courses.time[1]

                        # add space after last course
                        day_column.addStretch(latest_end - cur_time)
                        popup_daycolumn.addStretch(latest_end - cur_time)

                        day_cousrse_spaceing.addLayout(day_column, stretch=40)
                        day_cousrse_spaceing.addStretch(1)
                        popup_coursespaceing.addLayout(popup_daycolumn, stretch=40)
                        popup_coursespaceing.addStretch(1)

                        day_and_courses.addLayout(day_cousrse_spaceing)
                        schedule.addLayout(day_and_courses)
                        popup_day_and_courses.addLayout(popup_coursespaceing)
                        popup_shedule.addLayout(popup_day_and_courses)

                    self.graph_layout.addLayout(schedule)
                    self.popup_graph_layout.addLayout(popup_shedule)

    @staticmethod
    def convert_to_minutes(i: int) -> int:
        return i // 100 * 60 + i % 100

    @staticmethod
    def convert_to_timestr(i: int) -> str:
        m = i % 60
        h = i // 60
        # minute placeholder
        mp = ""
        # hour sufix
        hs = "AM"

        # make single digit minutes take 2 characters
        if m < 10:
            mp = "0"

        # am pm
        if h >= 12:
            h -= 12
            hs = "PM"
        if h == 0:
            h = 12
        return f"{h}:{mp}{m} {hs}"

    @staticmethod
    def save_as_json(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_json(my_schedules, name)

    @staticmethod
    def save_as_csv(my_schedules: list[list[CourseInstance]], name: str) -> None:
        ScheduleWriter.write_as_csv(my_schedules, name)

    def save_as_pdf(self, name: str) -> None:
        """Saves the current schedule as a PDF."""
        schedule = self.cur_schedules.schedules[self.index]
        mode = PdfMode.ROOM if self.mode == 2 else PdfMode.FACULTY
        PdfWriter.export_pdf(
            ScheduleHandler.room_schedule_columns(schedule)
            if mode == PdfMode.ROOM
            else ScheduleHandler.faculty_schedule_columns(schedule),
            name,
            mode,
        )
