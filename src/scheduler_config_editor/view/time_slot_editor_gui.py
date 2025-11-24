import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QComboBox, \
    QSplitter, QAbstractItemView, QListWidgetItem, QDialog, QLineEdit
from PyQt6.QtWidgets.QWidget import setWindowModality
from scheduler import FacultyConfig

sys.path.append("../controller")


class TimeSlotEditorGui(QMainWindow):
    """
    This class provides a visual display of what is in the time slot config. Users can click add to open an editable
    window to add new time blocks and class patterns. Users can also click on the time block indexes or class pattern
    indexes to open an editable window to modify each one. Users can also delete time blocks or class patterns in this
    editable view as well.
    """

    def __init__(self, controller: "TimeSlotEditorController", parent=None) -> None:
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

        # Day selector for time blocks
        day_layout = QHBoxLayout()
        main_layout.addLayout(day_layout)

        day_layout.addWidget(QLabel("Select Day:"))
        self.day_selector = QComboBox()
        self.day_selector.addItems(["MON", "TUE", "WED", "THU", "FRI"])
        day_layout.addWidget(self.day_selector)

        # Refreshes time blocks when a new day is selected
        self.day_selector.currentTextChanged.connect(self.load_time_blocks_for_day)

        # Splitting the window into two panels, one for time blocks and one for class patterns
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Time block panel layout (left side)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Time Blocks"))

        self.blocks_list = QListWidget()
        self.blocks_list.clicked.connect(self.open_edit_time_block)
        left_layout.addWidget(self.blocks_list)

        add_block_button = QPushButton("Add Time Block")
        add_block_button.clicked.connect(self.open_add_time_block)
        left_layout.addWidget(add_block_button)

        # Class pattern panel layout (right side)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Class Patterns"))

        self.class_list = QListWidget()
        self.class_list.clicked.connect(self.open_edit_class_pattern)
        right_layout.addWidget(self.class_list)

        add_class_button = QPushButton("Add Class Pattern")
        add_class_button.clicked.connect(self.open_add_class_pattern)
        right_layout.addWidget(add_class_button)

        # Populate class patterns into the list
        for i, class_pattern in enumerate(self.json_config.time_slot_config.classes):

            self.class_list.addItem(QListWidgetItem(f"[{i}] {class_pattern}"))

        # Adding panels to the splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)

    def load_time_blocks_for_day(self, day:str) -> None:
        """Populates the list of time blocks for the day selected."""
        self.blocks_list.clear()
        blocks = self.json_config.time_slot_config.times.get(day, [])
        for i, block in enumerate(blocks):
            item = QListWidgetItem(f"[{i}] {block}")
            self.blocks_list.addItem(item)

    class TimeBlockEditorWindow(QDialog):
        def __init__(self, controller: "TimeSlotEditorController", day: str, index: int|None, parent=None) -> None:
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
            self.user_start = QLineEdit()
            layout.addWidget(QLabel("Start Time:"))
            layout.addWidget(self.user_start)

            self.user_spacing = QLineEdit()
            layout.addWidget(QLabel("Spacing Time:"))
            layout.addWidget(self.user_spacing)

            self.user_end = QLineEdit()
            layout.addWidget(QLabel("End Time:"))
            layout.addWidget(self.user_end)

            # If editing, prepopulate the spaces
            if index is not None:
                time_block = self.json_config.time_slot_config.times.get(day)[index]
                self.user_start.setText(time_block.start)
                self.user_spacing.setText(str(time_block.spacing))
                self.user_end.setText(time_block.end)

            # Button layout
            button_layout = QHBoxLayout()
            if index is not None:
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(self.delete_block)
                button_layout.addWidget(delete_button)
            else:
                button_layout.addStretch(1)
            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_block)
            button_layout.addWidget(save_button)

            layout.addLayout(button_layout)

        def save_block(self) -> None:
            start = self.user_start.text()
            spacing = int(self.user_spacing.text())
            end = self.user_end.text()

            if self.index is None:
                day_index = ["MON", "TUE", "WED", "THU", "FRI"].index(self.day) +1
                self.controller.add_time_block(day_index, start, spacing, end)
            else:
                day_index = ["MON", "TUE", "WED", "THU", "FRI"].index(self.day) +1
                self.controller.mod_time_block(day_index, self.index, start, spacing, end)

        def delete_block(self) -> None:
            day_index = ["MON", "TUE", "WED", "THU", "FRI"].index(self.day) + 1
            self.controller.del_time_block(day_index, self.index)

    class ClassPatternEditorWindow(QDialog):
        def __init__(self, controller: "TimeSlotEditorController", day: str, index: int|None, parent=None) -> None:
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
            layout.addWidget(QLabel("Disabled:"))
            self.user_disabled.addItems(["False", "True"])
            layout.addWidget(self.user_disabled)
            self.user_start = QLineEdit()
            layout.addWidget(QLabel("Start Time:"))
            layout.addWidget(self.user_start)

            # Meeting list
            self.meetings_layout = QVBoxLayout()
            layout.addLayout(self.meetings_layout)

            self.add_meeting_button = QPushButton("Add Meeting")
            self.add_meeting_button.clicked.connect(self.add_meeting_row())
            self.meetings_layout.addWidget(self.add_meeting_button)

            # Load existing meetings
            if index is not None:
                pattern = self.json_config.time_slot_config.classes[index]
                self.user_credits.setText(str(pattern.credits))
                if pattern.start:
                    self.user_start.setText(pattern.start)
                for meeting in pattern.meetings:
                    self.add_meeting_row(meeting.day, meeting.start_time, meeting.duration, meeting.lab)


            button_layout = QHBoxLayout()
            if index is not None:
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(self.delete_class_pattern)
                button_layout.addWidget(delete_button)
            else:
                button_layout.addStretch(1)

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.save_class_pattern)
            button_layout.addWidget(save_button)

            layout.addLayout(button_layout)

        def add_meeting_row(self, day=None, start=None, duration=None,  lab=None) -> None:
            row = QHBoxLayout()
            day_edit = QComboBox()
            day_edit.addItems(["Mon", "Tue", "Wed", "Thu", "Fri"])
            if day:
                day_edit.setCurrentText(day)
            row.addWidget(day_edit)

            start_edit = QLineEdit()
            start_edit.setPlaceholderText("Start Time")
            if start:
                start_edit.setText(start)
            row.addWidget(start_edit)

            duration_edit = QLineEdit()
            duration_edit.setPlaceholderText("End Time")
            if duration:
                    duration_edit.setText(duration)
            row.addWidget(duration_edit)

            lab_edit = QComboBox()
            lab_edit.addItems(["False", "True"])
            if lab:
                lab_edit.setCurrentText(str(lab))
            row.addWidget(lab_edit)

            delete_button = QPushButton("🗑")
            delete_button.clicked.connect(self.delete_meeting_row(row))
            row.addWidget(delete_button)
            self.meetings_layout.addLayout(row)
            self.meeting_rows.append((row, day_edit, start_edit, duration_edit, lab_edit))

        def delete_meeting_row(self, row_layout) -> None:
            for (layout, day, start, duration, lab) in self.meeting_rows:
                if layout is row_layout:
                        self.meeting_rows.remove((layout, day, start, duration, lab))
                        break
            while row_layout.count():
                item = row_layout.takeAt(0)
                if item.widget():
                        item.widget().deleteLater()
            self.meetings_layout.removeItem(row_layout)





        def save_class_pattern(self) -> None:
            creds = int(self.user_credits.text())
            disabled = self.user_disabled.currentText() == "TRUE"
            start_time = self.user_start.text() or None

            meetings =[]
            for (day_edit, start_edit, duration_edit, lab_edit) in self.meetings_rows:
                meetings.append({
                    "day": day_edit.currentText(),
                    "start_time": start_edit.text(),
                    "duration": duration_edit.text(),
                    "lab": lab_edit.currentText() == "True",
                })
            if self.index is None:
                self.controller.add_class_pattern(creds, meetings, disabled, start_time)
            else:
                self.controller.mod_class_pattern(self.index, creds, meetings, disabled, start_time)

        def delete_class_pattern(self) -> None:
            self.controller.del_class_pattern(self.index)