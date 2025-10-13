from PyQt6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QListWidget, QGroupBox
from PyQt6.QtCore import Qt

class RoomEditorGui(QWidget):
    ROOM = "Room"
    LAB = "Lab"

    from scheduler_config_editor.controller.room_controller import RoomEditorController
    def __init__(self, controller: RoomEditorController) -> None:
        super().__init__()
        self.controller = controller
        self.json_config = controller.json_config

        # Layout Stuff
        self.my_layout = QVBoxLayout(self)
        
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
        room_add_button.clicked.connect(lambda item: self.controller.show_editor(item, RoomEditorGui.ROOM))
        room_layout.addWidget(room_add_button)

        self.room_list.itemClicked.connect(lambda item: self.controller.show_editor(item, RoomEditorGui.ROOM))

        # Labs Group Box
        lab_group_box = QGroupBox("Labs")
        lab_layout = QVBoxLayout()
        lab_group_box.setLayout(lab_layout)

        self.lab_list = QListWidget(self)
        lab_layout.addWidget(self.lab_list)

        lab_add_button = QPushButton("Add Lab")
        lab_add_button.clicked.connect(lambda item: self.controller.show_editor(item, RoomEditorGui.LAB))
        lab_layout.addWidget(lab_add_button)

        self.lab_list.itemClicked.connect(lambda item: self.controller.show_editor(item, RoomEditorGui.LAB))

        self.my_layout.addWidget(room_group_box)
        self.my_layout.addWidget(lab_group_box)

        # Add a groupbox for the editor
        self.editor_container = QGroupBox("Editor")
        self.editor_container.setLayout(QVBoxLayout())
        self.my_layout.addWidget(self.editor_container)
        self.editor_container.setHidden(True)