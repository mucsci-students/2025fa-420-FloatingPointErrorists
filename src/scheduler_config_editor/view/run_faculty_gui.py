import sys

from PyQt6.QtWidgets import QApplication

from scheduler_config_editor import JsonConfig
from scheduler_config_editor.controller.faculty_controller import FacultyEditorController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = JsonConfig("../unittests/dummy")
    controller = FacultyEditorController(config)
    controller.show()
    sys.exit(app.exec())