import sys
from typing import Callable

from scheduler import OptimizerFlags, Scheduler
from scheduler_config_editor.model.json import JsonConfig
from PyQt6.QtWidgets import QCheckBox, QLineEdit, QMessageBox
from scheduler.models import CourseInstance
from scheduler_config_editor.model.run_scheduler import run_using_config
from scheduler_config_editor.view.generator_gui import GeneratorGui

sys.path.append('../controller')

class GeneratorController:
    def __init__(self, config: JsonConfig) -> None:
        self.config = config
        self.view = GeneratorGui(self)
        self.schedules = None
        self.on_schedules_generated: Callable[[list[list[CourseInstance]]], None] = None  # callback

    def show(self) -> None:
        self.view.show()

    def generate(self) -> list[list["CourseInstance"]]:
        if self.config is None:
            raise ConfigMissingError("No config provided.")

        selected_flags: list[OptimizerFlags] = []

        optimizations = [
            OptimizerFlags.FACULTY_COURSE,
            OptimizerFlags.FACULTY_ROOM,
            OptimizerFlags.FACULTY_LAB,
            OptimizerFlags.SAME_ROOM,
            OptimizerFlags.SAME_LAB,
            OptimizerFlags.PACK_ROOMS,
            OptimizerFlags.PACK_LABS,
        ]

        check_list = self.view.get_checks()
        for i in range(7):
            if check_list[i].isChecked():
                selected_flags.append(optimizations[i])

        # Getting limit
        limit_value = self.view.get_limit()

        self.config.set_optimization(selected_flags)
        # self.config.combined_config.optimizer_flags = selected_flags
        self.config.set_limit(int(limit_value))

        schedules = run_using_config(self.config.combined_config)

        return schedules

    def on_generate_clicked(self) -> None:
        try:
            self.schedules = self.generate()
            QMessageBox.information(self.view, "Generation Complete", f"Generation Complete")

            if self.on_schedules_generated:
                self.on_schedules_generated(self.schedules)
        except ConfigMissingError as e:
            QMessageBox.critical(self.view, "Error", str(e))
        except Exception as e:
            # Catch-all for other unexpected issues
            QMessageBox.critical(self.view, "Unexpected Error", str(e))

    def update_config(self, config: JsonConfig) -> None:
        self.config = config

class ConfigMissingError(Exception):
    """Raised when config is missing for generation"""
    pass
