import sys

from PyQt6.QtCore import QTimer, QTime
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, \
    QHBoxLayout, QListWidget, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox, QGroupBox, QGridLayout, QTimeEdit
from PyQt6.QtGui import QGuiApplication, QIntValidator
from scheduler import TimeRange
from scheduler_config_editor.model import Faculty, JsonConfig

sys.path.append('../controller')


class FacultyEditorGui(QMainWindow):
    """
    This class provides a visual display of faculty members. Users can click add and open an editable window to add
    new faculty members. Users can also click on the faculty names and open an editable window to modify the
    faculty members. Users can also delete faculty members in this editable view as well.
    """

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config
        self.open_editing_window: list[QWidget] = []

        # Layout Stuff
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

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

        # Changes title
        self.title = QLabel("Faculty Editor")
        self.main_layout.addWidget(self.title)

        # Makes and places add button in the top right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.add_button = QPushButton("Add Faculty")
        button_layout.addWidget(self.add_button)
        self.main_layout.addLayout(button_layout)

        # Creating list of clickable faculty
        self.list = QListWidget(self)
        self.main_layout.addWidget(self.list)

        # Populates list of faculty
        for i, faculty in enumerate (self.json_config.scheduler_config.faculty):
            self.list.addItem(self.json_config.scheduler_config.faculty[i].name)

        # Connecting Buttons
        self.add_button.clicked.connect(self.controller.open_add_faculty_window)
        self.list.itemClicked.connect(self.controller.open_edit_faculty_window)

