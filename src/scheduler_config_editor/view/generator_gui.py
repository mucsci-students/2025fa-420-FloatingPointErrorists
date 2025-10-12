import sys
from typing import Callable

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QIntValidator
from scheduler_config_editor.view.base_gui import SimpleTabs
from scheduler import OptimizerFlags
from scheduler_config_editor.model.json import JsonConfig
from scheduler_config_editor.controller.generator_controller import generate, ConfigMissingError
from scheduler.models import CourseInstance

sys.path.append('../controller')

def setup_generator_tab(tabs_instance: SimpleTabs,
                        on_schedules_generated: Callable[[list[list[CourseInstance]]], None]) -> None:
    # === Layout Setup ===
    tabs_instance.generator_layout = QVBoxLayout()
    tabs_instance.generator_tab.setLayout(tabs_instance.generator_layout)

    generator_layout = tabs_instance.generator_layout

    # === Optimization Flags ===
    flags_group = QGroupBox("Optimization Flags")
    flags_layout = QVBoxLayout()

    # Checkboxes
    optimizer_checkboxes = []

    for flag in OptimizerFlags:
        checkbox = QCheckBox(f"{flag} optimization")
        flags_layout.addWidget(checkbox)
        optimizer_checkboxes.append(checkbox)

    flags_group.setLayout(flags_layout)
    generator_layout.addWidget(flags_group)

    # === Limit Input ===
    limit_group = QGroupBox("Schedule Generation Limit")
    limit_layout = QHBoxLayout()

    limit_label = QLabel("Max schedules:")
    limit_input = QLineEdit()
    limit_input.setPlaceholderText("Enter a positive integer")
    limit_input.setValidator(QIntValidator(1, 99999999))  # Only allows positive ints

    tabs_instance.limit_input = limit_input  # Save

    limit_layout.addWidget(limit_label)
    limit_layout.addWidget(limit_input)
    limit_group.setLayout(limit_layout)
    generator_layout.addWidget(limit_group)

    # === Generate Button ===
    generate_button = QPushButton("Generate")
    generator_layout.addWidget(generate_button)

    def on_generate_clicked() -> None:
        try:
            schedules = generate(optimizer_checkboxes, limit_input, tabs_instance.config)
            # Pass the generated schedules back using the callback
            on_schedules_generated(schedules)
            QMessageBox.information(tabs_instance, "Generation Complete", f"Generation Complete")
        except ConfigMissingError as e:
            QMessageBox.critical(tabs_instance, "Error", str(e))
        except Exception as e:
            # Catch-all for other unexpected issues
            QMessageBox.critical(tabs_instance, "Unexpected Error", str(e))

    generate_button.clicked.connect(on_generate_clicked)
