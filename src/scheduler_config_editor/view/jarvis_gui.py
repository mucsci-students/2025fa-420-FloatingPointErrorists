from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
)



class JarvisGUI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window title and size
        self.setWindowTitle("J.A.R.V.I.S")
        self.setWindowIcon(QtGui.QIcon("jarvis.png"))
        window_width = screen_width * 0.1
        window_height = screen_height * 0.5
        self.resize(int(window_width), int(window_height))

        jarvis_logo = QLabel()
        jarvis_pixmap = QPixmap("jarvis.png")
        jarvis_logo.setPixmap(jarvis_pixmap)
        self.setCentralWidget(jarvis_logo)

        ask_jarvis_line_edit = QLineEdit(parent=self)
        ask_jarvis_line_edit.setFixedWidth(int(window_width * 0.7))
        ask_jarvis_line_edit.setPlaceholderText("Ask J.A.R.V.I.S: ")
        ask_jarvis_line_edit.move(int(window_width * 0.15), int(window_height * 0.9))
        ask_jarvis_line_edit.setAlignment(Qt.AlignmentFlag.AlignBottom)
