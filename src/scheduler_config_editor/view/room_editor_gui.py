import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QTabWidget, QMainWindow, QHBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem, QSpinBox, QFormLayout, QMessageBox, QGroupBox
from PyQt6.QtGui import QGuiApplication, QIntValidator
from PyQt6.QtCore import Qt

import scheduler_config_editor
from scheduler_config_editor import Room, Lab, JsonConfig
from scheduler_config_editor.model import room

class RoomEditorGui(QMainWindow):
    ROOM = "room"
    LAB = "lab"

    def __init__(self, json_config) -> None:
        super().__init__()
        self.json_config = json_config

        # Layout Stuff
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))
        
        # Changes title
        self.title = QLabel("Room and Lab Editor")
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)


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
        # # Editor Box
        # self.editor_box = QGroupBox("Editor")
        # editor_layout = QVBoxLayout()
        # self.editor_box.setLayout(editor_layout)

        # self.editor_textbox = QLineEdit()
        # editor_layout.addWidget(self.editor_textbox)

        # editor_save_button = QPushButton("Save")
        # editor_save_button.clicked.connect(self.save)
        # editor_layout.addWidget(editor_save_button)

        # self.editor_box.hide()


        self.layout.addWidget(room_group_box) #, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(lab_group_box) #, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        # self.layout.addWidget(self.editor_box)
    
    def populate_lists(self) -> None:
        self.room_list.clear()
        self.lab_list.clear()
        for i, room in enumerate (self.json_config.scheduler_config.rooms):
            self.room_list.addItem(self.json_config.scheduler_config.rooms[i])

        for i, lab in enumerate (self.json_config.scheduler_config.labs):
            self.lab_list.addItem(self.json_config.scheduler_config.labs[i])

    def show_editor(self, item: QListWidgetItem, group: str) -> None:
        editor_box = QGroupBox("Editor")
        editor_layout = QVBoxLayout()
        editor_box.setLayout(editor_layout)

        editor_textbox = QLineEdit()
        editor_layout.addWidget(editor_textbox)

        name = ""
        if type(item) != bool:
            name = item.text()
        editor_textbox.setText(name)

        def save():
            self.write_out(editor_textbox.text(), name, group)
            self.populate_lists()
            self.layout.removeWidget(editor_box)

        editor_save_button = QPushButton("Save")
        editor_save_button.clicked.connect(save)
        editor_layout.addWidget(editor_save_button)

        self.layout.addWidget(editor_box)

        
    def write_out(self, name, oName: str, group: str) -> None:
        if group == "room":
            if oName != "":
                Room.mod_room(self.json_config, oName, name)
            else:
                Room.add_room(self.json_config, name)
        elif group == "lab":
            if oName != "":
                Lab.mod_lab(self.json_config, oName, name)
            else:
                Lab.add_lab(self.json_config, name)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = JsonConfig("../unittests/dummy")
    window = RoomEditorGui(config)
    window.show()
    sys.exit(app.exec())