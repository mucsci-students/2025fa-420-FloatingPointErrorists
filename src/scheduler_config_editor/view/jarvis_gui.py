from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
    QSizePolicy,
)

from scheduler_config_editor.model.langchain_client import LangchainClient
from scheduler_config_editor.model import JsonConfig


class JarvisGUI(QMainWindow):
    data_changed = pyqtSignal()

    def __init__(self, json_config: JsonConfig) -> None:
        super().__init__()
        print("data_changed type:", type(self.data_changed))
        print("has emit:", hasattr(self.data_changed, "emit"))
        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
        else:
            screen_width = 1920
            screen_height = 1080
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Set window title and size
        self.setWindowTitle("J.A.R.V.I.S")
        self.setWindowIcon(QtGui.QIcon("jarvis.png"))
        window_width = screen_width * 0.4
        window_height = screen_height * 0.75
        self.resize(int(window_width), int(window_height))

        # Main layout to add in the chat area
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Makes the chat area scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        # Adds the actual chat area
        self.chat = QWidget()
        self.chat_layout = QVBoxLayout(self.chat)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.chat)

        # Input area for Jarvis
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask J.A.R.V.I.S using format Jarvis, ...")
        self.input_field.returnPressed.connect(self.use_input)
        main_layout.addWidget(self.input_field)

        # Initializing LangChain
        self.langchain_client = LangchainClient(json_config=json_config)

    def use_input(self):
        query = self.input_field.text()
        if not query:
            return

        # Add's user's message to chat area
        self.add_message(query, sender="user")
        self.input_field.clear()

        # Asks LangChain client for a response to the query
        try:
            response = self.langchain_client.send_query(query)
        except Exception as e:
            response = f"Error: {e}"
        self.data_changed.emit()
        self.add_message(response, sender="jarvis")
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def add_message(self, query: str, sender: str) -> QLabel:
        # Adds chat bubbles layout
        chat_bubble = QWidget()
        chat_bubble.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        bubble_layout = QHBoxLayout(chat_bubble)

        # Bubble format and coloring
        label = QLabel(query)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        label.setMaximumWidth(int(self.width() * 0.7))

        if sender == "user":
            label.setStyleSheet(
                "background-color: gray; color: white; padding: 5px 10px; border-radius: 15px"
            )
            bubble_layout.addStretch()
            bubble_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignRight)
        if sender == "jarvis":
            # Jarvis logo
            jarvis_logo = QLabel()
            jarvis_pixmap = QPixmap("jarvis.png")
            jarvis_logo.setPixmap(
                jarvis_pixmap.scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio)
            )

            # Style and layout
            label.setStyleSheet(
                "background-color: lightgray; color: black; padding: 5px 10px;border-radius: 15px;"
            )
            bubble_layout.addWidget(jarvis_logo, 0, Qt.AlignmentFlag.AlignBottom)
            bubble_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignVCenter)
            bubble_layout.addStretch()

        self.chat_layout.addWidget(chat_bubble)
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        return label
