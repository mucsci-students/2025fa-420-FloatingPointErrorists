from PyQt6 import QtGui
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMainWindow,
    QLabel,
)

from scheduler_config_editor.model.langchain_client import LangchainClient
from scheduler_config_editor.model import JsonConfig


class QueryWorker(QThread):
    """Worker thread to run Langchain queries without blocking the GUI."""

    result_ready = pyqtSignal(str)

    def __init__(self, client, message) -> None:
        super().__init__()
        self.client = client
        self.message = message

    def run(self) -> None:
        try:
            response = self.client.send_query(self.message)
        except Exception as e:
            response = f"Error: {e}"
        self.result_ready.emit(response)


class JarvisGUI(QMainWindow):
    """Main GUI window for J.A.R.V.I.S interaction."""

    data_changed = pyqtSignal()

    def __init__(self, json_config: JsonConfig) -> None:
        super().__init__()

        # Screen size
        screen = QGuiApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            screen_width, screen_height = geom.width(), geom.height()
        else:
            screen_width, screen_height = 1920, 1080

        # Window setup
        self.setWindowTitle("J.A.R.V.I.S")
        self.setWindowIcon(QtGui.QIcon("assets/jarvis.png"))
        self.resize(int(screen_width * 0.4), int(screen_height * 0.75))

        # Message history
        self.history = []
        self.history_index = -1
        self.worker = None

        # Main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        main_layout.addWidget(self.chat_display)

        # Thinking indicator
        self.thinking_label = QLabel("")
        self.thinking_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thinking_label.setStyleSheet("color: gray; font-style: italic;")
        main_layout.addWidget(self.thinking_label)

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask J.A.R.V.I.S using format Jarvis, ...")
        self.input_field.returnPressed.connect(self.use_input)
        input_layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.use_input)
        input_layout.addWidget(send_button)
        main_layout.addLayout(input_layout)

        # LangChain client
        self.langchain_client = LangchainClient(json_config)

        # Thinking animation
        self.dot_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_thinking)

    def use_input(self) -> None:
        """Handle user input and send query to Langchain."""
        query = self.input_field.text().strip()
        if not query:
            return

        self.add_message(query)
        self.input_field.clear()
        self.history.append(query)
        self.history_index = -1

        # Start thinking animation
        self.thinking_label.setText("Jarvis is thinking")
        self.dot_count = 0
        self.timer.start(500)

        # Run Langchain in thread
        self.worker = QueryWorker(self.langchain_client, query)
        self.worker.result_ready.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, response: str) -> None:
        """Handle response from Langchain."""
        self.timer.stop()
        self.thinking_label.setText("")
        self.data_changed.emit()

        # Format newlines for QTextEdit
        safe_response = (
            response.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("  ", "&nbsp;&nbsp;")
            .replace("\n", "<br>")
            .replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        )
        self.chat_display.append(f"<b>Jarvis:</b><br>{safe_response}<br>")

    def add_message(self, text: str) -> None:
        """Add a message to the chat display."""
        self.chat_display.append(f"<b>You:</b> {text}<br>")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def animate_thinking(self) -> None:
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.thinking_label.setText(f"Jarvis is thinking{dots}")

    def keyPressEvent(self, event: QtGui.QKeyEvent | None) -> None:
        """Up/Down arrow recall for previous messages."""
        if self.input_field.hasFocus():
            if event.key() == Qt.Key.Key_Up:
                self.show_previous_message()
            elif event.key() == Qt.Key.Key_Down:
                self.show_next_message()
        super().keyPressEvent(event)

    def show_previous_message(self) -> None:
        if not self.history:
            return
        if self.history_index == -1:
            self.history_index = len(self.history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.input_field.setText(self.history[self.history_index])

    def show_next_message(self) -> None:
        if not self.history:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input_field.setText(self.history[self.history_index])
        else:
            self.history_index = -1
            self.input_field.clear()
