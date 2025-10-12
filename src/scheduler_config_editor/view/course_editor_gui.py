import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLineEdit, QPushButton, QComboBox, QGridLayout, QVBoxLayout, QTabWidget, QMainWindow
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

class CourseEditorGUI(QMainWindow):
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

            self.courses_widget.layout.addWidget(self.course_id_line_edit, 0, 0)
            self.courses_widget.layout.addWidget(self.course_credits_line_edit, 0, 1)
            self.courses_widget.layout.addWidget(self.course_room_line_edit, 1, 0)
            self.courses_widget.layout.addWidget(self.course_lab_line_edit, 1, 1)
            self.courses_widget.layout.addWidget(self.course_conflicts_line_edit, 2, 0)
            self.courses_widget.layout.addWidget(self.course_faculty_line_edit, 2, 1)

            self.layout.addWidget(self.courses_widget)
            self.setLayout(self.layout)

"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    #config = JsonConfig("../unittests/dummy")
    window = CourseEditorGUI()
    window.show()
    sys.exit(app.exec())"""