class EditFacultyWindow(QMainWindow):
    def __init__(self, controller, faculty_data=None, parent_gui=None) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config
        self.faculty_data = faculty_data
        self.parent_gui = parent_gui

        if getattr(self.faculty_data,"name", None):
            self.setWindowTitle("Edit Faculty: " + self.faculty_data.name)
            for i, faculty in enumerate(self.json_config.scheduler_config.faculty):
                if self.json_config.scheduler_config.faculty[i].name == self.faculty_data.name:
                    index = i
                    break
            self.faculty_data = self.json_config.scheduler_config.faculty[index]
            self.name = self.faculty_data.name
        else:
            self.setWindowTitle("Add New Faculty")
            self.faculty_data = None
            self.name = "Name"

        self.lab_preference_input: dict[str, QSpinBox] = {}
        self.room_preference_input: dict[str, QSpinBox] = {}
        self.course_preference_input: dict[str, QSpinBox] = {}
        self.time_availability: dict[str, list[tuple[QTimeEdit, QTimeEdit, QPushButton]]] = {}
        self.parent_gui = parent_gui

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

        # Layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.main_layout = QVBoxLayout()
        centralWidget.setLayout(self.main_layout)

        # Space to edit name
        self.name_edit = QLineEdit(self)
        self.main_layout.addWidget(QLabel("Name:"))
        if self.faculty_data:
            self.name_edit.setText(self.name)
        else:
            self.name_edit.setPlaceholderText("Name")
        self.main_layout.addWidget(self.name_edit)
        self.name_edit.setFocus()

        # Credit layout stuff
        self.credit_layout = QHBoxLayout()
        self.creds_validator = QIntValidator(0, 21)

        # Space to edit maximum credits
        self.max_creds_layout = QVBoxLayout()
        self.max_credits_edit = QLineEdit(self)
        self.max_credits_edit.setValidator(self.creds_validator)
        self.max_creds_layout.addWidget(QLabel("Max Credits:"))
        if self.faculty_data:
            self.max_credits_edit.setText(str(self.faculty_data.maximum_credits))
        else:
            self.max_credits_edit.setPlaceholderText("Maximum Credits")
        self.max_creds_layout.addWidget(self.max_credits_edit)
        self.credit_layout.addLayout(self.max_creds_layout)

        # Space to edit minimum credits
        self.min_creds_layout = QVBoxLayout()
        self.min_credits_edit = QLineEdit(self)
        self.min_credits_edit.setValidator(self.creds_validator)
        self.min_creds_layout.addWidget(QLabel("Min Credits:"))
        if self.faculty_data:
            self.min_credits_edit.setText(str(self.faculty_data.minimum_credits))
        else:
            self.min_credits_edit.setPlaceholderText("Minimum Credits")
        self.min_creds_layout.addWidget(self.min_credits_edit)
        self.credit_layout.addLayout(self.min_creds_layout)

        # Space to edit course limit
        self.course_validator = QIntValidator(0, 21)
        self.course_limit_layout = QVBoxLayout()
        self.course_limit_edit = QLineEdit(self)
        self.course_limit_edit.setValidator(self.course_validator)
        self.course_limit_layout.addWidget(QLabel("Course Limit:"))
        if self.faculty_data:
            self.course_limit_edit.setText(str(self.faculty_data.unique_course_limit))
        else:
            self.course_limit_edit.setPlaceholderText("Course Limit")
        self.course_limit_layout.addWidget(self.course_limit_edit)
        self.credit_layout.addLayout(self.course_limit_layout)
        self.main_layout.addLayout(self.credit_layout)

        # Space to edit time availability
        self.time_label = QLabel("Time Availability")
        self.main_layout.addWidget(self.time_label)
        self.time_layout = QGridLayout()
        self.main_layout.addLayout(self.time_layout)
        self.days = ["MON", "TUE", "WED", "THU", "FRI"]
        self.day_interval_widgets: dict[str, dict[str, list[tuple[QTimeEdit, QTimeEdit, QPushButton]]]] = {}

        for i, day in enumerate(self.days):
            self.day_layout = QVBoxLayout()
            self.day_label = QLabel(day)
            self.add_interval_button = QPushButton(f"Add Time Range")
            # Adds interval for each specific day
            self.add_interval_button.clicked.connect(lambda _, d=day:self.add_interval(d))

            self.day_layout.addWidget(self.day_label)
            self.day_layout.addWidget(self.add_interval_button)

            self.intervals_container = QVBoxLayout()
            self.day_layout.addLayout(self.intervals_container)
            self.day_interval_widgets[day] = {
                "container": self.intervals_container,
                "intervals": []
            }
            self.time_layout.addLayout(self.day_layout, 0 ,i)

        # Loading previous availabilities
        if self.faculty_data and self.faculty_data.times:
            for day, intervals in self.faculty_data.times.items():
                for interval in intervals:
                    self.add_interval(day, interval.start, interval.end)

        # Preference list options for labs/rooms/courses
        self.pref_list_layout = QHBoxLayout()

        # Space to choose multiple room preferences
        self.room_layout = QVBoxLayout()
        self.room_layout.addWidget(QLabel("Room Preferences:"))
        self.room_list = QListWidget(self)
        self.room_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, rooms in enumerate (self.json_config.scheduler_config.rooms):
            room = QListWidgetItem(self.json_config.scheduler_config.rooms[i])
            self.room_list.addItem(room)
        self.room_layout.addWidget(self.room_list)
        self.pref_list_layout.addLayout(self.room_layout)

        # Space to choose multiple course preferences
        self.course_layout = QVBoxLayout()
        self.course_layout.addWidget(QLabel("Course Preferences:"))
        self.course_list = QListWidget(self)
        self.course_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        seen_courses_list = set()
        for i, courses in enumerate(self.json_config.scheduler_config.courses):
            course_id = self.json_config.scheduler_config.courses[i].course_id
            if course_id not in seen_courses_list:
                seen_courses_list.add(course_id)
                course = QListWidgetItem(course_id)
                self.course_list.addItem(course)
        self.course_layout.addWidget(self.course_list)
        self.pref_list_layout.addLayout(self.course_layout)


        # Space to choose multiple lab preferences
        self.lab_layout = QVBoxLayout()
        self.lab_layout.addWidget(QLabel("Lab Preferences:"))
        self.lab_list = QListWidget(self)
        self.lab_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, labs in enumerate(self.json_config.scheduler_config.labs):
            lab = QListWidgetItem(self.json_config.scheduler_config.labs[i])
            self.lab_list.addItem(lab)
        self.lab_layout.addWidget(self.lab_list)
        self.pref_list_layout.addLayout(self.lab_layout)

        # Preference values layout
        self.main_layout.addLayout(self.pref_list_layout)
        self.pref_layout = QHBoxLayout()
        self.main_layout.addLayout(self.pref_layout)
        self.room_pref_layout = QFormLayout()
        self.course_pref_layout = QFormLayout()
        self.lab_pref_layout = QFormLayout()
        self.pref_layout.addLayout(self.room_pref_layout)
        self.pref_layout.addLayout(self.course_pref_layout)
        self.pref_layout.addLayout(self.lab_pref_layout)

        # Preselecting preference values if editing
        if self.faculty_data:
            self.preselect_items(
                self.room_list,
                self.faculty_data.room_preferences,
                self.room_pref_layout,
                self.room_preference_input
            )
            self.preselect_items(
                self.course_list,
                self.faculty_data.course_preferences,
                self.course_pref_layout,
                self.course_preference_input
            )
            self.preselect_items(
                self.lab_list,
                self.faculty_data.lab_preferences,
                self.lab_pref_layout,
                self.lab_preference_input
            )

        # When changes are made, show preference boxes
        self.room_list.itemSelectionChanged.connect(lambda: self.generic_update_preferences(
            self.room_list, self.room_pref_layout, self.room_preference_input))
        self.course_list.itemSelectionChanged.connect(lambda: self.generic_update_preferences(
            self.course_list, self.course_pref_layout, self.course_preference_input))
        self.lab_list.itemSelectionChanged.connect(lambda: self.generic_update_preferences(
            self.lab_list, self.lab_pref_layout, self.lab_preference_input))

        # Delete button in bottom left and save in bottom right
        self.main_layout.addStretch()
        bottom_buttons_layout = QHBoxLayout()
        if self.faculty_data:
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda: self.controller.delete_faculty(self))
            bottom_buttons_layout.addWidget(delete_button)
        bottom_buttons_layout.addStretch()
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.controller.save_faculty(self))
        bottom_buttons_layout.addWidget(save_button)
        self.main_layout.addLayout(bottom_buttons_layout)

    def add_interval(self, day: str, start_time_str: str |None = None, end_time_str: str | None = None) -> None:
        container = self.day_interval_widgets[day]["container"]

        interval_widget = QWidget()
        interval_layout = QHBoxLayout()
        interval_layout.setContentsMargins(4, 2, 4, 2)
        interval_layout.setSpacing(8)
        interval_widget.setLayout(interval_layout)

        #Formatting time stuff
        start_time = QTimeEdit()
        start_time.setDisplayFormat("HH:mm")
        start_time.setMaximumWidth(70)
        if start_time_str:
            h, m = map(int, start_time_str.split(":"))
            start_time.setTime(QTime(h, m))
        else:
            start_time.setTime(start_time.time().currentTime())
        end_time = QTimeEdit()
        end_time.setDisplayFormat("HH:mm")
        end_time.setMaximumWidth(70)
        if end_time_str:
            h, m = map(int, end_time_str.split(":"))
            end_time.setTime(QTime(h, m))
        else:
            end_time.setTime(end_time.time().currentTime())

        remove_button = QPushButton("🗑️")
        remove_button.setMaximumWidth(70)
        interval_tuple = start_time, end_time, remove_button

        def remove_interval() -> None:
            container.removeWidget(interval_widget)
            interval_widget.deleteLater()
            self.day_interval_widgets[day]["intervals"].remove((start_time, end_time, remove_button))

        remove_button.clicked.connect(remove_interval)

        interval_layout.addWidget(QLabel("Start:"))
        interval_layout.addWidget(start_time)
        interval_layout.addWidget(QLabel("End:"))
        interval_layout.addWidget(end_time)
        interval_layout.addWidget(remove_button)

        container.addWidget(interval_widget)
        self.day_interval_widgets[day]["intervals"].append((start_time, end_time, remove_button))


    # Pre-selecting preferences with data already in config
    def preselect_items(self, list_widget: QListWidget, keys: dict[str, int], layout: QFormLayout,
                        input: dict[str, QSpinBox]) -> None:
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item is None:
                continue
            self.name = item.text()
            if self.name in keys:
                item.setSelected(True)
                spin = QSpinBox(self)
                spin.setRange(0,10)
                spin.setValue(keys[self.name])
                layout.addRow(f"{self.name} preference:", spin)
                input[self.name] = spin

    # Selecting preference values
    def generic_update_preferences(self, list_widget: QListWidget, layout: QFormLayout,
                                   input_preferences: dict[str, QSpinBox]) -> None:
        # Clearing the previous preferences if changes made after first selections
        current_values = {
            name: spin.value()
            for name, spin in input_preferences.items()
        }

        already_selected = {i.text() for i in list_widget.selectedItems()}
        for name in list(input_preferences.keys()):
            if name not in already_selected:
                for i in range(layout.rowCount()):
                    label = layout.itemAt(i, QFormLayout.ItemRole.LabelRole)
                    if label is not None:
                        if isinstance(label.widget(), QLabel):
                            if label.widget().text() == f"{name} preference:":
                                layout.removeRow(i)
                            break
                del input_preferences[name]

        for i in list_widget.selectedItems():
            name = i.text()
            if name not in input_preferences:
                spin = QSpinBox(self)
                spin.setRange(0, 10)
                spin.setValue(current_values.get(name, 0))
                layout.addRow(f"{name} preference:", spin)
                input_preferences[name] = spin
