import sys
from typing import TYPE_CHECKING, cast, Literal
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QComboBox,
    QSplitter,
    QListWidgetItem,
    QDialog,
    QLineEdit,
    QMessageBox,
)
from scheduler import Meeting

if TYPE_CHECKING:
    from scheduler_config_editor.controller.time_slot_controller import (
        TimeSlotController,
    )

sys.path.append("../controller")

Day = Literal["MON", "TUE", "WED", "THU", "FRI"]
DAYS: tuple[Day, ...] = ("MON", "TUE", "WED", "THU", "FRI")
DAY_TO_INDEX: dict[str, int] = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}


def normalize_time(time: str) -> str | None:
    """
    Validates if the given entry could be a time.
    Normalize a time to HH:MM format.
    """
    time = time.strip()
    if ":" in time:
        parts = time.split(":")
        if len(parts) != 2:
            return None

        hour, minute = parts
        if not hour.isdigit() or not minute.isdigit():
            return None
        hour = int(hour)
        minute = int(minute)
    else:
        if not time.isdigit():
            return None
        hour, minute = int(time), 0
    return f"{hour:02d}:{minute:02d}"


class TimeSlotEditorGui(QMainWindow):
    """
    This class provides a visual display of what is in the time slot config. Users can click add to open an editable
    window to add new time blocks and class patterns. Users can also click on the time block indexes or class pattern
    indexes to open an editable window to modify each one. Users can also delete time blocks or class patterns in this
    editable view as well.
    """

    def __init__(self, controller: "TimeSlotController", parent=None) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config

        # Window title and modality
        self.setWindowTitle("Time Slot Editor")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Layout Stuff
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
        else:
            screen_width = 1920
            screen_height = 1080
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Top layout of day selector and min_overlap and max_gap
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # Day selector for time blocks
        day_layout = QHBoxLayout()
        top_layout.addLayout(day_layout)
        top_layout.addStretch(1)

        day_layout.addWidget(QLabel("Select Time Block Day:"))
        self.day_selector = QComboBox()
        self.day_selector.addItems(["MON", "TUE", "WED", "THU", "FRI"])
        day_layout.addWidget(self.day_selector)

        # Refreshes time blocks when a new day is selected
        self.day_selector.currentTextChanged.connect(self.load_time_blocks_for_day)

        # Add editing spaces for max_time_gap and min_time_overlap and populating based on current values
        min_max_layout = QHBoxLayout()
        top_layout.addLayout(min_max_layout)

        min_max_layout.addWidget(QLabel("Minimum Time Overlap:"))
        self.input_min_overlap = QLineEdit()
        min_max_layout.addWidget(self.input_min_overlap)

        min_max_layout.addWidget(QLabel("Maximum Time Gap:"))
        self.input_max_gap = QLineEdit()
        min_max_layout.addWidget(self.input_max_gap)

        self.input_min_overlap.setText(
            str(self.json_config.time_slot_config.min_time_overlap)
        )
        self.input_max_gap.setText(str(self.json_config.time_slot_config.max_time_gap))

        self.input_min_overlap.returnPressed.connect(self.save_min_max_inputs)
        self.input_min_overlap.editingFinished.connect(self.save_min_max_inputs)

        self.input_max_gap.returnPressed.connect(self.save_min_max_inputs)
        self.input_max_gap.editingFinished.connect(self.save_min_max_inputs)

        # Splitting the window into two panels, one for time blocks and one for class patterns
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Time block panel layout (left side)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Time Blocks"))

        self.blocks_list = QListWidget()
        self.blocks_list.clicked.connect(self.on_time_block_clicked)
        left_layout.addWidget(self.blocks_list)

        add_block_button = QPushButton("Add Time Block")
        add_block_button.clicked.connect(self.add_time_block_clicked)
        left_layout.addWidget(add_block_button)

        # Class pattern panel layout (right side)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Class Patterns"))

        self.class_list = QListWidget()
        self.class_list.clicked.connect(self.on_class_pattern_clicked)
        right_layout.addWidget(self.class_list)

        add_class_button = QPushButton("Add Class Pattern")
        add_class_button.clicked.connect(self.add_class_pattern_clicked)
        right_layout.addWidget(add_class_button)

        # Populate class patterns into the list
        for i, class_pattern in enumerate(self.controller.get_class_patterns()):
            self.class_list.addItem(QListWidgetItem(f"[{i}] {class_pattern}"))

        # Adding panels to the splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

    def save_min_max_inputs(self):
        min_overlap = self.input_min_overlap.text().strip()
        max_gap = self.input_max_gap.text().strip()
        if not min_overlap.isdigit():
            QMessageBox.warning(
                self, "Invalid Input", "Min overlap must be an integer."
            )
            return
        if not max_gap.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Max gap must be a number.")
            return

        min_overlap = int(min_overlap)
        max_gap = int(max_gap)
        self.json_config.time_slot_config.min_time_overlap = min_overlap
        self.json_config.time_slot_config.max_time_gap = max_gap
        self.json_config.save()

    def load_time_blocks_for_day(self, day: str) -> None:
        """Populates the list of time blocks for the day selected."""
        self.blocks_list.clear()
        blocks = self.controller.get_time_blocks(day)
        for i, block in enumerate(blocks):
            item = QListWidgetItem(f"[{i}] {block}")
            self.blocks_list.addItem(item)

    def load_class_patterns(self):
        self.class_list.clear()
        class_patterns = self.controller.get_class_patterns()
        for i, class_pattern in enumerate(class_patterns):
            item = QListWidgetItem(f"[{i}] {class_pattern}")
            self.class_list.addItem(item)

    def open_time_block_editor(self, day: str, index: int | None) -> None:
        dialog = self.TimeBlockEditorWindow(self.controller, day, index)
        dialog.exec()
        self.controller.refresh_list()

    def open_class_pattern_editor(self, index: int | None) -> None:
        dialog = self.ClassPatternEditorWindow(self.controller, index)
        dialog.exec()
        self.controller.refresh_list()

    def on_time_block_clicked(self, index) -> None:
        day_str = self.day_selector.currentText()
        if day_str not in DAYS:
            raise ValueError("Invalid day selected")
        day: Day = cast(Day, day_str)
        self.open_time_block_editor(day, index.row())

    def on_class_pattern_clicked(self, index) -> None:
        self.open_class_pattern_editor(index.row())

    def add_time_block_clicked(self) -> None:
        day_str = self.day_selector.currentText()
        if day_str not in DAYS:
            raise ValueError("Invalid day selected")
        day: Day = cast(Day, day_str)
        self.open_time_block_editor(day, None)

    def add_class_pattern_clicked(self) -> None:
        self.open_class_pattern_editor(None)

    class TimeBlockEditorWindow(QDialog):
        def __init__(
            self,
            controller: "TimeSlotController",
            day: str,
            index: int | None,
            parent=None,
        ) -> None:
            super().__init__()
            self.controller = controller
            self.json_config = controller.json_config
            self.setWindowTitle("Time Slot Editor")
            self.day = day
            self.index = index

            if index is None:
                self.setWindowTitle("Add Time Block")
            else:
                self.setWindowTitle("Edit Time Block")

            self.setWindowModality(Qt.WindowModality.ApplicationModal)

            # Layout and editing spaces
            layout = QVBoxLayout()
            self.setLayout(layout)
            self.user_start = QLineEdit()
            layout.addWidget(QLabel("Start Time:"))
            layout.addWidget(self.user_start)

            self.user_spacing = QLineEdit()
            layout.addWidget(QLabel("Spacing Time:"))
            layout.addWidget(self.user_spacing)

            self.user_end = QLineEdit()
            layout.addWidget(QLabel("End Time:"))
            layout.addWidget(self.user_end)
            day_lit = cast(Literal["MON", "TUE", "WED", "THU", "FRI"], day)
            # If editing, prepopulate the spaces
            if index is not None:
                time_block = self.json_config.time_slot_config.times[day_lit][index]
                self.user_start.setText(time_block.start)
                self.user_spacing.setText(str(time_block.spacing))
                self.user_end.setText(time_block.end)

            # Button layout
            button_layout = QHBoxLayout()
            if index is not None:
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(self.delete_block)

                delete_button.setAutoDefault(False)
                delete_button.setDefault(False)

                button_layout.addWidget(delete_button)
            else:
                button_layout.addStretch(1)
            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_block)
            button_layout.addWidget(save_button)

            layout.addLayout(button_layout)

        def save_block(self) -> None:
            start = self.user_start.text().strip()
            spacing = self.user_spacing.text().strip()
            end = self.user_end.text().strip()

            # Input validation
            if not start or not spacing or not end:
                QMessageBox.warning(self, "Invalid Input", "All fields are required.")
                return

            if not spacing.isdigit():
                QMessageBox.warning(
                    self, "Invalid Spacing Input", "Spacing must be an integer."
                )
                return

            # Format input
            spacing = int(spacing)
            start = normalize_time(start)
            end = normalize_time(end)
            if start is None:
                QMessageBox.warning(
                    self, "Invalid Input", "Must enter a valid start time."
                )
                return
            if end is None:
                QMessageBox.warning(
                    self, "Invalid Input", "Must enter a valid end time."
                )
                return

            day_index = ["MON", "TUE", "WED", "THU", "FRI"].index(self.day) + 1
            if self.index is None:
                self.controller.add_time_block(day_index, start, spacing, end)
            else:
                self.controller.mod_time_block(
                    day_index, self.index, start, spacing, end
                )
            self.accept()

        def delete_block(self) -> None:
            if self.index is None:
                QMessageBox.warning(self, "Error", "No time block chosen")
                return
            day_index = ["MON", "TUE", "WED", "THU", "FRI"].index(self.day) + 1
            self.controller.del_time_block(day_index, self.index)
            self.accept()

    class ClassPatternEditorWindow(QDialog):
        def __init__(
            self, controller: "TimeSlotController", index: int | None, parent=None
        ) -> None:
            super().__init__()
            self.controller = controller
            self.json_config = controller.json_config
            self.index = index
            self.meeting_rows = []

            if index is None:
                self.setWindowTitle("Add Class Pattern")
            else:
                self.setWindowTitle("Edit Class Pattern")
            self.setWindowModality(Qt.WindowModality.ApplicationModal)

            layout = QVBoxLayout()
            self.setLayout(layout)

            # Adding line edits to layout
            self.user_credits = QLineEdit()
            layout.addWidget(QLabel("Credits:"))
            layout.addWidget(self.user_credits)
            self.user_disabled = QComboBox()
            layout.addWidget(QLabel("Pattern Disabled:"))
            self.user_disabled.addItems(["False", "True"])
            layout.addWidget(self.user_disabled)
            self.user_start = QLineEdit()
            layout.addWidget(QLabel("Start Time (Optional):"))
            layout.addWidget(self.user_start)

            # Meeting list
            self.meetings_layout = QVBoxLayout()
            layout.addLayout(self.meetings_layout)

            self.add_meeting_button = QPushButton("Add Meeting")
            self.add_meeting_button.clicked.connect(lambda: self.add_meeting_row())
            self.meetings_layout.addWidget(self.add_meeting_button)

            # Load existing meetings
            if index is not None:
                pattern = self.json_config.time_slot_config.classes[index]
                self.user_credits.setText(str(pattern.credits))
                if pattern.start_time:
                    self.user_start.setText(pattern.start_time)
                for meeting in pattern.meetings:
                    self.add_meeting_row(
                        meeting.day, meeting.start_time, meeting.duration, meeting.lab
                    )

            button_layout = QHBoxLayout()
            if index is not None:
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(self.delete_class_pattern)

                delete_button.setAutoDefault(False)
                delete_button.setDefault(False)

                button_layout.addWidget(delete_button)
            else:
                button_layout.addStretch(1)

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_class_pattern)
            button_layout.addWidget(save_button)

            layout.addLayout(button_layout)

        def add_meeting_row(
            self, day=None, start=None, duration=None, lab=None
        ) -> None:
            row = QHBoxLayout()
            day_edit = QComboBox()
            day_edit.addItems(["MON", "TUE", "WED", "THU", "FRI"])
            if day:
                day_edit.setCurrentText(day)
            row.addWidget(QLabel("Day:"))
            row.addWidget(day_edit)

            start_edit = QLineEdit()
            start_edit.setPlaceholderText("00:00")
            if start:
                start_edit.setText(start)
            row.addWidget(QLabel("Start Time:"))
            row.addWidget(start_edit)

            duration_edit = QLineEdit()
            duration_edit.setPlaceholderText("00:00")
            if duration:
                duration_edit.setText(str(duration))
            row.addWidget(QLabel("Duration:"))
            row.addWidget(duration_edit)

            lab_edit = QComboBox()
            lab_edit.addItems(["False", "True"])
            if lab:
                lab_edit.setCurrentText(str(lab))
            row.addWidget(QLabel("Lab:"))
            row.addWidget(lab_edit)

            delete_button = QPushButton("Delete Meeting")
            delete_button.clicked.connect(lambda _, r=row: self.delete_meeting_row(r))
            row.addWidget(delete_button)
            self.meetings_layout.addLayout(row)
            self.meeting_rows.append(
                (row, day_edit, start_edit, duration_edit, lab_edit)
            )

        def delete_meeting_row(self, row_layout) -> None:
            for entry in self.meeting_rows:
                if entry[0] is row_layout:
                    self.meeting_rows.remove(entry)
                    break
            while row_layout.count():
                item = row_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            row_layout.deleteLater()

        def save_class_pattern(self) -> None:
            creds = self.user_credits.text().strip()
            if not creds.isdigit():
                QMessageBox.warning(
                    self, "Invalid Input", "Credits must be an integer."
                )
                return
            creds = int(creds)

            disabled = self.user_disabled.currentText() == "True"
            start_time = self.user_start.text().strip()
            if start_time == "":
                start_time = None
            else:
                start_time = normalize_time(start_time)
                if start_time is None:
                    QMessageBox.warning(
                        self, "Invalid Input", "Must enter a valid start time."
                    )
                    return

            meetings = []
            for _, day_edit, start_edit, duration_edit, lab_edit in self.meeting_rows:
                start_edit = normalize_time(start_edit.text().strip())
                if start_edit is None:
                    QMessageBox.warning(
                        self, "Invalid Input", "Must enter a valid start time."
                    )
                    return
                duration_val = duration_edit.text().strip()

                if not duration_val.isdigit():
                    QMessageBox.warning(
                        self, "Invalid Input", "Duration must be an integer."
                    )
                    return
                duration_val = int(duration_val)

                meetings.append(
                    Meeting(
                        day=day_edit.currentText(),
                        start_time=start_edit,
                        duration=duration_val,
                        lab=lab_edit.currentText() == "True",
                    )
                )
            if self.index is None:
                self.controller.add_class_pattern(creds, meetings, disabled, start_time)
            else:
                self.controller.mod_class_pattern(
                    self.index, creds, meetings, disabled, start_time
                )

            self.accept()

        def delete_class_pattern(self) -> None:
            if self.index is None:
                QMessageBox.warning(self, "Error", "No class pattern chosen")
                return
            self.controller.del_class_pattern(self.index)
            self.accept()
