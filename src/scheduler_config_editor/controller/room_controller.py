from PyQt6.QtWidgets import QMessageBox, QListWidgetItem, QVBoxLayout, QPushButton, QTextEdit, QWidget

from scheduler_config_editor.model import Room, Lab,JsonConfig

class RoomEditorController:
    def __init__(self, json_config: JsonConfig) -> None:
        from scheduler_config_editor.view.room_editor_gui import RoomEditorGui
        self.json_config = json_config
        self.room_view = RoomEditorGui(self)
        self.refresh_lists()

    def refresh_lists(self) -> None:
        self.room_view.room_list.clear()
        self.room_view.lab_list.clear()
        for i, room in enumerate (self.json_config.scheduler_config.rooms):
            self.room_view.room_list.addItem(self.json_config.scheduler_config.rooms[i])

        for i, lab in enumerate (self.json_config.scheduler_config.labs):
            self.room_view.lab_list.addItem(self.json_config.scheduler_config.labs[i])


    def show_editor(self, item: QListWidgetItem, group: str) -> None:
        editor_box = self.get_editor(item, group)

        # clear previous editor content
        container_layout = self.room_view.editor_container.layout()
        if container_layout is not None:
            while container_layout.count() > 0:
                layout_item = container_layout.takeAt(0)
                if layout_item is not None:
                    old_widget = layout_item.widget()
                    if old_widget is not None:
                        old_widget.setParent(None)
                        old_widget.deleteLater()
        
            # add new editor content
            container_layout.addWidget(editor_box)

        self.room_view.editor_container.setTitle(f"{group} Editor")
        self.room_view.editor_container.show()

    def get_editor(self, item: QListWidgetItem, group: str) -> QWidget:
        editor_widget = QWidget(parent=self.room_view.editor_container)
        editor_layout = QVBoxLayout()
        editor_widget.setLayout(editor_layout)

        # Adds a text box to add/edit name
        editor_textbox = QTextEdit()
        editor_textbox.setPlaceholderText(f"{group} name...")
        editor_layout.addWidget(editor_textbox)

        # Adds a button to delete the selected room
        #   IF clicked on item from a list
        editor_del_button = QPushButton("Delete")
        editor_del_button.setHidden(True)
        editor_layout.addWidget(editor_del_button)

        # Sets the text box editor to a name if clicked on item from list
        name = ""
        if type(item) is QListWidgetItem:
            name = item.text()
            editor_del_button.setVisible(True)
        editor_textbox.setText(name)

        # Defines a function for writing out to the json
        def save() -> None:
            self.write_out(editor_textbox.toPlainText(), name, group)
            self.refresh_lists()
            self.room_view.editor_container.setHidden(True)

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

            self.refresh_lists()
            self.room_view.editor_container.setHidden(True)

        editor_del_button.clicked.connect(delete)

        def cancel() -> None:
            self.refresh_lists()
            self.room_view.editor_container.setHidden(True)

        editor_cancel_button = QPushButton("Cancel")
        editor_cancel_button.clicked.connect(cancel)
        editor_layout.addWidget(editor_cancel_button)

        #self.my_layout.addWidget(editor_box)
        return editor_widget

    def write_out(self, name: str, oName: str, group: str) -> None:
        from scheduler_config_editor.view.room_editor_gui import RoomEditorGui
        if group == RoomEditorGui.ROOM:
            if oName != "":
                try:
                    Room.mod_room(self.json_config, oName, name)
                except Room.RoomExistsError as e:
                    self.show_error(group, e)
            else:
                try:
                    Room.add_room(self.json_config, name)
                except Room.RoomExistsError as e:
                    self.show_error(group, e)
        elif group == RoomEditorGui.LAB:
            if oName != "":
                try:
                    Lab.mod_lab(self.json_config, oName, name)
                except Lab.LabExistsError as e:
                    self.show_error(group, e)
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