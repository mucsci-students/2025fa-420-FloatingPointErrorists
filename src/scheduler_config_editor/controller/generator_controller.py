import sys
from scheduler import OptimizerFlags
from scheduler_config_editor.model.json import JsonConfig
from PyQt6.QtWidgets import QCheckBox, QLineEdit
from scheduler.models import CourseInstance
from scheduler_config_editor.model.run_scheduler import run_using_config

sys.path.append('../controller')

def generate(checkboxes: list[QCheckBox], limit: QLineEdit, config: JsonConfig) -> list[list[CourseInstance]]:
    if not config:
        raise ConfigMissingError("No config provided.")

    optimizer_map = {}
    selected_flags = []

    # Finding which optimizations to set
    for fg, cbox in zip(OptimizerFlags, checkboxes):
        is_checked = cbox.isChecked()
        optimizer_map[fg] = is_checked

        if is_checked:
            selected_flags.append(fg)

    # Getting limit
    limit_value = limit.text() or "0"
    config.set_optimization(selected_flags)
    config.set_limit(limit_value)

    return run_using_config(config.combined_config)

class ConfigMissingError(Exception):
    """Raised when config is missing for generation"""
    pass
