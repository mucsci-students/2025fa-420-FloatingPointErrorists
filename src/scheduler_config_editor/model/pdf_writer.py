from PyQt6.QtCore import Qt, QMarginsF
from PyQt6.QtGui import QPainter, QPageLayout
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication

from scheduler_config_editor.controller.schedule_controller import SchedulerController
from scheduler_config_editor.model import INDEX_TO_DAY
from scheduler_config_editor.model.schedule_handler import CourseMeeting


class PdfWriter:

    @staticmethod
    def graph_schedule(mode: int, week: list[list[CourseMeeting]], name: str) -> QWidget:
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        graph_layout.setSpacing(0)

        # Header
        cur_graph_name = QLabel(name)
        cur_graph_name.setAlignment(Qt.AlignmentFlag.AlignTop)
        graph_layout.addWidget(cur_graph_name)

        # MAIN TABLE LAYOUT
        schedule = QHBoxLayout()
        graph_layout.addLayout(schedule)
        graph_layout.setContentsMargins(0, 0, 0, 0)
        schedule.setContentsMargins(0, 0, 0, 0)
        schedule.setSpacing(0)

        # --- LEFT TIME COLUMN ---
        time_index = QVBoxLayout()

        top_label = QLabel()
        top_label.setStyleSheet("border: 1px solid black;")
        top_label.setFixedHeight(50)
        time_index.addWidget(top_label)

        for hour in range(8, 20):
            time_label = QLabel(
                SchedulerController.convert_to_timestr(
                    SchedulerController.convert_to_minutes(hour * 100)
                )
            )
            time_label.setStyleSheet("border: 1px solid black;")
            time_label.setMinimumHeight(100)
            time_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            time_index.addWidget(time_label)

        schedule.addLayout(time_index)

        # --- COLORS ---
        colors = [
            ("red", "white"), ("blue", "white"),
            ("yellow", "black"), ("purple", "white"),
            ("green", "white"), ("orange", "black"),
            ("pink", "black"), ("lightblue", "black"),
            ("limegreen", "black"), ("lightgray", "black"),
            ("cyan", "black"), ("black", "white"),
        ]
        found_classes = []
        # --- DAY COLUMNS ---
        for idx, day in enumerate(week):
            day_container = QVBoxLayout()

            # Day header label
            day_label = QLabel(INDEX_TO_DAY[idx + 1])
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setFixedHeight(50)
            day_label.setMinimumWidth(125)
            day_label.setStyleSheet("border: 1px solid black;")
            day_container.addWidget(day_label)

            cur_time = SchedulerController.convert_to_minutes(800)

            day_column = QVBoxLayout()

            # Render courses in order
            for course in day:
                # Blank space before course
                day_column.addStretch(course.time[0] - cur_time)

                # Course widget
                if mode == 1:
                    content = f"{course.name}\n{course.room}\n" \
                              f"{SchedulerController.convert_to_timestr(course.time[0])} to " \
                              f"{SchedulerController.convert_to_timestr(course.time[1])}"
                else:
                    content = f"{course.name}\n{course.faculty}\n" \
                              f"{SchedulerController.convert_to_timestr(course.time[0])} to " \
                              f"{SchedulerController.convert_to_timestr(course.time[1])}"

                block = QLabel(content)

                # Consistent color assignment
                if course.name not in found_classes:
                    found_classes.append(course.name)
                    color_index = len(found_classes) % len(colors)

                bg, fg = colors[found_classes.index(course.name)]

                block.setStyleSheet(
                    f"background-color: {bg}; color: {fg}; "
                    f"border: 1px solid black; border-radius: 5px;"
                )

                # Height based on duration
                stretch = course.time[1] - course.time[0]
                day_column.addWidget(block, stretch=stretch)

                cur_time = course.time[1]

            # Space after last course
            day_column.addStretch(
                SchedulerController.convert_to_minutes(2000) - cur_time
            )

            day_container.addLayout(day_column)
            schedule.addLayout(day_container)

        return graph_widget

    # ----------------------------------------------------------------------
    # PDF EXPORT
    # ----------------------------------------------------------------------
    @staticmethod
    def export_room_schedule(
            schedule: list[tuple[str, list[list[CourseMeeting]]]],
            output_path: str
    ):
        # Ensure a QApplication exists
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)

        painter = QPainter()
        printer.setResolution(600)
        painter.begin(printer)

        first_page = True

        for room_name, week in schedule:

            widget = PdfWriter.graph_schedule(1, week, room_name)
            widget.resize(1100, 1600)

            if not first_page:
                printer.newPage()
            first_page = False

            # ------- FIX: use correct unit ------
            page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            # -------------------------------------

            scale_x = page_rect.width() / widget.width()
            scale_y = page_rect.height() / widget.height()
            scale = max(scale_x, scale_y)

            painter.save()
            painter.scale(scale, scale)
            widget.render(painter)
            painter.restore()

        painter.end()

