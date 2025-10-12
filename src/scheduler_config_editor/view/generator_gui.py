import sys
from typing import Callable

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QMessageBox, QGroupBox, QMainWindow, QTabWidget, QWidget
)
from PyQt6.QtGui import QIntValidator
from scheduler import OptimizerFlags
from scheduler_config_editor.model.json import JsonConfig
from scheduler.models import CourseInstance

sys.path.append('../controller')

class GeneratorGui(QWidget):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.config
        self.generator_layout = QVBoxLayout()
        self.schedules = []
        self.optimizer_checkboxes = []
        self.limit_input = QLineEdit()
        self.setup_generator_tab()

    def setup_generator_tab(self) -> None:
        # === Layout Setup ===
        self.setLayout(self.generator_layout)

        generator_layout = self.generator_layout

        # === Optimization Flags ===
        flags_group = QGroupBox("Optimization Flags")
        flags_layout = QVBoxLayout()

        # Checkboxes
        for flag in OptimizerFlags:
            checkbox = QCheckBox(f"{flag} optimization")
            flags_layout.addWidget(checkbox)
            self.optimizer_checkboxes.append(checkbox)

        flags_group.setLayout(flags_layout)
        generator_layout.addWidget(flags_group)

        # === Limit Input ===
        limit_group = QGroupBox("Schedule Generation Limit")
        limit_layout = QHBoxLayout()

        limit_label = QLabel("Max schedules:")
        self.limit_input.setPlaceholderText("Enter a positive integer")
        self.limit_input.setValidator(QIntValidator(1, 99999999))  # Only allows positive ints

        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.limit_input)
        limit_group.setLayout(limit_layout)
        generator_layout.addWidget(limit_group)

        # === Generate Button ===
        generate_button = QPushButton("Generate")
        generator_layout.addWidget(generate_button)

        generate_button.clicked.connect(self.controller.on_generate_clicked)

    def update_config(self, config: JsonConfig) -> None:
        self.json_config = config

    def get_limit(self) -> str:
        return self.limit_input.text()

    def get_checks(self) -> list[QCheckBox]:
        return self.optimizer_checkboxes
