import sys
from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTabWidget, QMainWindow,
    QCheckBox, QComboBox, QFileDialog, QGridLayout,
    QScrollArea, QMessageBox
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt
from scheduler.models import CourseInstance

from scheduler_config_editor.controller.course_editor_controller import CourseEditorController
from scheduler_config_editor.controller.generator_controller import GeneratorController
from scheduler_config_editor.view.generator_gui import GeneratorGui

sys.path.append('../controller')
from scheduler_config_editor.controller.testing import ModClass
from scheduler_config_editor.controller.schedule_controller import SchedulerController
from scheduler_config_editor.controller.faculty_controller import FacultyEditorController
from scheduler_config_editor.model.schedule_handler import ScheduleHandler
from scheduler_config_editor.view.schedule_window import newWindow
from scheduler_config_editor.view.faculty_editor_gui import FacultyEditorGui
from scheduler_config_editor.controller.schedule_controller import SchedulerController
from scheduler_config_editor.view.course_editor_gui import CourseEditorGUI
from scheduler_config_editor.view.schedule_window import newWindow

import scheduler_config_editor
from scheduler_config_editor.model.json import JsonConfig

sys.path.append('../controller')
from scheduler_config_editor.controller.testing import ModClass

"""Simple Gui Window Initializer"""

class SimpleGUI(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Set window title and size
        self.setWindowTitle("Scheduler App")
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Centering the tabs widget
        self.tab_widget = SimpleTabs(self)
        self.setCentralWidget(self.tab_widget)


"""Simple Tabs Initializer"""

class SimpleTabs(QWidget):
    def __init__(self, parent) -> None:
        super(QWidget, self).__init__(parent)

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.layout = QVBoxLayout(self)

        # Initialize Tabs
        self.tabs = QTabWidget()
        self.editor_tab = QWidget()
        self.generator_tab = QWidget()
        self.schedule_viewer_tab = QWidget()
        self.tabs.resize(int(screen_width * 0.25), int(screen_height * 0.25))

        # Config
        self.config: JsonConfig = None
        self.schedules: list[list[CourseInstance]]

        # TabBar Stylesheet
        self.setStyleSheet('''
        QTabWidget::tab-bar {
            alignment: center; 
        }'''
        '''QTabBar::tab { height: 100px; width: 500px; }'''
        )

        # Adding the tabs
        self.tabs.addTab(self.editor_tab, "Editor")
        self.tabs.addTab(self.generator_tab, "Generator")
        self.tabs.addTab(self.schedule_viewer_tab, "Schedules")

        self.editor_tab.layout = QGridLayout()
        self.editor_tab.setLayout(self.editor_tab.layout)

        self.generator_tab.layout = QVBoxLayout()
        self.generator_tab.setLayout(self.generator_tab.layout)

        # Dropdown code
        self.editor_combo_box = QComboBox()
        self.editor_combo_box.addItems(['Course', 'Room', 'Lab', 'Faculty'])
        self.editor_tab.layout.addWidget(self.editor_combo_box, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Creates a container for the editor content
        self.editor_content_area = QVBoxLayout(self)
        self.editor_tab.layout.addLayout(self.editor_content_area, 1, 0, 1, 2)

        # Faculty placeholders
        self.faculty_controller = None
        self.faculty_gui = None
        self.editor_tab.layout.addWidget(self.editor_combo_box, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        # Course placeholders
        self.course_controller = None
        self.course_gui = None

        # Generator placeholders
        self.generator_controller = GeneratorController(self.config)
        self.generator_gui = self.generator_controller.view

        self.generator_controller.on_schedules_generated = self.handle_schedules_generated

        # Add the generator_gui into the generator_tab's layout
        self.generator_tab.layout.addWidget(self.generator_gui)

        # When dropdown changes
        def on_editor_selection_change() -> None:
            while self.editor_content_area.count():
                item = self.editor_content_area.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            selected = self.editor_combo_box.currentText()

            if selected == 'Course':
                self.editor_content_area.addWidget(self.course_controller.view)
            elif selected == 'Room':
                label = QLabel('Room Editor Placeholder')
                self.editor_content_area.addWidget(label)
            elif selected == 'Lab':
                label = QLabel('Lab Editor Placeholder')
                self.editor_content_area.addWidget(label)
            elif selected == 'Faculty':
                if not self.faculty_controller:
                    label = QLabel ("Please load a config file first.")
                    self.editor_content_area.addWidget(label)
                else:
                    self.faculty_gui = FacultyEditorGui(self.faculty_controller)
                    self.editor_content_area.addWidget(self.faculty_gui)

        self.editor_combo_box.currentTextChanged.connect(on_editor_selection_change)

        # Button Layout for Load/Save Config
        bottom_buttons_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)

        self.save_config_button = QPushButton("Save Config")
        self.save_config_button.clicked.connect(self.save_config)
        self.save_config_button.setEnabled(False)

        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(self.load_config_button)
        bottom_buttons_layout.addWidget(self.save_config_button)

        self.editor_tab.layout.addLayout(bottom_buttons_layout, 99, 0, 1, 2)

# Schedule Viewer Tab #########################################################################################
        
        sc = SchedulerController()

        def set_schedule_label(text: str) -> None:
            self.schedule_viewer_label.setText(text)

        def set_len_label(text: str) -> None:
            self.schedule_viewer_label_len.setText(text)

        #main layout
        self.schedule_layout = QVBoxLayout()

        #add top layout
        view_top_layout = QHBoxLayout(self)

        #add view_by_courses button
        def view_by_courses() -> None:
            try:
                sc.mode = 0
                self.schedule_viewer_label.setText(sc.get_format())
            except:
                self.schedule_viewer_label.setText("""Schedule by course will be shown here""")    

        self.schedule_viewer_button = QPushButton("Courses")
        self.schedule_viewer_button.clicked.connect(view_by_courses)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_faulty button
        def view_by_faulty() -> None:
            try:
                sc.mode = 1
                self.schedule_viewer_label.setText(sc.get_format())
            except:
                set_schedule_label("""Schedule by faculty will be shown here""")    

        self.schedule_viewer_button = QPushButton("Faculty")
        self.schedule_viewer_button.clicked.connect(view_by_faulty)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_room button
        def view_by_room() -> None:
            try:
                sc.mode = 2
                self.schedule_viewer_label.setText(sc.get_format())
            except:
                set_schedule_label("""Schedule by room will be shown here""")    

        self.schedule_viewer_button = QPushButton("Room")
        self.schedule_viewer_button.clicked.connect(view_by_room)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add pop out button
        self.nw = newWindow()
        def popoutwindow() -> None:
            self.nw.show()
            try:
                self.nw.widget.schedule.setText(sc.get_format())
            except:
                self.nw.widget.schedule.setText("""Schedule Not Selected""")    

        self.schedule_viewer_button = QPushButton("Popout Window")
        self.schedule_viewer_button.clicked.connect(popoutwindow)
        view_top_layout.addWidget(self.schedule_viewer_button) 

        #end top layout
        view_top_layout.addStretch()
        self.schedule_layout.addLayout(view_top_layout) 

        #scroll area for schedule
        self.my_scroll = QScrollArea()
        self.my_scroll.setWidgetResizable(True)
        self.schedule_layout.addWidget(self.my_scroll, stretch= 2)


        # text for Schedule Viewer Tab
        self.schedule_viewer_label = QLabel()
        self.schedule_viewer_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.schedule_viewer_label.setWordWrap(True)
        set_schedule_label("""Schedule by course will be shown here""")    
        self.my_scroll.setWidget(self.schedule_viewer_label)

        #add bot layout
        view_bot_layout = QHBoxLayout()
        view_bot_layout.addStretch()

        #add prev_schedule button
        def schedule_back() -> None:
            sc.previous_schedule()
            self.schedule_viewer_label.setText(sc.get_format())
            self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))

        self.schedule_viewer_button = QPushButton("<--")
        self.schedule_viewer_button.clicked.connect(schedule_back)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        #add label static text
        self.schedule_viewer_label_static = QLabel()
        self.schedule_viewer_label_static.setText("Schedule:")
        view_bot_layout.addWidget(self.schedule_viewer_label_static)

        #add index box
        def schedule_index_change(i: str) -> None:
            try:
                newIndex = int(i)
                if newIndex < 1:
                    sc.index = 0
                elif newIndex > sc.length:
                    sc.index = sc.length - 1
                else:
                    sc.index = newIndex - 1

                self.schedule_viewer_label.setText(sc.get_format())
                self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))

            except:
                pass
                    
        self.schedule_viewer_index = QLineEdit()
        self.schedule_viewer_index.setPlaceholderText("x")
        self.schedule_viewer_index.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.schedule_viewer_index.setFixedSize(30, 30)
        
        self.schedule_viewer_index.returnPressed.connect(lambda: schedule_index_change(self.schedule_viewer_index.text()))
        view_bot_layout.addWidget(self.schedule_viewer_index)

        #add label suffix
        self.schedule_viewer_label_len = QLabel()
        self.schedule_viewer_label_len.setText("/Len")
        view_bot_layout.addWidget(self.schedule_viewer_label_len)

        #add next_schedule button
        def schedule_forward() -> None:
            sc.next_schedule()
            self.schedule_viewer_label.setText(sc.get_format())
            self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))

        self.schedule_viewer_button = QPushButton("-->")
        self.schedule_viewer_button.clicked.connect(schedule_forward)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        #push next widgets to right
        view_bot_layout.addStretch()

        #bot_right sub layout
        view_bot_right_layout = QVBoxLayout()
        view_bot_right_layout.addStretch()

        #add checkboxs
        checkbox1 = QCheckBox('json')
        view_bot_right_layout.addWidget(checkbox1)
        checkbox2 = QCheckBox('csv')
        view_bot_right_layout.addWidget(checkbox2)

        # Save button for Schedule Viewer Tab
        def save_button() -> None:
            if checkbox1.isChecked():
                pass # SAVE AS JSON HERE
            if checkbox2.isChecked():
                pass # SAVE AS CSV HERE

        self.schedule_viewer_button = QPushButton("Save")
        self.schedule_viewer_button.clicked.connect(save_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        # Load button
        def load_button() -> None:

            #open a file dialog to select file
            try:
                test = QFileDialog.getOpenFileName(
                    self,
                    'Open file',
                    'schedules',
                    'All Files (*);; JSON files (*.json);; CSV files (*.csv)')
                sc.cur_schedules.import_schedules(test[0])
                sc.length = len(sc.cur_schedules.schedules)

                #show first schedule
                self.schedule_viewer_label.setText(sc.get_format())
                self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))
                self.schedule_viewer_label_len.setText("/" + str(sc.length))
            except:
                pass
        
        self.schedule_viewer_button = QPushButton("Load")
        self.schedule_viewer_button.clicked.connect(load_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        #end bot right sub layout
        view_bot_right_layout.addStretch()
        view_bot_layout.addLayout(view_bot_right_layout)

        #end bot layout
        self.schedule_layout.addLayout(view_bot_layout)

        # Set final layout

        self.schedule_viewer_tab.setLayout(self.schedule_layout)   
       
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def handleButton(self) -> None:
        self.modifier = ModClass(self)
        self.modifier.test()

    # Asks user for config file
    def load_config(self) -> None:
        config_path, _ = QFileDialog.getOpenFileName(self,
            "Select Scheduler Config File","", "JSON Files (*.json);;All Files (*)")

        if not config_path:
            QMessageBox.warning(self, "No Config File Selected", "Please select a valid config file")
            return

        try:
            self.config = JsonConfig(config_path)
            QMessageBox.information(self, "Config Loaded", "Successfully loaded config")
            self.faculty_controller = FacultyEditorController(self.config)
            self.course_controller = CourseEditorController(self.config)
            self.generator_controller.update_config(self.config)
            self.generator_gui.update_config(self.config)

            # Enables save button
            self.save_config_button.setEnabled(True)

            # If faculty tab is currently being used, refresh GUI
            if self.editor_combo_box.currentText() == "Faculty":
                while self.editor_content_area.count():
                    item = self.editor_content_area.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
                self.faculty_gui = FacultyEditorGui(self.faculty_controller)
                self.editor_content_area.addWidget(self.faculty_gui)

        except Exception as error:
                QMessageBox.warning(self, "Load Error", error)

    # Saves config file
    def save_config(self) -> None:
        if not self.config:
                QMessageBox.warning(self, "Error", "No config loaded to save.")
                return
        try:
            self.config.save()
            self.generator_gui.update_config(self.config)
            self.generator_controller.update_config(self.config)
            QMessageBox.information(self, "Config Saved", "Config saved successfully")
        except Exception as error:
            QMessageBox.warning(self, "Save Error", error)

    def handle_schedules_generated(self, schedules: list[list[CourseInstance]]) -> None:
        self.schedules = schedules
