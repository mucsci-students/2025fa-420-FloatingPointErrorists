from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox
from scheduler import TimeRange

from scheduler_config_editor.model import Faculty, JsonConfig
from scheduler_config_editor.view.faculty_editor_gui import (
    EditFacultyWindow,
    FacultyEditorGui,
)


class FacultyEditorController:
    """
    Controller for the faculty editor
    """

    def __init__(self, json_config: JsonConfig) -> None:
        self.json_config = json_config
        self.view = FacultyEditorGui(self)
        self.refresh_list()

    def show(self) -> None:
        self.view.show()

    def refresh_list(self) -> None:
        self.view.list.clear()
        for i, _faculty in enumerate(self.json_config.scheduler_config.faculty):
            self.view.list.addItem(self.json_config.scheduler_config.faculty[i].name)
        self.view.list.clearSelection()

    def open_edit_faculty_window(self, item: QListWidgetItem) -> None:
        name = item.text()
        for i, _faculty in enumerate(self.json_config.scheduler_config.faculty):
            if self.json_config.scheduler_config.faculty[i].name == name:
                index = i
                break
        faculty_data = self.json_config.scheduler_config.faculty[index]
        if faculty_data:
            edit_window = EditFacultyWindow(self, faculty_data)
            edit_window.show()

    def open_add_faculty_window(self) -> None:
        add_window = EditFacultyWindow(self)
        add_window.show()

    def delete_faculty(self, edit_window: EditFacultyWindow) -> None:
        name = edit_window.name_edit.text()
        confirm = QMessageBox.question(
            edit_window, "Confirm Delete Faculty",
            f"Are you sure you want to delete faculty member: {name}?",
            QMessageBox.StandardButton.Yes  | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                Faculty.del_faculty(self.json_config, name)
                self.json_config.save()
                del_message = QMessageBox()
                del_message.setWindowTitle("Success")
                del_message.setText(f"Successfully deleted faculty member: {name}")
                del_message.show()
                QTimer.singleShot(2500, del_message.close)
                self.refresh_list()
                edit_window.close()

            except Exception as error:
                QMessageBox.warning(edit_window, "Error", f"Failed to delete faculty member: {name}: {error}")


    def save_faculty (self, edit_window: EditFacultyWindow) -> None:
        try:
            # Validate input
            name = edit_window.name_edit.text()
            minimum_creds = int(edit_window.min_credits_edit.text())
            maximum_creds = int(edit_window.max_credits_edit.text())
            course_limit = int(edit_window.course_limit_edit.text())

            if 0 > maximum_creds:
                raise ValueError("Maximum credits must be greater than or equal to 0.")
            if 0 > minimum_creds:
                raise ValueError("Minimum credits must be greater than or equal to 0.")
            if minimum_creds > maximum_creds:
                raise ValueError("Minimum credits must be less than or equal to maximum credits.")
            if 1 > course_limit:
                raise ValueError("Course limit must be a positive integer.")

            times = {}
            for day, widgets in edit_window.day_interval_widgets.items():
                intervals = []
                for start_edit, end_edit, _ in widgets["intervals"]:
                    start = start_edit.time()
                    end = end_edit.time()
                    if start >= end:
                        QMessageBox.warning(edit_window, "Error", f"On {day}, start time must be before end time.")
                        return
                    interval = TimeRange(start = start.toString("HH:mm"), end = end.toString("HH:mm"))
                    intervals.append(interval)
                if intervals:
                    times[day] = intervals

            if len(times) == 0:
                QMessageBox.warning(edit_window, "Error", "Faculty must have at least one available time interval.")
                return

            room_preferences = {
                room: edit_window.room_preference_input[room].value()
                for room in edit_window.room_preference_input
            }

            course_preferences = {
                course: edit_window.course_preference_input[course].value()
                for course in edit_window.course_preference_input
            }

            lab_preferences = {
                    lab: edit_window.lab_preference_input[lab].value()
                    for lab in edit_window.lab_preference_input
            }

            if edit_window.faculty_data:
                old_name = edit_window.faculty_data.name
                Faculty.mod_faculty(self.json_config,
                    old_name = old_name,
                    new_name = name,
                    maximum_credits=int(edit_window.max_credits_edit.text()),
                    minimum_credits = int(edit_window.min_credits_edit.text()),
                    unique_course_limit = int(edit_window.course_limit_edit.text()),
                    times = times,
                    course_preferences = course_preferences,
                    room_preferences = room_preferences,
                    lab_preferences = lab_preferences)
            else:
                Faculty.add_faculty(self.json_config,
                    name = name,
                    maximum_credits=int(edit_window.max_credits_edit.text()),
                    minimum_credits = int(edit_window.min_credits_edit.text()),
                    unique_course_limit = int(edit_window.course_limit_edit.text()),
                    times = times,
                    course_preferences = course_preferences,
                    room_preferences = room_preferences,
                    lab_preferences = lab_preferences,
                )
            self.json_config.save()

            # Save message and close window
            save_message = QMessageBox()
            save_message.setWindowTitle("Success")
            if edit_window.faculty_data:
                save_message.setText("Successfully saved edits to " + name)
            else:
                save_message.setText("Successfully added faculty member: " + name)
            save_message.show()
            QTimer.singleShot(2500, save_message.close)
            self.refresh_list()
            edit_window.close()

        except ValueError as error:
            QMessageBox.warning(edit_window, "Input Error", str(error))
