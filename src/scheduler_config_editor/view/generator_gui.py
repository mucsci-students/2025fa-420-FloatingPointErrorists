import sys
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QIntValidator
from scheduler_config_editor.view.base_gui import SimpleTabs

sys.path.append('../controller')

def setup_generator_tab(tabs_instance: SimpleTabs) -> None:

    # layout
    tabs_instance.generator_layout = QVBoxLayout()
    tabs_instance.generator_tab.setLayout(tabs_instance.generator_layout)

    generator_layout = tabs_instance.generator_layout

    # === 1. Section: Optimization Flags ===
    flags_group = QGroupBox("Optimization Flags")
    flags_layout = QVBoxLayout()

    # We'll store checkboxes in case you want to access them later
    tabs_instance.optimizer_checkboxes = []

    for i in range(7):
        checkbox = QCheckBox(f"Flag {i+1}")
        flags_layout.addWidget(checkbox)
        tabs_instance.optimizer_checkboxes.append(checkbox)

    flags_group.setLayout(flags_layout)
    generator_layout.addWidget(flags_group)

    # === 2. Section: Limit Input ===
    limit_group = QGroupBox("Schedule Generation Limit")
    limit_layout = QHBoxLayout()

    limit_label = QLabel("Max schedules:")
    limit_input = QLineEdit()
    limit_input.setPlaceholderText("Enter a non-negative integer")
    limit_input.setValidator(QIntValidator(0, 99999))  # Only allows non-negative ints

    tabs_instance.limit_input = limit_input  # Save if you need access later

    limit_layout.addWidget(limit_label)
    limit_layout.addWidget(limit_input)
    limit_group.setLayout(limit_layout)
    generator_layout.addWidget(limit_group)

    # === 3. Generate Button ===
    generate_button = QPushButton("Generate")
    generator_layout.addWidget(generate_button)

    # === 4. Placeholder generate button behavior ===
    def on_generate():
        selected_flags = [cb.isChecked() for cb in tabs_instance.optimizer_checkboxes]
        limit_value = limit_input.text() or "0"
        QMessageBox.information(
            tabs_instance,
            "Generation Triggered",
            f"Selected Flags: {selected_flags}\nLimit: {limit_value}"
        )

    generate_button.clicked.connect(on_generate)

    # # Add a label
    # label = QLabel("Welcome to the Generator tab!")
    # generator_layout.addWidget(label)
    #
    # # Add a line edit
    # input_box = QLineEdit()
    # input_box.setPlaceholderText("Enter something...")
    # generator_layout.addWidget(input_box)
    #
    # # Add a button
    # button = QPushButton("Generate!")
    # generator_layout.addWidget(button)
    #
    # # Connect button to a function
    # def on_generate_clicked():
    #     user_input = input_box.text()
    #     QMessageBox.information(tabs_instance, "Generator Output", f"You entered: {user_input}")
    #
    # button.clicked.connect(on_generate_clicked)
