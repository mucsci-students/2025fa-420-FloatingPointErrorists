from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from scheduler.models import CourseInstance

from scheduler_config_editor.controller.course_editor_controller import (
    CourseEditorController,
)
from scheduler_config_editor.controller.faculty_controller import (
    FacultyEditorController,
)
from scheduler_config_editor.controller.generator_controller import GeneratorController
from scheduler_config_editor.controller.room_controller import RoomEditorController
from scheduler_config_editor.controller.schedule_controller import SchedulerController
from scheduler_config_editor.model.json import JsonConfig
from scheduler_config_editor.view.course_editor_gui import CourseEditorGUI
from scheduler_config_editor.view.faculty_editor_gui import FacultyEditorGui
from scheduler_config_editor.view.schedule_window import newWindow

"""Simple Gui Window Initializer"""

class SimpleGUI(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Grabbing dimensions of user's primary screen
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
        else:
            screen_width = 0
            screen_height = 0

        # Set window title and size
        self.setWindowTitle("Scheduler App")
        self.resize(int(screen_width * 0.5), int(screen_height * 0.5))

        # Centering the tabs widget
        self.tab_widget = SimpleTabs(self)
        self.setCentralWidget(self.tab_widget)


"""Simple Tabs Initializer"""

class SimpleTabs(QWidget):

    def __init__(self, parent: QWidget) -> None:
        super(QWidget, self).__init__(parent)

        # Grabbing dimensions of user's primary screen
        self.schedules: list[list[CourseInstance]] = []
        screen = QGuiApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.availableGeometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
        else:
            screen_width = 0
            screen_height = 0

        self.main_layout = QVBoxLayout(self)

        # Initialize Tabs
        self.tabs = QTabWidget()
        self.editor_tab = QWidget()
        self.generator_tab = QWidget()
        self.schedule_viewer_tab = QWidget()
        self.tabs.resize(int(screen_width * 0.25), int(screen_height * 0.25))

        # Config
        self.config: JsonConfig | None = None

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

        editor_layout = QGridLayout()
        self.editor_tab.setLayout(editor_layout)

        generator_layout = QVBoxLayout()
        self.generator_tab.setLayout(generator_layout)

        # Dropdown code
        self.editor_combo_box = QComboBox()
        self.editor_combo_box.addItems(['Course', 'Room/Lab', 'Faculty'])
        editor_layout.addWidget(self.editor_combo_box, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        # Creates a container for the editor content
        self.editor_content_area = QVBoxLayout(self)
        editor_layout.addLayout(self.editor_content_area, 1, 0, 1, 2)

        # Prompt to load a config json
        self.config_prompt = QLabel ("Please load a config file first.")
        self.editor_content_area.addWidget(self.config_prompt)

        # Room and Lab placeholder
        self.room_controller: RoomEditorController | None = None

        # Faculty placeholders
        self.faculty_controller: FacultyEditorController | None = None
        self.faculty_gui: FacultyEditorGui | None = None
        editor_layout.addWidget(self.editor_combo_box, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        # Course placeholders
        self.course_controller: CourseEditorController | None = None
        self.course_gui: CourseEditorGUI | None = None

        # Generator placeholders
        self.generator_controller = GeneratorController(self.config)
        self.generator_gui = self.generator_controller.view

        self.generator_controller.on_schedules_generated = self.handle_schedules_generated

        # Add the generator_gui into the generator_tab's main_layout
        generator_layout.addWidget(self.generator_gui)

        # When dropdown changes
        def on_editor_selection_change() -> None:
            while self.editor_content_area.count():
                item = self.editor_content_area.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        self.editor_content_area.removeWidget(widget)
                        widget.setParent(None)
            selected = self.editor_combo_box.currentText()

            if selected == 'Course':
                if not self.course_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.course_controller.view)
            elif selected == 'Room/Lab':
                if not self.room_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.room_controller.view)
            elif selected == 'Faculty':
                if not self.faculty_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    # self.faculty_gui = FacultyEditorGui(self.faculty_controller)
                    self.editor_content_area.addWidget(self.faculty_controller.view)

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

        editor_layout.addLayout(bottom_buttons_layout, 99, 0, 1, 2)

# Schedule Viewer Tab #########################################################################################
        
        self.sc = SchedulerController()

        def set_schedule_label(text: str) -> None:
            self.schedule_viewer_label.setText(text)

        def set_len_label(text: str) -> None:
            self.schedule_viewer_label_len.setText(text)

        #main main_layout
        self.schedule_layout = QVBoxLayout()

        #add top main_layout
        view_top_layout = QHBoxLayout(self)

        #add view_by_courses button
        def view_by_courses() -> None:
            try:
                self.sc.mode = 0
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
            except:
                self.schedule_viewer_label.setText("""Schedule by course will be shown here""")
                self.my_scroll.setWidget(self.schedule_viewer_label)

        self.schedule_viewer_button = QPushButton("Courses")
        self.schedule_viewer_button.clicked.connect(view_by_courses)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_faulty button
        def view_by_faulty() -> None:
            try:
                self.sc.mode = 1
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
            except:
                set_schedule_label("""Schedule by faculty will be shown here""")
                self.my_scroll.setWidget(self.schedule_viewer_label) 

        self.schedule_viewer_button = QPushButton("Faculty")
        self.schedule_viewer_button.clicked.connect(view_by_faulty)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_room button
        def view_by_room() -> None:
            try:
                self.sc.mode = 2
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
            except:
                set_schedule_label("""Schedule by room will be shown here""")
                self.my_scroll.setWidget(self.schedule_viewer_label)

        self.schedule_viewer_button = QPushButton("Room")
        self.schedule_viewer_button.clicked.connect(view_by_room)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add pop out button
        self.nw = newWindow()
        def popoutwindow() -> None:
            self.nw.show()
            try:
                #Copies schedule_table into new window's my_table
                new_table = QTableWidget()
                new_table.setRowCount(self.schedule_table.rowCount())
                new_table.setColumnCount(self.schedule_table.columnCount())

                if self.sc.mode == 0:
                    new_table.setColumnCount(5)
                    new_table.setHorizontalHeaderLabels(["Course", "Faculty", "Room", "Lab", "Times"])
                elif self.sc.mode == 1:
                    new_table.setColumnCount(8)
                    new_table.setHorizontalHeaderLabels(["Faculty", "Course", "Room (Lab)", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
                else:
                    new_table.setColumnCount(8)
                    new_table.setHorizontalHeaderLabels(["Room", "Course", "Faculty", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

                for i in range(self.schedule_table.rowCount()):
                    for j in range(self.schedule_table.columnCount()):
                        item = self.schedule_table.item(i, j)
                        if item:
                            new_table.setItem(i, j, item.clone())

                self.nw.widget.my_table = new_table
                self.nw.widget.scroll_area_w.setWidget(new_table)

            except:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")  

        self.schedule_viewer_button = QPushButton("Popout Window")
        self.schedule_viewer_button.clicked.connect(popoutwindow)
        view_top_layout.addWidget(self.schedule_viewer_button) 

        #end top main_layout
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

        #table
        self.schedule_table = QTableWidget()

        #add bot main_layout
        view_bot_layout = QHBoxLayout()
        view_bot_layout.addStretch(7)

        #add prev_schedule button
        def schedule_back() -> None:
            try:
                self.sc.previous_schedule()
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
            except:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")


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
                    self.sc.index = 0
                elif newIndex > self.sc.length:
                    self.sc.index = self.sc.length - 1
                else:
                    self.sc.index = newIndex - 1

                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))

            except:
                QMessageBox.warning(self, "Error", "No schedule loaded or non valid integer.")
                    
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
            try:
                self.sc.next_schedule()
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
            except:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")

        self.schedule_viewer_button = QPushButton("-->")
        self.schedule_viewer_button.clicked.connect(schedule_forward)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        #push next widgets to right
        view_bot_layout.addStretch(6)

        #bot_right sub main_layout
        view_bot_right_layout = QVBoxLayout()
        view_bot_right_layout.addStretch()

        #add checkboxs
        self.checkboxjson = QCheckBox('json')
        view_bot_right_layout.addWidget(self.checkboxjson)
        self.checkboxcsv = QCheckBox('csv')
        view_bot_right_layout.addWidget(self.checkboxcsv)

        #add filename lineedit
        self.schedule_viewer_filename = QLineEdit()
        self.schedule_viewer_filename.setPlaceholderText("Filename")
        self.schedule_viewer_filename.setAlignment(Qt.AlignmentFlag.AlignRight)
        view_bot_right_layout.addWidget(self.schedule_viewer_filename)

        # Save button for Schedule Viewer Tab
        def save_button() -> None:
            if self.schedules:
                try:
                    if not self.checkboxjson.isChecked() and not self.checkboxcsv.isChecked():
                        QMessageBox.warning(self, "Error", "No file format selected.")
                        return
                    if self.checkboxjson.isChecked():
                        self.sc.save_as_json(self.schedules, self.schedule_viewer_filename.text() or "_")
                    if self.checkboxcsv.isChecked():
                        self.sc.save_as_csv(self.schedules, self.schedule_viewer_filename.text()  or "_")
                    QMessageBox.information(self, "Information", "Save Complete.")
                except:
                    QMessageBox.warning(self, "Error", "You trying to save a non generated schedule.")
            else:
                QMessageBox.warning(self, "Error", "No or empty generated schedule")

        self.schedule_viewer_button = QPushButton("Save")
        self.schedule_viewer_button.clicked.connect(save_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        # Load button
        def load_button() -> None:

            #open a file dialog to select file
            try:
                self.sc.reset_index()
                my_file = QFileDialog.getOpenFileName(
                    self,
                    'Open file',
                    'schedules',
                    'All Files (*);; JSON files (*.json);; CSV files (*.csv)')
                self.sc.cur_schedules.import_schedules(my_file[0])
                self.sc.length = len(self.sc.cur_schedules.schedules)
                #reset generated schedule if any
                self.schedules = []

                #show first schedule
                self.sc.set_table()
                self.schedule_table = self.sc.cur_table
                self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
                self.schedule_viewer_label_len.setText("/" + str(self.sc.length))
            except Exception as e:
                QMessageBox.warning(self, "Error", f"{e}")
        
        self.schedule_viewer_button = QPushButton("Load")
        self.schedule_viewer_button.clicked.connect(load_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        #end bot right sub main_layout
        view_bot_right_layout.addStretch()
        view_bot_layout.addLayout(view_bot_right_layout, stretch=1)

        #end bot main_layout
        self.schedule_layout.addLayout(view_bot_layout)

        # Set final main_layout

        self.schedule_viewer_tab.setLayout(self.schedule_layout)   
       
        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

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
            self.room_controller = RoomEditorController(self.config)
            

            # Enables save button
            self.save_config_button.setEnabled(True)

            # refresh GUI
            while self.editor_content_area.count():
                item = self.editor_content_area.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        self.editor_content_area.removeWidget(widget)
                        widget.setParent(None)
            if self.editor_combo_box.currentText() == "Faculty":
                self.editor_content_area.addWidget(self.faculty_controller.view)
            elif self.editor_combo_box.currentText() == "Room/Lab":
                self.editor_content_area.addWidget(self.room_controller.view)
            else:
                self.editor_content_area.addWidget(self.course_controller.view)
        except Exception as error:
                QMessageBox.critical(self, "Load Error", str(error))

    # Saves config file
    def save_config(self) -> None:
        if not self.config:
                QMessageBox.warning(self, "Error", "No config loaded to save.")
                return
        try:
            self.config.save()
            self.generator_controller.update_config(self.config)
            QMessageBox.information(self, "Config Saved", "Config saved successfully")
        except Exception as error:
            QMessageBox.critical(self, "Save Error", str(error))

    def handle_schedules_generated(self, schedules: list[list[CourseInstance]]) -> None:
        if self.sc is not None:
            self.sc.cur_schedules.load_schedules(schedules)
            self.sc.index = 0
            self.sc.length = len(self.sc.cur_schedules.schedules)

            #show first schedule
            self.sc.set_table()
            self.schedule_table = self.sc.cur_table
            self.my_scroll.setWidget(self.schedule_table)
            self.schedule_viewer_index.setText(str(self.sc.index + 1))
            self.schedule_viewer_label_len.setText("/" + str(self.sc.length))

            #save as list[list[courseinstance]]
            self.schedules = schedules

