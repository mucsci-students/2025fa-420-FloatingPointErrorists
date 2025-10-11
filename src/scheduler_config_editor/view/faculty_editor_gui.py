import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QMainWindow, \
    QHBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox
from PyQt6.QtGui import QGuiApplication, QIntValidator
from scheduler.models import course

import scheduler_config_editor
from scheduler_config_editor import Faculty, JsonConfig
from scheduler_config_editor.model import room, lab

sys.path.append('../controller')


class FacultyEditorGui(QMainWindow):
    """
    This class provides a visual display of faculty members. Users can click add and open an editable window to add
    new faculty members. Users can also click on the faculty names and open an editable window to modify the
    faculty members. Users can also delete faculty members in this editable view as well.
    """

    def __init__(self, json_config) -> None:
        super().__init__()
        self.json_config = json_config
        self.open_editing_window = []

        # Layout Stuff
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Changes title
        self.title = QLabel("Faculty Editor")
        self.layout.addWidget(self.title)

        # Makes and places add button in the top right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.add_button = QPushButton("Add Faculty")
        button_layout.addWidget(self.add_button)
        self.layout.addLayout(button_layout)

        # Creating list of clickable faculty
        self.list = QListWidget(self)
        self.layout.addWidget(self.list)

        # Populates list of faculty
        for i, faculty in enumerate (self.json_config.scheduler_config.faculty):
            self.list.addItem(self.json_config.scheduler_config.faculty[i].name)

        # Connecting Buttons
     #   self.add_button.clicked.connect(self.add_faculty_window)
        self.list.itemClicked.connect(self.open_edit_faculty_window)

    def open_edit_faculty_window(self, item) -> None:
        name = item.text()
        edit_window = EditFacultyWindow(name, self.json_config)
        edit_window.show()
        self.open_editing_window.append(edit_window)

