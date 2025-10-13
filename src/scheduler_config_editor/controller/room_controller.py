from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox, QListWidget, QListWidgetItem, QGroupBox, QVBoxLayout, QPushButton, QTextEdit, QLabel

from scheduler_config_editor.model import Room, Lab,JsonConfig

class RoomEditorController:
    def __init__(self, json_config: JsonConfig) -> None:
        from scheduler_config_editor.view.room_editor_gui import RoomEditorGui
        self.json_config = json_config
        self.room_view = RoomEditorGui(self)
        self.populate_lists()
        self.room_view.repaint()

    def populate_lists(self) -> None:
        self.room_view.room_list.clear()
        self.room_view.lab_list.clear()
        for i, room in enumerate (self.json_config.scheduler_config.rooms):
            self.room_view.room_list.addItem(self.json_config.scheduler_config.rooms[i])

        for i, lab in enumerate (self.json_config.scheduler_config.labs):
            self.room_view.lab_list.addItem(self.json_config.scheduler_config.labs[i])


    def show_editor(self, item: QListWidgetItem, group: str) -> None:
        editor_box = self.get_editor(item, group)
        if self.room_view.my_layout.count() != 4:
            self.room_view.my_layout.addWidget(editor_box)
            self.current_editor = editor_box
        else:
            self.room_view.my_layout.replaceWidget(self.current_editor, editor_box)
            self.current_editor.setParent(None)
            self.current_editor = editor_box

    def get_editor(self, item: QListWidgetItem, group: str) -> QGroupBox:
        # Editor Group Box
        editor_box = QGroupBox(f"{group} Editor")
        editor_layout = QVBoxLayout()
        editor_box.setLayout(editor_layout)

        # Adds a text box to add/edit name
        editor_textbox = QTextEdit()
        editor_textbox.setPlaceholderText(f"{group} name...")
        editor_layout.addWidget(editor_textbox)

        # Adds a button to delete the selected room
        #   IF clicked on item from a list
        editor_del_button = QPushButton("Delete")
        editor_del_button.setHidden(True)

        # Sets the text box editor to a name if clicked on item from list
        name = ""
        if type(item) is QListWidgetItem:
            name = item.text()
            editor_del_button.setVisible(True)
        editor_textbox.setText(name)

        # Defines a function for writing out to the json
        def save() -> None:
            self.write_out(editor_textbox.toPlainText(), name, group)
            self.populate_lists()
            editor_box.setHidden(True)
            self.room_view.my_layout.removeWidget(editor_box)

        editor_save_button = QPushButton("Save")
        editor_save_button.clicked.connect(save)
        editor_layout.addWidget(editor_save_button)

        def enable_save() -> None:
            if editor_textbox.toPlainText() != name:
                editor_save_button.setDisabled(False)
            else:
                editor_save_button.setDisabled(True)

        editor_textbox.textChanged.connect(enable_save)
        editor_save_button.setDisabled(True)

        # Defines a function for deleting from the json
        def delete() -> None:
            from scheduler_config_editor.view.room_editor_gui import RoomEditorGui
            if group == RoomEditorGui.ROOM:
                try:
                    Room.del_room(self.json_config, name)
                except Room.RoomMissingError as e:
                    self.show_error(group, e)
            elif group == RoomEditorGui.LAB:
                try:
                    Lab.del_lab(self.json_config, name)
                except Lab.LabMissingError as e:
                    self.show_error(group, e)

            self.populate_lists()
            editor_box.setHidden(True)
            self.room_view.my_layout.removeWidget(editor_box)

        editor_del_button.clicked.connect(delete)
        editor_layout.addWidget(editor_del_button)

        def cancel() -> None:
            self.populate_lists()
            editor_box.setHidden(True)
            self.room_view.my_layout.removeWidget(editor_box)

        editor_cancel_button = QPushButton("Cancel")
        editor_cancel_button.clicked.connect(cancel)
        editor_layout.addWidget(editor_cancel_button)

        #self.my_layout.addWidget(editor_box)
        return editor_box

    def write_out(self, name: str, oName: str, group: str) -> None:
        from scheduler_config_editor.view.room_editor_gui import RoomEditorGui
        if group == RoomEditorGui.ROOM:
            if oName != "":
                Room.mod_room(self.json_config, oName, name)
            else:
                try:
                    Room.add_room(self.json_config, name)
                except Room.RoomExistsError as e:
                    self.show_error(group, e)
        elif group == RoomEditorGui.LAB:
            if oName != "":
                Lab.mod_lab(self.json_config, oName, name)
            else:
                try:
                    Lab.add_lab(self.json_config, name)
                except Lab.LabExistsError as e:
                    self.show_error(group, e)
            
    def show_error(self, group: str, error: Exception) -> None:
        error_box = QMessageBox()
        error_box.setWindowTitle(f"{group} Error")
        error_box.setText(f"{error}")
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        error_box.exec()