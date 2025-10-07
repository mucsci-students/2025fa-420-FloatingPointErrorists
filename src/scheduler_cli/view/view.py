import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from scheduler_cli.view.base_gui import SimpleGUI

def view() -> None:
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    view()
    