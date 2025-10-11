import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from scheduler_config_editor.view.base_gui import SimpleGUI, SimpleTabs
from generator_gui import setup_generator_tab

def view() -> None:
    app = QApplication(sys.argv)
    window = SimpleGUI()
    setup_generator_tab(window.tab_widget)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    view()
    