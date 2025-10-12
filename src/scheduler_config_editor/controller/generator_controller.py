from typing import Callable
from scheduler import OptimizerFlags
from scheduler_config_editor.model.json import JsonConfig
from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from scheduler.models import CourseInstance
from scheduler_config_editor.model.run_scheduler import run_using_config
from scheduler_config_editor.view.generator_gui import GeneratorGui

# ---- Worker Thread (runs the heavy computation) ----
class RunWorker(QThread):
    """Worker thread to run the scheduler without blocking the GUI."""
    finished_success = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, config: JsonConfig):
        super().__init__()
        self.config = config

    def run(self):
        try:
            # Run your scheduler here
            result = run_using_config(self.config.combined_config)
            self.finished_success.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ---- Simple Popup with Loading Bar ----
class LoadingDialog(QDialog):
    """A simple modal dialog with a loading bar."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generating schedules...")
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)

        layout = QVBoxLayout()
        self.label = QLabel("Please wait while schedules are generated...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # infinite animation

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)


# ---- Controller ----
class GeneratorController:
    """
    Controller for the schedule generator GUI
    """
    def __init__(self, config: JsonConfig) -> None:
        self.config = config
        self.view = GeneratorGui(self)
        self.schedules = None
        self.on_schedules_generated: Callable[[list[list[CourseInstance]]], None] = None  # callback
        self.worker = None
        self.loading = None

    def _prepare_config(self) -> None:
        """Read user selections and update config before running."""
        selected_flags = []
        for fg, cbox in zip(OptimizerFlags, self.view.get_checks()):
            if cbox.isChecked():
                selected_flags.append(fg)

        limit_value = self.view.get_limit() or self.config.combined_config.limit
        self.config.set_optimization(selected_flags)
        self.config.set_limit(int(limit_value))

    def on_generate_clicked(self) -> None:
        """Handle the Generate button click."""
        if self.config is None:
            QMessageBox.critical(self.view, "Error", "No config provided.")
            return

        try:
            # Prepare configuration from GUI selections
            self._prepare_config()

            # Create and show loading dialog
            self.loading = LoadingDialog(self.view)
            self.loading.show()

            # Create worker thread to run scheduler
            self.worker = RunWorker(self.config)
            self.worker.finished_success.connect(self._on_generation_done)
            self.worker.error_occurred.connect(self._on_generation_error)
            self.worker.finished.connect(self.loading.close)
            self.worker.start()

        except Exception as e:
            QMessageBox.critical(self.view, "Unexpected Error", str(e))

    def _on_generation_done(self, schedules: list[list[CourseInstance]]) -> None:
        """Handle completion of schedule generation."""
        self.schedules = schedules

        if not schedules:
            QMessageBox.information(
                self.view,
                "No Solutions Found",
                "No schedules could be generated with the current configuration."
            )
            return

        QMessageBox.information(
            self.view,
            "Generation Complete",
            "Schedules have been generated successfully."
        )

        if self.on_schedules_generated:
            self.on_schedules_generated(schedules)

    def _on_generation_error(self, message: str) -> None:
        """Handle errors during schedule generation."""
        QMessageBox.critical(self.view, "Unexpected Error", message)

    def update_config(self, config: JsonConfig) -> None:
        """Update the controller's config."""
        self.config = config


# ---- Custom Exception ----
class ConfigMissingError(Exception):
    """Raised when config is missing for generation"""
    pass
