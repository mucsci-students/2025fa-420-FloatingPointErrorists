import sys
from typing import Callable

from scheduler import OptimizerFlags
from scheduler_config_editor.model.json import JsonConfig
from PyQt6.QtWidgets import QMessageBox
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

        selected_flags = []
        # Finding which optimizations to set
        for fg, cbox in zip(OptimizerFlags, self.view.get_checks()):
            is_checked = cbox.isChecked()

            if is_checked:
                selected_flags.append(fg)

        # Getting limit
        limit_value = self.view.get_limit() or self.config.combined_config.limit

        self.config.set_optimization(selected_flags)
        self.config.set_limit(int(limit_value))

        schedules = run_using_config(self.config.combined_config)

        return schedules

    def on_generate_clicked(self) -> None:
        try:
            self.schedules = self.generate()
            if len(self.schedules) == 0:
                QMessageBox.information(self.view, "No Solutions Found", "No schedules could be generated with the current configuration.")
                return
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
