import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLineEdit, QPushButton, QComboBox, QGridLayout, QVBoxLayout, QTabWidget, QMainWindow
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

from scheduler_config_editor.model.json import JsonConfig
from scheduler_config_editor.model.courses import Course


class CourseEditorGUI(QMainWindow):
    """
    A visual display of courses that allows users to edit the config
    """
    def __init__(self)  -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # Set window title and size
        self.setWindowTitle("Course Editor")
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Centering the tabs widget
        self.courses_widget = CoursesEditorWidget(self)
        self.setCentralWidget(self.courses_widget)

class CoursesEditorWidget(QWidget):
        def __init__(self, parent) -> None:
            super(QWidget, self).__init__(parent)

            self.courses_widget = QWidget()

            self.layout = QGridLayout(self)

            self.courses_widget.layout = QGridLayout(self)
            self.courses_widget.setLayout(self.courses_widget.layout)

             # course id
             # credits
             # room
             # lab
             # conflicts
             # faculty
            self.course_id_line_edit = QLineEdit(self)
            self.course_id_line_edit.setPlaceholderText("Enter Course ID Here")
            self.course_credits_line_edit = QLineEdit(self)
            self.course_credits_line_edit.setPlaceholderText("Enter Credits") 
            self.course_room_line_edit = QLineEdit(self)
            self.course_room_line_edit.setPlaceholderText("Enter Room")
            self.course_lab_line_edit = QLineEdit(self)
            self.course_lab_line_edit.setPlaceholderText("Enter Lab")
            self.course_conflicts_line_edit = QLineEdit(self)
            self.course_conflicts_line_edit.setPlaceholderText("Enter Course Conflict")
            self.course_faculty_line_edit = QLineEdit(self)
            self.course_faculty_line_edit.setPlaceholderText("Enter Faculty")
            self.course_index_line_edit = QLineEdit(self)
            self.course_index_line_edit.setPlaceholderText("Enter Index")

            self.courses_widget.layout.addWidget(self.course_id_line_edit, 0, 0)
            self.courses_widget.layout.addWidget(self.course_credits_line_edit, 0, 1)
            self.courses_widget.layout.addWidget(self.course_room_line_edit, 1, 0)
            self.courses_widget.layout.addWidget(self.course_lab_line_edit, 1, 1)
            self.courses_widget.layout.addWidget(self.course_conflicts_line_edit, 2, 0)
            self.courses_widget.layout.addWidget(self.course_faculty_line_edit, 2, 1)
            self.courses_widget.layout.addWidget(self.course_index_line_edit, 3, 0)

            self.save_button = QPushButton("Save Course")
            self.delete_button = QPushButton("Delete Course")
            self.courses_widget.layout.addWidget(self.save_button, 4, 0)
            self.courses_widget.layout.addWidget(self.delete_button, 4, 1)

            self.save_button.clicked.connect(self.save_course)
            self.delete_button.clicked.connect(self.delete_course)

            self.layout.addWidget(self.courses_widget)
            self.setLayout(self.layout)

            self.course_id = self.course_id_line_edit.text()
            self.credits = self.course_credits_line_edit.text()
            self.room = self.course_room_line_edit.text()
            self.lab = self.course_lab_line_edit.text()
            self.conflicts = self.course_conflicts_line_edit.text()
            self.index = self.course_index_line_edit.text()

        def save_course(self):
            #CoursesEditorWidget.mod_course( )
            print("saved course")
            pass
            
        def delete_course(self):
            #.delete_course()
            print("deleted course")
            pass

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = JsonConfig("../unittests/dummy")
    window = CourseEditorGUI(config)
    window.show()
    sys.exit(app.exec())"""