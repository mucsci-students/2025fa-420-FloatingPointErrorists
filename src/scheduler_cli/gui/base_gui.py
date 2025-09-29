import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QGuiApplication

"""THROWAWAY!!! just for project structure/testing purposes."""

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window title and size
        self.setWindowTitle("Binging with Babish.")
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))
        self.move(int(screen_width * 0.25), int(screen_height * 0.25))

        # Create widgets
        self.label = QLabel("i'm over here-", self)
        self.sample_button = QPushButton("Click Me", self)
        self.button2 = QPushButton("foetnite", self)

        # Connect button to function
        self.sample_button.clicked.connect(self.sample_button_click)
        self.button2.clicked.connect(self.button2_click)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.sample_button)
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def sample_button_click(self):
        self.label.setText("You clicked the button!")

    def button2_click(self):
        self.label.setText("yuh.")
        self.label.resize(100, 100)
        self.resize(random.randint(1, 1000), random.randint(1, 1000))
