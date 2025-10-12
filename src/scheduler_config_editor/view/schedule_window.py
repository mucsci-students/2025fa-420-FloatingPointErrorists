from PyQt6.QtWidgets import QLabel, QWidget,  QVBoxLayout, QMainWindow, QScrollArea
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

class newWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()

        # Set window title and size
        self.setWindowTitle("Schedule")
        self.resize(int(screen_width * 0.25), int(screen_height * 0.25))

        self.widget = newWidget(self)
        self.setCentralWidget(self.widget)



class newWidget(QWidget):

    def __init__(self, parent: newWindow) -> None:

        super(QWidget, self).__init__(parent)

        self.my_widget = QWidget()
        self.schedule = QLabel()
        self.schedule.setText("Please Wait up to a minute.")

        #scroll area for schedule
        self.scroll_area_w = QScrollArea()
        self.scroll_area_w.setWidgetResizable(True)
        self.scroll_area_w.setWidget(self.schedule)

        self.my_layout = QVBoxLayout()
        self.my_layout.addWidget(self.scroll_area_w)
        self.setLayout(self.my_layout)
