
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QListWidgetItem, QMessageBox

from scheduler_config_editor.model import Course, JsonConfig
from scheduler_config_editor.view.course_editor_gui import (
    CourseEditorGUI,
    CoursesEditorWidget,
)


class CourseEditorController:
    """
    Controller for the faculty editor
    """

    def __init__(self, json_config: JsonConfig) -> None:
        self.json_config = json_config
        self.view = CourseEditorGUI(self)
        self.refresh_list()

    def show(self) -> None:
        self.view.show()

    def refresh_list(self) -> None:
        self.view.list.clear()
        for i, course in enumerate(self.json_config.scheduler_config.courses):
            item_text = f"{course.course_id} - {i}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, course)
            item.setData(Qt.ItemDataRole.UserRole + 1, i)
            self.view.list.addItem(item)
        self.view.list.clearSelection()

    def open_edit_course_window(self, item: QListWidgetItem) -> None:
        index = item.data(Qt.ItemDataRole.UserRole + 1)
        course_data = self.json_config.scheduler_config.courses[index]
        if course_data:
            edit_window = CoursesEditorWidget(self, course_data, index)
            edit_window.show()
            self.view.open_editing_window.append(edit_window)

    def open_add_course_window(self) -> None:
        add_window = CoursesEditorWidget(self)
        add_window.show()
        self.view.open_editing_window.append(add_window)

    def delete_course(self, edit_window: CoursesEditorWidget) -> None:
        course_id = edit_window.course_id_line_edit.text()
        confirm = QMessageBox.question(
            edit_window, "Confirm Delete Course",
            f"Are you sure you want to delete course: {course_id}?",
            QMessageBox.StandardButton.Yes  | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                if edit_window.index is not None:
                    Course.del_course(edit_window.index, self.json_config)
                    self.json_config.save()
                    del_message = QMessageBox()
                    del_message.setWindowTitle("Success")
                    del_message.setText(f"Successfully deleted course: {course_id}")
                    del_message.show()
                    QTimer.singleShot(2500, del_message.close)
                    self.refresh_list()
                    edit_window.close()

            except Exception as error:
                QMessageBox.warning(edit_window, "Error", f"Failed to delete course: {course_id}: {error}")


    def save_course (self, edit_window: CoursesEditorWidget) -> None:
        try:
            course_id = edit_window.course_id_line_edit.text()
            course_credits = int(edit_window.course_credits_line_edit.text())

            # Stores selected rooms, labs, faculty, conflicts
            rooms = [item.text() for item in edit_window.room_list.selectedItems()]
            labs = [item.text() for item in edit_window.lab_list.selectedItems()]
            conflicts = [item.text() for item in edit_window.course_conflicts_list.selectedItems()]
            faculty = [item.text() for item in edit_window.faculty_list.selectedItems()]

            if edit_window.course_data and edit_window.index is not None:
                Course.mod_course(index = edit_window.index,
                    json_config=self.json_config,
                    course_id=course_id,
                    course_credits=course_credits,
                    room = rooms,
                    lab = labs,
                    conflicts = conflicts,
                    faculty = faculty
                )
            else:
                Course.add_course(json_config = self.json_config,
                    course_id = course_id,
                    course_credits = course_credits,
                    room = rooms,
                    lab = labs,
                    conflicts = conflicts,
                    faculty = faculty
                )
            self.json_config.save()

            # Save message and close window
            save_message = QMessageBox()
            save_message.setWindowTitle("Success")
            if edit_window.course_data:
                save_message.setText("Successfully saved edits to " + course_id)
            else:
                save_message.setText("Successfully added course: " + course_id)
            save_message.show()
            QTimer.singleShot(2500, save_message.close)
            self.refresh_list()
            edit_window.close()

        except ValueError as error:
            QMessageBox.warning(edit_window, "Input Error", str(error))