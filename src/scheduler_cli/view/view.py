import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from base_gui import SimpleGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())
    