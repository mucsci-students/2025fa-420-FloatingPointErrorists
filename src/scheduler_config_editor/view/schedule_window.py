from PyQt6.QtWidgets import QLabel, QWidget,  QVBoxLayout, QMainWindow
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

class newWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window title and size
        self.setWindowTitle("Schedule")
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        self.widget = newWidget(self)
        self.setCentralWidget(self.widget)



class newWidget(QWidget):
    def __init__(self, parent) -> None:

        super(QWidget, self).__init__(parent)

        self.newWidget = QWidget()
        self.schedule = QLabel()
        self.schedule.setText("test")


        self.newWidget.layout = QVBoxLayout()
        self.newWidget.layout.addWidget(self.schedule)
        self.setLayout(self.newWidget.layout)
