import sys
from typing import TYPE_CHECKING

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from scheduler.models import CourseInstance

if TYPE_CHECKING:
    from scheduler_config_editor.controller.generator_controller import (
        GeneratorController,
    )

from scheduler_config_editor.model.json_config import JsonConfig

sys.path.append("../controller")


class GeneratorGui(QDialog):
    def __init__(self, controller: "GeneratorController") -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.config
        self.generator_layout = QVBoxLayout()
        self.schedules: list[list[CourseInstance]] = []
        self.optimizer_checkboxes: list[QCheckBox] = []
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
        flag_descs = [
            "Optimize faculty course assignments using preferences",
            "Optimize faculty room assignments using preferences",
            "Optimize faculty lab assignments using preferences",
            "Force same room usage for courses taught by the same faculty",
            "Force same lab usage for courses taught by the same faculty",
            "Optimize packing of rooms for courses taught",
            "Optimize packing of labs for courses taught",
        ]

        for flag in flag_descs:
            checkbox = QCheckBox(flag)
            flags_layout.addWidget(checkbox)
            self.optimizer_checkboxes.append(checkbox)

        flags_group.setLayout(flags_layout)
        generator_layout.addWidget(flags_group)

        # === Limit Input ===
        limit_group = QGroupBox("Schedule Generation Limit")
        limit_layout = QHBoxLayout()

        limit_label = QLabel("Max schedules:")
        self.limit_input.setPlaceholderText("Enter a positive integer")
        self.limit_input.setValidator(
            QIntValidator(1, 99999999)
        )  # Only allows positive ints
        self.limit_input.setToolTip(
            "Set a limit on number of schedules to generate. If left empty, defaults to 1."
        )

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
