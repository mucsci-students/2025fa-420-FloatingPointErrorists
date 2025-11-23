import os
import signal
from enum import Enum
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QApplication
from scheduler_config_editor.model import INDEX_TO_DAY
from scheduler_config_editor.model.schedule_handler import CourseMeeting

_app = QApplication.instance()


def get_app():
    """Get or create the QApplication instance. Uses singleton to ensure only one instance exists."""
    global _app
    if _app is None:
        _app = QApplication([])
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    return _app


class PdfMode(Enum):
    """Modes for PDF schedule export."""

    FACULTY = "faculty"
    ROOM = "room"


class PdfWriter:
    """Class for exporting schedules to PDF files."""

    @staticmethod
    def _graph_schedule(
        mode: PdfMode, week: list[list[CourseMeeting]], name: str
    ) -> QWidget:
        """Create a graphical representation of the schedule."""
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        graph_layout.setSpacing(0)

        # Header
        graph_name = QLabel(name)
        graph_name.setAlignment(Qt.AlignmentFlag.AlignTop)
        graph_name.setStyleSheet("font-size: 24px; font-weight: bold;")
        graph_layout.addWidget(graph_name)

        # Table Layout
        schedule = QHBoxLayout()
        graph_layout.addLayout(schedule)
        schedule.setSpacing(0)

        # Time Column
        time_index = QVBoxLayout()
        top_label = QLabel()
        top_label.setStyleSheet("border: 1px solid black;")
        top_label.setFixedHeight(50)
        time_index.addWidget(top_label)

        for hour in range(8, 21):
            time_label = QLabel(
                PdfWriter._convert_to_timestr(
                    PdfWriter._convert_to_minutes(hour * 100)
                )
            )
            time_label.setStyleSheet(
                "border: 1px solid black; font-size: 16px; font-weight: bold;"
            )
            time_label.setMinimumHeight(100)
            time_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            time_index.addWidget(time_label)

        schedule.addLayout(time_index)

        # Colors
        colors = [
            ("#0066ff", "#ffffff"),  # 50% light
            ("#0052cc", "#ffffff"),  # 40% light
            ("#33adff", "#000000"),  # 60% light
            ("#005c99", "#ffffff"),  # 30% light
            ("#66a3ff", "#000000"),  # 70% light
            ("#002966", "#ffffff"),  # 20% light
            ("#99c2ff", "#000000"),  # 80% light
            ("#001433", "#ffffff"),  # 10% light
            ("#b3d1ff", "#000000"),  # 90% light
            ("#000000", "#ffffff"),  # 00% light
        ]
        found_classes = []
        # Day Columns
        for idx, day in enumerate(week):
            day_container = QVBoxLayout()
            day_label = QLabel(INDEX_TO_DAY[idx + 1])
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            day_label.setFixedHeight(50)
            day_label.setMinimumWidth(125)
            day_label.setStyleSheet(
                "border: 1px solid black; font-size: 16px; font-weight: bold;"
            )
            day_container.addWidget(day_label)
            cur_time = PdfWriter._convert_to_minutes(800)
            day_column = QVBoxLayout()

            # Render courses in order
            for course in day:
                # Blank space before course
                day_column.addStretch(course.time[0] - cur_time)

                # Course widget
                if mode == PdfMode.FACULTY:
                    content = (
                        f"{course.name}\n{course.room}\n"
                        f"{PdfWriter._convert_to_timestr(course.time[0])} to "
                        f"{PdfWriter._convert_to_timestr(course.time[1])}"
                    )
                else:
                    content = (
                        f"{course.name}\n{course.faculty}\n"
                        f"{PdfWriter._convert_to_timestr(course.time[0])} to "
                        f"{PdfWriter._convert_to_timestr(course.time[1])}"
                    )

                block = QLabel(content)

                # Consistent color assignment
                if course.name not in found_classes:
                    found_classes.append(course.name)
                bg, fg = colors[found_classes.index(course.name)]

                block.setStyleSheet(
                    f"background-color: {bg}; color: {fg}; "
                    f"border: 1px solid black; border-radius: 5px;"
                    f"font-size: 16px; font-weight: bold;"
                )

                # Height based on duration
                stretch = course.time[1] - course.time[0]
                day_column.addWidget(block, stretch=stretch)

                cur_time = course.time[1]

            # Space after last course
            day_column.addStretch(
                PdfWriter._convert_to_minutes(2000) - cur_time
            )

            day_container.addLayout(day_column)
            schedule.addLayout(day_container)

        return graph_widget

    @staticmethod
    def _convert_to_minutes(i: int) -> int:
        return i // 100 * 60 + i % 100

    @staticmethod
    def _convert_to_timestr(i: int) -> str:
        m = i % 60
        h = i // 60
        # minute placeholder
        mp = ""
        # hour suffix
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
    def _export_to_pdf(schedule: list[QWidget], name: str) -> None:
        """Export the given schedule widgets to a PDF file."""
        path = os.path.join("schedulePDFs", f"{name}.pdf")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(path)
        painter = QPainter()
        painter.begin(printer)
        first_page = True
        for widget in schedule:
            widget.resize(1100, 1600)
            if not first_page:
                printer.newPage()
            first_page = False
            page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            scale_x = page_rect.width() / widget.width()
            scale_y = page_rect.height() / widget.height()
            scale = max(scale_x, scale_y)
            painter.save()
            painter.scale(scale, scale)
            widget.render(painter)
            painter.restore()
        painter.end()

    @staticmethod
    def export_graph_pdf(
        schedule: list[tuple[str, list[list[CourseMeeting]]]],
        output_path: str,
        mode: PdfMode,
    ) -> None:
        """Export the schedule as a graphical PDF."""
        get_app()  # Ensure QApplication is initialized because the PdfWriter uses Qt widgets
        widgets = []
        for name, week in schedule:
            widget = PdfWriter._graph_schedule(mode, week, name)
            widgets.append(widget)
        PdfWriter._export_to_pdf(widgets, output_path)
