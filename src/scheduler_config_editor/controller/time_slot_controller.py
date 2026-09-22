from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
from scheduler import TimeBlock, Meeting

from scheduler_config_editor.model import JsonConfig, TimeSlot
from scheduler_config_editor.view.time_slot_editor_gui import TimeSlotEditorGui


class TimeSlotController:
    """ "
    Controller for the time slot editor.
    """

    def __init__(self, json_config: JsonConfig) -> None:
        self.json_config = json_config
        self.view = TimeSlotEditorGui(self)
        self.refresh_list()

    def show(self) -> None:
        self.view.show()

    def get_time_blocks(self, day: str) -> list[TimeBlock]:
        times_dict = dict(self.json_config.time_slot_config.times)
        return times_dict.get(day, [])

    def get_class_patterns(self):
        return self.json_config.time_slot_config.classes

    def refresh_list(self) -> None:
        self.view.load_time_blocks()
        self.view.load_class_patterns()

    def open_edit_time_block_window(self, day: str, index: int) -> None:
        self.view.open_time_block_editor(day, index)

    def open_add_time_block_window(self, day: str) -> None:
        self.view.open_time_block_editor(day, None)

    def open_edit_class_pattern_window(self, index: int) -> None:
        self.view.open_class_pattern_editor(index)

    def open_add_class_pattern_window(self) -> None:
        self.view.open_class_pattern_editor(None)

    def add_time_block(
        self, day_index: int, start: str, spacing: int, end: str
    ) -> None:
        TimeSlot.add_time_block(
            json_config=self.json_config,
            day_index=day_index,
            start=start,
            spacing=spacing,
            end=end,
        )
        # Save message
        save_message = QMessageBox(self.view)
        save_message.setWindowTitle("Success")
        save_message.setText("Time block added successfully.")
        save_message.show()
        QTimer.singleShot(2500, save_message.close)
        self.refresh_list()

    def mod_time_block(
        self, day_index: int, index: int, start: str, spacing: int, end: str
    ) -> None:
        TimeSlot.mod_time_block(
            json_config=self.json_config,
            day_index=day_index,
            index=index,
            start=start,
            spacing=spacing,
            end=end,
        )
        # Save message
        save_message = QMessageBox(self.view)
        save_message.setWindowTitle("Success")
        save_message.setText("Time block updated successfully.")
        save_message.show()
        QTimer.singleShot(2500, save_message.close)
        self.refresh_list()

    def del_time_block(self, day_index: int, index: int) -> None:
        confirm = QMessageBox.question(
            self.view,
            "Confirm Delete",
            "Are you sure you want to delete this time block?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                TimeSlot.del_time_block(
                    json_config=self.json_config, day_index=day_index, index=index
                )
                self.json_config.save()
                del_message = QMessageBox()
                del_message.setWindowTitle("Success")
                del_message.setText("Successfully deleted time block")
                del_message.show()
                QTimer.singleShot(2500, del_message.close)
                self.refresh_list()

            except Exception as error:
                QMessageBox.warning(
                    self.view,
                    "Error",
                    f"Failed to delete time block: {error}",
                )

    def add_class_pattern(
        self,
        creds: int,
        meetings: list[Meeting],
        disabled: bool,
        start_time: str | None,
    ) -> None:
        TimeSlot.add_class_pattern(
            json_config=self.json_config,
            creds=creds,
            meetings=meetings,
            disabled=disabled,
            start_time=start_time,
        )
        # Save message
        save_message = QMessageBox(self.view)
        save_message.setWindowTitle("Success")
        save_message.setText("Class pattern added successfully.")
        save_message.show()
        QTimer.singleShot(2500, save_message.close)
        self.refresh_list()

    def mod_class_pattern(
        self,
        index: int,
        creds: int,
        meetings: list[Meeting],
        disabled: bool,
        start_time: str | None,
    ) -> None:
        TimeSlot.mod_class_pattern(
            json_config=self.json_config,
            index=index,
            creds=creds,
            meetings=meetings,
            disabled=disabled,
            start_time=start_time,
        )
        # Save message
        save_message = QMessageBox(self.view)
        save_message.setWindowTitle("Success")
        save_message.setText("Class pattern updated successfully.")
        save_message.show()
        QTimer.singleShot(2500, save_message.close)
        self.refresh_list()

    def del_class_pattern(self, index: int) -> None:
        confirm = QMessageBox.question(
            self.view,
            "Confirm Delete",
            "Are you sure you want to delete this class pattern?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                TimeSlot.del_class_pattern(json_config=self.json_config, index=index)
                self.json_config.save()
                del_message = QMessageBox()
                del_message.setWindowTitle("Success")
                del_message.setText("Successfully deleted class pattern")
                del_message.show()
                QTimer.singleShot(2500, del_message.close)
                self.refresh_list()

            except Exception as error:
                QMessageBox.warning(
                    self.view,
                    "Error",
                    f"Failed to delete class pattern: {error}",
                )
