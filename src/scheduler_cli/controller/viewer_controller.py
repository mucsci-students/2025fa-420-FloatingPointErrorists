import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QMainWindow
from PyQt6.QtGui import QGuiApplication

class viewerClass:
    def __init__ (self, target_widget):
        self.target_widget = target_widget

    def change_schedule(self, schedule):
        self.target_widget.schedule_viewer_label.setText(schedule)