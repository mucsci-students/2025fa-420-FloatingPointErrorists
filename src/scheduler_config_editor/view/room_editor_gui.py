import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QTextEdit, QPushButton, QVBoxLayout, QMainWindow, QListWidget, QListWidgetItem, QMessageBox, QGroupBox
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

import scheduler_config_editor
from scheduler_config_editor.model import Room, Lab, JsonConfig

class RoomEditorGui(QMainWindow):
    ROOM = "Room"
    LAB = "Lab"

    def __init__(self, json_config: JsonConfig) -> None:
        super().__init__()
        self.json_config = json_config

        # Layout Stuff
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.my_layout = QVBoxLayout()
        central_widget.setLayout(self.my_layout)

        my_screen = QGuiApplication.primaryScreen()
        if my_screen is not None:
            screen_geometry = my_screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
            self.resize(int(screen_width * 0.5), int(screen_height * 0.5))
        
        # Changes title
        self.title = QLabel("Room and Lab Editor")
        self.my_layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)

        # Room Group Box
        room_group_box = QGroupBox("Rooms")
        room_layout = QVBoxLayout()
        room_group_box.setLayout(room_layout)

        self.room_list = QListWidget(self)
        room_layout.addWidget(self.room_list)

        room_add_button = QPushButton("Add Room")
        room_add_button.clicked.connect(lambda item: self.show_editor(item, RoomEditorGui.ROOM))
        room_layout.addWidget(room_add_button)

        self.room_list.itemClicked.connect(lambda item: self.show_editor(item, RoomEditorGui.ROOM))

        # Labs Group Box
        lab_group_box = QGroupBox("Labs")
        lab_layout = QVBoxLayout()
        lab_group_box.setLayout(lab_layout)

        self.lab_list = QListWidget(self)
        lab_layout.addWidget(self.lab_list)

        lab_add_button = QPushButton("Add Lab")
        lab_add_button.clicked.connect(lambda item: self.show_editor(item, RoomEditorGui.LAB))
        lab_layout.addWidget(lab_add_button)

        self.lab_list.itemClicked.connect(lambda item: self.show_editor(item, RoomEditorGui.LAB))

        self.populate_lists()

        self.my_layout.addWidget(room_group_box)
        self.my_layout.addWidget(lab_group_box)
    

    def populate_lists(self) -> None:
        self.room_list.clear()
        self.lab_list.clear()
        for i, room in enumerate (self.json_config.scheduler_config.rooms):
            self.room_list.addItem(self.json_config.scheduler_config.rooms[i])

        for i, lab in enumerate (self.json_config.scheduler_config.labs):
            self.lab_list.addItem(self.json_config.scheduler_config.labs[i])


    def show_editor(self, item: QListWidgetItem, group: str) -> None:
        editor_box = self.get_editor(item, group)
        if self.my_layout.count() != 4:
            self.my_layout.addWidget(editor_box)
            self.current_editor = editor_box
        else:
            self.my_layout.replaceWidget(self.current_editor, editor_box)
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
        editor_del_button.hide()

        # Sets the text box editor to a name if clicked on item from list
        name = ""
        if type(item) is QListWidgetItem:
            name = item.text()
            editor_del_button.show()
        editor_textbox.setText(name)

        # Defines a function for writing out to the json
        def save() -> None:
            self.write_out(editor_textbox.toPlainText(), name, group)
            self.populate_lists()
            editor_box.hide()
            self.my_layout.removeWidget(editor_box)

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
            editor_box.hide()
            self.my_layout.removeWidget(editor_box)

        editor_del_button.clicked.connect(delete)
        editor_layout.addWidget(editor_del_button)

        def cancel() -> None:
            self.populate_lists()
            editor_box.hide()
            self.my_layout.removeWidget(editor_box)

        editor_cancel_button = QPushButton("Cancel")
        editor_cancel_button.clicked.connect(cancel)
        editor_layout.addWidget(editor_cancel_button)

        #self.my_layout.addWidget(editor_box)
        return editor_box
        
        
    def write_out(self, name: str, oName: str, group: str) -> None:
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


#Test initaliser for when I call the file directly
#Code in here is for testing purposes with the dummy json
#   SHOULD BE REMOVED LATER
if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = JsonConfig("../unittests/dummy")
    window = RoomEditorGui(config)
    window.show()
    sys.exit(app.exec())