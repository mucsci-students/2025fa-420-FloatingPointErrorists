import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLineEdit, QPushButton, QComboBox, QGridLayout, \
    QVBoxLayout, QTabWidget, QMainWindow, QLabel, QHBoxLayout, QListWidget, QListWidgetItem, QFormLayout
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

from scheduler_config_editor.model.json import JsonConfig
from scheduler_config_editor.model.courses import Course


class CourseEditorGUI(QMainWindow):
    """
    A visual display of courses that allows users to edit the courses
    """
    def __init__(self, controller)  -> None:
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
        
        # Set window title
        self.title = QLabel("Course Editor")
        self.main_layout.addWidget(self.title)

        # Makes and places add button in the top right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.add_button = QPushButton("Add Course")
        button_layout.addWidget(self.add_button)
        self.main_layout.addLayout(button_layout)

        # Creating list of clickable courses and populating it
        self.list = QListWidget(self)
        self.main_layout.addWidget(self.list)

        for i, course in enumerate (self.json_config.scheduler_config.courses):
            item_text = f"{course.course_id} - {i}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, course)
            item.setData(Qt.ItemDataRole.UserRole + 1, i)
            self.list.addItem(item)

        # Connecting Buttons
        self.add_button.clicked.connect(self.controller.open_add_course_window)
        self.list.itemClicked.connect(self.controller.open_edit_course_window)

        # Centering the tabs widget
        # self.courses_widget = CoursesEditorWidget(self)
        # self.setCentralWidget(self.courses_widget)

class CoursesEditorWidget(QWidget):
        def __init__(self, controller, course_data=None, parent=None) -> None:
            super().__init__()
            self.controller = controller
            self.json_config = controller.json_config
            self.course_data = course_data
            self.parent = parent

            if getattr(self.course_data, "course_id", None):
                self.setWindowTitle("Edit Course: " + self.course_data.course_id)
                for i, course in enumerate(self.json_config.scheduler_config.courses):
                    if self.json_config.scheduler_config.courses[i].course_id == self.course_data.course_id:
                        index = i
                        break
                self.course_data = self.json_config.scheduler_config.courses[index]
                self.course_id = self.course_data.course_id
            else:
                self.setWindowTitle("Add New Course")
                self.faculty_data = None
                self.course_id = "Course ID"
            self.courses_widget = QWidget()

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

            # Space to edit course id and credits
            self.course_id_line_edit = QLineEdit(self)
            if self.course_data:
                self.course_id_line_edit.setText(self.course_id)
            else:
                self.course_id_line_edit.setPlaceholderText("Enter Course ID Here")


            self.course_credits_line_edit = QLineEdit(self)
            if self.course_data:
                self.course_credits_line_edit.setText(self.course_data.credits)
            else:
                self.course_credits_line_edit.setPlaceholderText("Enter Credits")

            # Preference list options for labs/rooms/courses
            self.pref_list_layout = QHBoxLayout()

            # Space to choose acceptable rooms
            self.room_layout = QVBoxLayout()
            self.room_layout.addWidget(QLabel("Choose Room(s):"))
            self.room_list = QListWidget(self)
            self.room_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for i, rooms in enumerate(self.json_config.scheduler_config.rooms):
                room = QListWidgetItem(self.json_config.scheduler_config.rooms[i])
                self.room_list.addItem(room)
            self.room_layout.addWidget(self.room_list)
            self.pref_list_layout.addLayout(self.room_layout)

            # Space to choose acceptable labs
            self.lab_layout = QVBoxLayout()
            self.lab_layout.addWidget(QLabel("Choose Lab(s):"))
            self.lab_list = QListWidget(self)
            self.lab_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for i, labs in enumerate(self.json_config.scheduler_config.labs):
                lab = QListWidgetItem(self.json_config.scheduler_config.labs[i])
                self.lab_list.addItem(lab)
            self.lab_layout.addWidget(self.lab_list)
            self.pref_list_layout.addLayout(self.lab_layout)

            # Space to choose course conflicts
            self.course_conflict_layout = QVBoxLayout()
            self.course_conflict_layout.addWidget(QLabel("Choose Course Conflict(s):"))
            self.course_conflicts_list = QListWidget(self)
            self.course_conflicts_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for i, courses in enumerate(self.json_config.scheduler_config.courses):
                course = QListWidgetItem(self.json_config.scheduler_config.courses[i].course_id)
                self.course_conflicts_list.addItem(course)
            self.course_conflict_layout.addWidget(self.course_conflicts_list)
            self.pref_list_layout.addLayout(self.course_conflict_layout)

            # Space to choose faculty available
            self.faculty_layout = QVBoxLayout()
            self.faculty_layout.addWidget(QLabel("Choose Faculty Member(s):"))
            self.faculty_list = QListWidget(self)
            self.faculty_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            for i, faculty in enumerate(self.json_config.scheduler_config.faculty):
                name = QListWidgetItem(self.json_config.scheduler_config.faculty[i].name)
                self.faculty_list.addItem(name)
            self.faculty_layout.addWidget(self.faculty_list)
            self.pref_list_layout.addLayout(self.faculty_layout)

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
            if course_data:
                room_keys = set(getattr(course_data, 'room', []) or [])
                lab_keys = set(getattr(course_data, 'lab', []) or [])
                conflict_keys = set(getattr(course_data, 'conflicts', []) or [])
                faculty_keys = set(getattr(course_data, 'faculty', []) or [])
                # Rooms
                self.preselect_items(self.room_list, room_keys)
                 # Labs
                self.preselect_items(self.lab_list, lab_keys)
                # Course Conflicts
                self.preselect_items(self.course_conflicts_list, conflict_keys)
                # Faculty
                self.preselect_items(self.faculty_list, faculty_keys)

            # Delete button in bottom left and save in bottom right
            self.main_layout.addStretch()
            bottom_buttons_layout = QHBoxLayout()
            if self.course_data:
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda: self.controller.delete_course(self))
                bottom_buttons_layout.addWidget(delete_button)
            bottom_buttons_layout.addStretch()
            save_button = QPushButton("Save")
            save_button.clicked.connect(lambda: self.controller.save_course(self))
            bottom_buttons_layout.addWidget(save_button)
            self.main_layout.addLayout(bottom_buttons_layout)

         # Pre-selecting preferences with data already in config
        def preselect_items(self, list_widget: QListWidget, keys: set[str]) -> None:
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if item and item.text() in keys:
                    item.setSelected(True)