class EditFacultyWindow(QMainWindow):
    def __init__(self, name, json_config) -> None:
        super().__init__()
        self.setWindowTitle("Edit Faculty: " + name)
        self.json_config = json_config
        self.old_name = name
        self.lab_preference_input = {}
        self.room_preference_input = {}
        self.course_preference_input = {}

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = QVBoxLayout()
        centralWidget.setLayout(self.layout)

        # Saving faculty index based on name
        for i, faculty in enumerate(self.json_config.scheduler_config.faculty):
            if json_config.scheduler_config.faculty[i].name == name:
                index = i
                break

        # Space to edit name
        self.name_edit = QLineEdit(self)
        self.layout.addWidget(QLabel("Name:"))
        self.name_edit.setText(name)
        self.layout.addWidget(self.name_edit)

        # Credit layout stuff
        self.credit_layout = QHBoxLayout()
        self.creds_validator = QIntValidator(0, 21)

        # Space to edit maximum credits
        self.max_creds_layout = QVBoxLayout()
        self.max_credits_edit = QLineEdit(self)
        self.max_credits_edit.setValidator(self.creds_validator)
        self.max_creds_layout.addWidget(QLabel("Max Credits:"))
        self.max_credits_edit.setText(str(json_config.scheduler_config.faculty[index].maximum_credits))
        self.max_creds_layout.addWidget(self.max_credits_edit)
        self.credit_layout.addLayout(self.max_creds_layout)

        # Space to edit minimum credits
        self.min_creds_layout = QVBoxLayout()
        self.min_credits_edit = QLineEdit(self)
        self.min_credits_edit.setValidator(self.creds_validator)
        self.min_creds_layout.addWidget(QLabel("Min Credits:"))
        self.min_credits_edit.setText(str(json_config.scheduler_config.faculty[index].minimum_credits))
        self.min_creds_layout.addWidget(self.min_credits_edit)
        self.credit_layout.addLayout(self.min_creds_layout)

        # Space to edit course limit
        self.course_validator = QIntValidator(0, 21)
        self.course_limit_layout = QVBoxLayout()
        self.course_limit_edit = QLineEdit(self)
        self.course_limit_edit.setValidator(self.course_validator)
        self.course_limit_layout.addWidget(QLabel("Course Limit:"))
        self.course_limit_edit.setText(str(json_config.scheduler_config.faculty[index].unique_course_limit))
        self.course_limit_layout.addWidget(self.course_limit_edit)
        self.credit_layout.addLayout(self.course_limit_layout)
        self.layout.addLayout(self.credit_layout)

        # Space to edit time availability

        # Preference list options for labs/rooms/courses
        self.pref_list_layout = QHBoxLayout()

        # Space to choose multiple room preferences
        self.room_layout = QVBoxLayout()
        self.room_layout.addWidget(QLabel("Room Preferences:"))
        self.room_list = QListWidget(self)
        self.room_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, rooms in enumerate (self.json_config.scheduler_config.rooms):
            room = QListWidgetItem(json_config.scheduler_config.rooms[i])
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
            course_id = json_config.scheduler_config.courses[i].course_id
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
            lab = QListWidgetItem(json_config.scheduler_config.labs[i])
            self.lab_list.addItem(lab)
        self.lab_layout.addWidget(self.lab_list)
        self.pref_list_layout.addLayout(self.lab_layout)

        # Preference values layout
        self.layout.addLayout(self.pref_list_layout)
        self.pref_layout = QHBoxLayout()
        self.layout.addLayout(self.pref_layout)
        self.room_pref_layout = QFormLayout()
        self.course_pref_layout = QFormLayout()
        self.lab_pref_layout = QFormLayout()
        self.pref_layout.addLayout(self.room_pref_layout)
        self.pref_layout.addLayout(self.course_pref_layout)
        self.pref_layout.addLayout(self.lab_pref_layout)

        # When changes are made, show preference boxes
        self.room_list.itemSelectionChanged.connect(self.update_room_preferences)
        self.course_list.itemSelectionChanged.connect(self.update_course_preferences)
        self.lab_list.itemSelectionChanged.connect(self.update_lab_preferences)

        # Delete button in bottom left and save in bottom right
        self.layout.addStretch()
        bottom_buttons_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        # delete_button.clicked.connect(self.delete_faculty)
        bottom_buttons_layout.addWidget(delete_button)
        bottom_buttons_layout.addStretch()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_faculty)
        bottom_buttons_layout.addWidget(save_button)
        self.layout.addLayout(bottom_buttons_layout)

    # Selecting room preference values
    def update_room_preferences(self) -> None:
        # Clearing the previous preferences if changes made after first selections
        while self.room_pref_layout.rowCount():
            self.room_pref_layout.removeRow(0)
        self.room_preference_input.clear()

        for i in self.room_list.selectedItems():
            room_name = i.text()
            if room_name in self.room_preference_input:
                    return
            spin = QSpinBox(self)
            spin.setRange(0,10)
            spin.setValue(0)
            self.room_pref_layout.addRow(f"{room_name} preference:", spin)
            self.room_preference_input[room_name] = spin

    # Selecting course preference values
    def update_course_preferences(self) -> None:
        # Clearing the previous preferences if changes made after first selections
        while self.course_pref_layout.rowCount():
            self.course_pref_layout.removeRow(0)
        self.course_preference_input.clear()

        for i in self.course_list.selectedItems():
            course_name = i.text()
            if course_name in self.course_preference_input:
                    return
            spin = QSpinBox(self)
            spin.setRange(0,10)
            spin.setValue(0)
            self.course_pref_layout.addRow(f"{course_name} preference:", spin)
            self.course_preference_input[course_name] = spin

    # Selecting lab preference values
    def update_lab_preferences(self) -> None:
        # Clearing the previous preferences if changes made after first selections
        while self.lab_pref_layout.rowCount():
            self.lab_pref_layout.removeRow(0)
        self.lab_preference_input.clear()

        for i in self.lab_list.selectedItems():
            lab_name = i.text()
            if lab_name in self.lab_preference_input:
                    return
            spin = QSpinBox(self)
            spin.setRange(0, 10)
            spin.setValue(0)
            self.lab_pref_layout.addRow(f"{lab_name} preference:", spin)
            self.lab_preference_input[lab_name] = spin

    def save_faculty (self) -> None:
        try:
            self.minimum_creds = int(self.min_credits_edit.text())
            self.maximum_creds = int(self.max_credits_edit.text())
            self.course_limit = int(self.course_limit_edit.text())

            if 0 > self.minimum_creds or self.minimum_creds > 21:
                raise ValueError("Minimum credits must be between 0 and 21 credits.")
            if 0 > self.maximum_creds or self.maximum_creds > 21:
                raise ValueError("Maximum credits must be between 0 and 21 credits.")
            if 0 > self.course_limit or self.course_limit > 21:
                raise ValueError("Course limit must be between 0 and 21 courses.")
            if self.minimum_creds > self.maximum_creds:
                raise ValueError("Minimum credits must be less than maximum credits.")
            self.room_preferences = {
                room: self.room_preference_input[room].value()
                for room in self.room_preference_input
            }

            self.course_preferences = {
                course: self.course_preference_input[course].value()
                for course in self.course_preference_input
            }

            self.lab_preferences = {
                    lab: self.lab_preference_input[lab].value()
                    for lab in self.lab_preference_input
            }

            EditFacultyWindow.mod_faculty(self.json_config, self.name,
                new_name = self.name_edit.text(),
                minimum_credits = int(self.min_credits_edit.text()),
                maximum_credits = int(self.max_credits_edit.text()),
                unique_course_limit = int(self.course_limit_edit.text()),
                times = {},
                course_preferences = self.course_preferences,
                room_preferences = self.room_preferences,
                lab_preferences = self.lab_preferences)

        except ValueError as error:
            QMessageBox.warning(self, "Input Error: ", str(error))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = JsonConfig("../unittests/dummy")
    window = FacultyEditorGui(config)
    window.show()
    sys.exit(app.exec())