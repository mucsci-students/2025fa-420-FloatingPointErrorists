from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from scheduler import CourseConfig

if TYPE_CHECKING:
    from scheduler_config_editor.controller.course_editor_controller import (
        CourseEditorController,
    )


class CourseEditorGUI(QWidget):
    """
    A visual display of courses that allows users to edit the courses
    """

    def __init__(self, controller: "CourseEditorController") -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config
        self.open_editing_window: list[QWidget] = []

        # Layout Stuff
        self.main_layout = QVBoxLayout(self)

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

        for i, course in enumerate(self.json_config.scheduler_config.courses):
            item_text = f"{course.course_id} - {i}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, course)
            item.setData(Qt.ItemDataRole.UserRole + 1, i)
            self.list.addItem(item)

        # Connecting Buttons
        self.add_button.clicked.connect(self.controller.open_add_course_window)
        self.list.itemClicked.connect(self.controller.open_edit_course_window)


class CoursesEditorWidget(QWidget):
    def __init__(
        self,
        controller: "CourseEditorController",
        course_data: CourseConfig | None = None,
        index: int = -1,
    ) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config
        self.course_data = course_data
        self.index = index
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if getattr(self.course_data, "course_id", None):
            if self.course_data is not None:
                self.setWindowTitle("Edit Course: " + self.course_data.course_id)
                for i, course in enumerate(self.json_config.scheduler_config.courses):
                    if (
                        self.json_config.scheduler_config.courses[i].course_id
                        == self.course_data.course_id
                    ):
                        self.course_data = self.json_config.scheduler_config.courses[
                            index
                        ]
                        self.course_id = self.course_data.course_id
                        break
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
        self.main_layout = QVBoxLayout(self)

        # Space to edit course id and credits
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Course ID:"))
        self.course_id_line_edit = QLineEdit(self)
        if self.course_data:
            self.course_id_line_edit.setText(self.course_id)
        else:
            self.course_id_line_edit.setPlaceholderText("Enter Course ID Here")
        top_layout.addWidget(self.course_id_line_edit)

        top_layout.addWidget(QLabel("Credits:"))
        self.course_credits_line_edit = QLineEdit(self)
        if self.course_data:
            self.course_credits_line_edit.setText(str(self.course_data.credits))
        else:
            self.course_credits_line_edit.setPlaceholderText("Enter Credits")
        top_layout.addWidget(self.course_credits_line_edit)
        self.main_layout.addLayout(top_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        # Space to choose acceptable rooms
        self.room_layout = QVBoxLayout()
        self.room_layout.addWidget(QLabel("Choose Room(s):"))
        self.room_list = QListWidget(self)
        self.room_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, _rooms in enumerate(self.json_config.scheduler_config.rooms):
            room = QListWidgetItem(self.json_config.scheduler_config.rooms[i])
            self.room_list.addItem(room)
        self.room_layout.addWidget(self.room_list)
        scroll_layout.addLayout(self.room_layout)

        # Space to choose acceptable labs
        self.lab_layout = QVBoxLayout()
        self.lab_layout.addWidget(QLabel("Choose Lab(s):"))
        self.lab_list = QListWidget(self)
        self.lab_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, _labs in enumerate(self.json_config.scheduler_config.labs):
            lab = QListWidgetItem(self.json_config.scheduler_config.labs[i])
            self.lab_list.addItem(lab)
        self.lab_layout.addWidget(self.lab_list)
        scroll_layout.addLayout(self.lab_layout)

        # Space to choose course conflicts
        self.course_conflict_layout = QVBoxLayout()
        self.course_conflict_layout.addWidget(QLabel("Choose Course Conflict(s):"))
        self.course_conflicts_list = QListWidget(self)
        self.course_conflicts_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        seen_courses_list = {self.course_id}
        for i, _courses in enumerate(self.json_config.scheduler_config.courses):
            course_id = self.json_config.scheduler_config.courses[i].course_id
            if course_id not in seen_courses_list:
                seen_courses_list.add(course_id)
                course = QListWidgetItem(course_id)
                self.course_conflicts_list.addItem(course)
        self.course_conflict_layout.addWidget(self.course_conflicts_list)
        scroll_layout.addLayout(self.course_conflict_layout)

        # Space to choose faculty available
        self.faculty_layout = QVBoxLayout()
        self.faculty_layout.addWidget(QLabel("Choose Faculty Member(s):"))
        self.faculty_list = QListWidget(self)
        self.faculty_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for i, _faculty in enumerate(self.json_config.scheduler_config.faculty):
            name = QListWidgetItem(self.json_config.scheduler_config.faculty[i].name)
            self.faculty_list.addItem(name)
        self.faculty_layout.addWidget(self.faculty_list)
        scroll_layout.addLayout(self.faculty_layout)

        # Preference values main_layout
        pref_box = QWidget()
        pref_box_layout = QHBoxLayout(pref_box)
        self.room_pref_layout = QFormLayout()
        self.course_pref_layout = QFormLayout()
        self.lab_pref_layout = QFormLayout()
        pref_box_layout.addLayout(self.room_pref_layout)
        pref_box_layout.addLayout(self.course_pref_layout)
        pref_box_layout.addLayout(self.lab_pref_layout)

        scroll_layout.addWidget(pref_box)
        scroll_area.setWidget(scroll_content)
        self.main_layout.addWidget(scroll_area)

        # Preselecting preference values if editing
        if course_data:
            room_keys = set(getattr(course_data, "room", []) or [])
            lab_keys = set(getattr(course_data, "lab", []) or [])
            conflict_keys = set(getattr(course_data, "conflicts", []) or [])
            faculty_keys = set(getattr(course_data, "faculty", []) or [])
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
