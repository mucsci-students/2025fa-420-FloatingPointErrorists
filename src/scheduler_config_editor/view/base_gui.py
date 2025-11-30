from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt, QTimer, QSettings
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
    QStyle,
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
from scheduler_config_editor.model.json_config import JsonConfig
from scheduler_config_editor.controller.time_slot_controller import TimeSlotController
from scheduler_config_editor.view.course_editor_gui import CourseEditorGUI
from scheduler_config_editor.view.faculty_editor_gui import FacultyEditorGui
from scheduler_config_editor.view.schedule_window import newWindow
from scheduler_config_editor.view.jarvis_gui import JarvisGUI
from scheduler_config_editor.view.time_slot_editor_gui import TimeSlotEditorGui

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
        window_icon = QtGui.QPixmap("assets/dripGoku.png")
        self.setWindowIcon(QtGui.QIcon(window_icon))
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
        self.setStyleSheet(
            """
        QTabWidget::tab-bar {
            alignment: center; 
        }"""
            """QTabBar::tab { height: 50px; width: 250px; }"""
        )

        # Adding the tabs
        self.tabs.addTab(self.editor_tab, "Editor")
        self.tabs.addTab(self.generator_tab, "Generator")
        self.tabs.addTab(self.schedule_viewer_tab, "Schedules")

        editor_layout = QGridLayout()
        self.editor_tab.setLayout(editor_layout)

        generator_layout = QVBoxLayout()
        self.generator_tab.setLayout(generator_layout)

        # Tab Popups
        self.initial_popup_shown = False
        self.generator_info_shown = False
        self.editor_info_shown = False
        self.viewer_info_shown = False

        # Dropdown code
        self.editor_combo_box = QComboBox()
        self.editor_combo_box.addItems(["Course", "Room/Lab", "Faculty", "Time Slot"])
        editor_layout.addWidget(
            self.editor_combo_box, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Creates a container for the editor content
        self.editor_content_area = QVBoxLayout(self)
        editor_layout.addLayout(self.editor_content_area, 1, 0, 1, 2)

        # Prompt to load a config json
        self.config_prompt = QLabel("Please load a config file first.")
        self.editor_content_area.addWidget(self.config_prompt)

        # Room and Lab placeholder
        self.room_controller: RoomEditorController | None = None

        # Faculty placeholders
        self.faculty_controller: FacultyEditorController | None = None
        self.faculty_gui: FacultyEditorGui | None = None
        editor_layout.addWidget(
            self.editor_combo_box, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft
        )

        # Course placeholders
        self.course_controller: CourseEditorController | None = None
        self.course_gui: CourseEditorGUI | None = None

        # Generator placeholders
        self.generator_controller = GeneratorController(self.config)
        self.generator_gui = self.generator_controller.view

        # Time Slot placeholders
        self.time_slot_controller: TimeSlotController | None = None
        self.time_slot_gui: TimeSlotEditorGui | None = None

        self.generator_controller.on_schedules_generated = (
            self.handle_schedules_generated
        )

        # Jarvis Placeholder
        self.jarvis_gui: JarvisGUI | None = None

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

            if selected == "Course":
                if not self.course_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.course_controller.view)
            elif selected == "Room/Lab":
                if not self.room_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.room_controller.view)
            elif selected == "Faculty":
                if not self.faculty_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.faculty_controller.view)
            elif selected == "Time Slot":
                if not self.time_slot_controller:
                    self.editor_content_area.addWidget(self.config_prompt)
                else:
                    self.editor_content_area.addWidget(self.time_slot_controller.view)

        self.editor_combo_box.currentTextChanged.connect(on_editor_selection_change)

        # Button Layout for Load/Save Config and Undo/Redo
        bottom_buttons_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)

        self.save_config_button = QPushButton("Save Config")
        self.save_config_button.clicked.connect(self.save_config)
        self.save_config_button.setEnabled(False)

        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")

        self.undo_button.clicked.connect(self.undo)
        self.redo_button.clicked.connect(self.redo)

        self.undo_button.setEnabled(False)
        self.redo_button.setEnabled(False)

        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(self.load_config_button)
        bottom_buttons_layout.addWidget(self.save_config_button)
        bottom_buttons_layout.addWidget(self.undo_button)
        bottom_buttons_layout.addWidget(self.redo_button)

        editor_layout.addLayout(bottom_buttons_layout, 99, 0, 1, 2)

        # Jarvis Button
        self.jarvis_button = QPushButton()
        self.jarvis_button.setToolTip("Open J.A.R.V.I.S")
        self.jarvis_icon = QtGui.QPixmap("assets/jarvis.png")
        style = self.style()
        if style is not None:
            self.jarvis_button.setIcon(QtGui.QIcon(self.jarvis_icon))
            self.jarvis_button.setIconSize(QtCore.QSize(80, 80))
            self.jarvis_button.setFixedSize(80, 80)
            self.jarvis_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.jarvis_button.setFlat(True)
            self.jarvis_button.setStyleSheet(
                """
                QPushButton {
                    border: none;
                    padding: 25;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 100, 30%);
                    border-radius: 4px;
                }
            """
            )

        self.jarvis_button.clicked.connect(self.activate_jarvis)
        self.jarvis_button.setEnabled(False)

        # Schedule Viewer Tab #########################################################################################

        self.sc = SchedulerController()

        def set_schedule_label(text: str) -> None:
            self.schedule_viewer_label.setText(text)

        def set_len_label(text: str) -> None:
            self.schedule_viewer_label_len.setText(text)

        # main main_layout
        self.schedule_layout = QVBoxLayout()

        # add top main_layout
        view_top_layout = QHBoxLayout(self)

        # add view_by_courses button
        def view_by_courses() -> None:
            if self.sc.length > 0:
                self.sc.mode = 0
                self.sc.set_tables()
                self.schedule_table_widgets = self.sc.cur_widgets
                self.my_scroll.setWidget(self.sc.cur_widgets)
            else:
                self.schedule_viewer_label.setText(
                    """Schedule by course will be shown here"""
                )
                self.my_scroll.setWidget(self.schedule_viewer_label)

        self.schedule_viewer_button = QPushButton("Courses")
        self.schedule_viewer_button.clicked.connect(view_by_courses)
        view_top_layout.addWidget(self.schedule_viewer_button)

        # add view_by_faulty button
        def view_by_faulty() -> None:
            if self.sc.length > 0:
                self.sc.mode = 1
                self.sc.graph_schedule()
                self.schedule_table = self.sc.graph_widget
                self.my_scroll.setWidget(self.schedule_table)
            else:
                set_schedule_label("""Schedule by faculty will be shown here""")
                self.my_scroll.setWidget(self.schedule_viewer_label)

        self.schedule_viewer_button = QPushButton("Faculty")
        self.schedule_viewer_button.clicked.connect(view_by_faulty)
        view_top_layout.addWidget(self.schedule_viewer_button)

        # add view_by_room button
        def view_by_room() -> None:
            if self.sc.length > 0:
                self.sc.mode = 2
                self.sc.graph_schedule()
                self.schedule_table = self.sc.graph_widget
                self.my_scroll.setWidget(self.schedule_table)
            else:
                set_schedule_label("""Schedule by room will be shown here""")
                self.my_scroll.setWidget(self.schedule_viewer_label)

        self.schedule_viewer_button = QPushButton("Room")
        self.schedule_viewer_button.clicked.connect(view_by_room)
        view_top_layout.addWidget(self.schedule_viewer_button)

        # add pop out button
        self.nw = newWindow()

        def popoutwindow() -> None:
            self.nw.show()
            if self.sc.length > 0:
                if self.sc.mode == 0:
                    self.nw.widget.my_widget = self.sc.popup_widget
                    self.nw.widget.scroll_area_w.setWidget(self.nw.widget.my_widget)
                else:
                    self.nw.widget.graph_widget = self.sc.popup_graph_widget
                    self.nw.widget.scroll_area_w.setWidget(self.nw.widget.graph_widget)

            else:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")

        self.schedule_viewer_button = QPushButton("Popout Window")
        self.schedule_viewer_button.clicked.connect(popoutwindow)
        view_top_layout.addWidget(self.schedule_viewer_button)

        # end top main_layout
        view_top_layout.addStretch()
        self.schedule_layout.addLayout(view_top_layout)

        # scroll area for schedule
        self.my_scroll = QScrollArea()
        self.schedule_layout.addWidget(self.my_scroll, stretch=2)

        # text for Schedule Viewer Tab
        self.schedule_viewer_label = QLabel()
        self.schedule_viewer_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.schedule_viewer_label.setWordWrap(True)
        set_schedule_label("""Schedule by course will be shown here""")
        self.my_scroll.setWidget(self.schedule_viewer_label)

        # table
        self.schedule_table = QTableWidget()

        # add bot main_layout
        view_bot_layout = QHBoxLayout()
        view_bot_layout.addStretch(7)

        # add prev_schedule button
        def schedule_back() -> None:
            if self.sc.length > 0:
                self.sc.previous_schedule()
                if self.sc.mode == 0:
                    self.sc.set_tables()
                    self.schedule_table_widgets = self.sc.cur_widgets
                    self.my_scroll.setWidget(self.sc.cur_widgets)
                else:
                    self.sc.graph_schedule()
                    self.schedule_table = self.sc.graph_widget
                    self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
            else:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")

        self.schedule_viewer_button = QPushButton("<--")
        self.schedule_viewer_button.clicked.connect(schedule_back)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        # add label static text
        self.schedule_viewer_label_static = QLabel()
        self.schedule_viewer_label_static.setText("Schedule:")
        view_bot_layout.addWidget(self.schedule_viewer_label_static)

        # add index box
        def schedule_index_change(i: str) -> None:
            if self.sc.length > 0:
                try:
                    newIndex = int(i)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Non valid integer.")
                    return
                if newIndex < 1:
                    self.sc.index = 0
                elif newIndex > self.sc.length:
                    self.sc.index = self.sc.length - 1
                else:
                    self.sc.index = newIndex - 1
                if self.sc.mode == 0:
                    self.sc.set_tables()
                    self.schedule_table_widgets = self.sc.cur_widgets
                    self.my_scroll.setWidget(self.sc.cur_widgets)
                else:
                    self.sc.graph_schedule()
                    self.schedule_table = self.sc.graph_widget
                    self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
            else:
                QMessageBox.warning(self, "Error", "No schedule loaded.")

        self.schedule_viewer_index = QLineEdit()
        self.schedule_viewer_index.setPlaceholderText("x")
        self.schedule_viewer_index.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.schedule_viewer_index.setFixedSize(30, 30)

        self.schedule_viewer_index.returnPressed.connect(
            lambda: schedule_index_change(self.schedule_viewer_index.text())
        )
        view_bot_layout.addWidget(self.schedule_viewer_index)

        # add label suffix
        self.schedule_viewer_label_len = QLabel()
        self.schedule_viewer_label_len.setText("/Len")
        view_bot_layout.addWidget(self.schedule_viewer_label_len)

        # add next_schedule button
        def schedule_forward() -> None:
            if self.sc.length > 0:
                self.sc.next_schedule()
                if self.sc.mode == 0:
                    self.sc.set_tables()
                    self.schedule_table_widgets = self.sc.cur_widgets
                    self.my_scroll.setWidget(self.sc.cur_widgets)
                else:
                    self.sc.graph_schedule()
                    self.schedule_table = self.sc.graph_widget
                    self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
            else:
                QMessageBox.warning(self, "Error", "No Schedule Loaded")

        self.schedule_viewer_button = QPushButton("-->")
        self.schedule_viewer_button.clicked.connect(schedule_forward)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        # push next widgets to right
        view_bot_layout.addStretch(6)

        # bot_right sub main_layout
        view_bot_right_layout = QVBoxLayout()
        view_bot_right_layout.addStretch()

        # add checkboxs
        self.checkboxjson = QCheckBox("JSON")
        view_bot_right_layout.addWidget(self.checkboxjson)
        self.checkboxcsv = QCheckBox("CSV")
        view_bot_right_layout.addWidget(self.checkboxcsv)

        # add filename lineedit
        self.schedule_viewer_filename = QLineEdit()
        self.schedule_viewer_filename.setPlaceholderText("Filename")
        self.schedule_viewer_filename.setAlignment(Qt.AlignmentFlag.AlignRight)
        view_bot_right_layout.addWidget(self.schedule_viewer_filename)

        def pdf_export() -> None:
            """Export current schedule as PDF using a background worker and a spinner dialog."""
            name = self.schedule_viewer_filename.text() or "_"
            self.sc.save_as_pdf(name)
            QMessageBox.information(self, "Information", "PDF Export Complete.")

        self.schedule_viewer_pdfbutton = QPushButton("Export PDF")
        self.schedule_viewer_pdfbutton.clicked.connect(pdf_export)
        self.schedule_viewer_pdfbutton.setEnabled(False)
        view_bot_right_layout.addWidget(self.schedule_viewer_pdfbutton)

        # Save button for Schedule Viewer Tab
        def save_button() -> None:
            if self.schedules:
                if (
                    not self.checkboxjson.isChecked()
                    and not self.checkboxcsv.isChecked()
                ):
                    QMessageBox.warning(self, "Error", "No file format selected.")
                    return
                if self.checkboxjson.isChecked():
                    self.sc.save_as_json(
                        self.schedules, self.schedule_viewer_filename.text() or "_"
                    )
                if self.checkboxcsv.isChecked():
                    self.sc.save_as_csv(
                        self.schedules, self.schedule_viewer_filename.text() or "_"
                    )
                QMessageBox.information(self, "Information", "Save Complete.")
            else:
                QMessageBox.warning(self, "Error", "No schedules generated to save.")

        self.schedule_viewer_savebutton = QPushButton("Save")
        self.schedule_viewer_savebutton.clicked.connect(save_button)
        self.schedule_viewer_savebutton.setEnabled(False)
        view_bot_right_layout.addWidget(self.schedule_viewer_savebutton)

        # Load button
        def load_button() -> None:
            # open a file dialog to select file
            try:
                self.sc.reset_index()
                my_file = QFileDialog.getOpenFileName(
                    self,
                    "Open file",
                    "schedules",
                    "All Files (*);; JSON files (*.json);; CSV files (*.csv)",
                )
                self.sc.cur_schedules.import_schedules(my_file[0])
                self.sc.length = len(self.sc.cur_schedules.schedules)
                # reset generated schedule if any
                self.schedules = []

                # show first schedule
                if self.sc.mode == 0:
                    self.sc.set_tables()
                    self.schedule_table_widgets = self.sc.cur_widgets
                    self.my_scroll.setWidget(self.schedule_table_widgets)
                else:
                    self.sc.graph_schedule()
                    self.schedule_table = self.sc.graph_widget
                    self.my_scroll.setWidget(self.schedule_table)
                self.schedule_viewer_index.setText(str(self.sc.index + 1))
                self.schedule_viewer_label_len.setText("/" + str(self.sc.length))

                # Disable Save Button
                self.schedule_viewer_savebutton.setEnabled(False)
                self.schedule_viewer_pdfbutton.setEnabled(True)

            except Exception as e:
                QMessageBox.warning(self, "Error", f"{e}")

        self.schedule_viewer_button = QPushButton("Load")
        self.schedule_viewer_button.clicked.connect(load_button)
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        # End bot right sub main_layout
        view_bot_right_layout.addStretch()
        view_bot_layout.addLayout(view_bot_right_layout, stretch=1)

        # End bot main_layout
        self.schedule_layout.addLayout(view_bot_layout)

        # Set final main_layout
        self.schedule_viewer_tab.setLayout(self.schedule_layout)

        # self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

        # persistent settings (stored per user/system)
        self.settings = QSettings("Millersville", "SchedulerConfigEditor")

        # --- Small reset icon button ---
        reset_button = QPushButton()
        reset_button.setToolTip("Reset all help popups")
        style = self.style()
        if style is not None:
            reset_button.setIcon(
                style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
            )
            reset_button.setIconSize(QtCore.QSize(30, 30))
            reset_button.setFixedSize(40, 40)
            reset_button.setCursor(Qt.CursorShape.PointingHandCursor)
            reset_button.setFlat(True)
            reset_button.setStyleSheet("""
                QPushButton {
                    border: none;
                    padding: 25;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 100, 30%);
                    border-radius: 4px;
                }
            """)

        reset_button.clicked.connect(self.reset_all_popups)

        # Layout for tabs, Jarvis, and help info
        top_layout = QVBoxLayout()
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.addWidget(
            self.jarvis_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(
            reset_button, alignment=Qt.AlignmentFlag.AlignRight
        )
        top_layout.addLayout(top_buttons_layout)
        top_layout.addWidget(self.tabs)

        self.main_layout.addLayout(top_layout)

        # Track initial popup
        self.initial_popup_scheduled = False

        # When changing tab, show popup
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        """Called automatically when the window is first shown."""
        super().showEvent(event)

        if not self.initial_popup_shown:
            self.initial_popup_shown = True
            # Make sure the window is visible and sized before showing editor popup
            QTimer.singleShot(
                100, lambda: self.on_tab_changed(self.tabs.currentIndex())
            )

    def show_info_popup(self, tab_name: str, key: str) -> None:
        """Shows popups for each tab, including a do not show again button."""
        msg = QMessageBox(self)
        msg.setWindowTitle(f"{tab_name} Tab")
        msg.setIcon(QMessageBox.Icon.Information)

        if tab_name == "Editor":
            msg.setText(
                "This is the Editor tab.\n\nHere, you can load, save, and edit a configuration file.\n\nUse the dropdown to select what you want to edit.\n"
            )
        elif tab_name == "Generator":
            msg.setText(
                "This is the Generator tab.\n\nHere you can configure optimizations, set a number of schedules to generate, and run the generator.\n"
            )
        elif tab_name == "Schedules":
            msg.setText(
                "This is the Schedules tab.\n\nHere, you can load, save, and view schedules that have been generated or loaded.\n\nUse the buttons at the top to format the table view.\n"
            )

        # Add the "Don't show again" checkbox
        dont_show_box = QCheckBox("Don't show this message again")
        msg.setCheckBox(dont_show_box)

        msg.addButton(QPushButton("OK"), QMessageBox.ButtonRole.AcceptRole)
        msg.exec()

        # Persist setting
        if dont_show_box.isChecked():
            self.settings.setValue(key, False)

    # When changing tabs
    def on_tab_changed(self, index: int) -> None:
        """Called when the tab changes."""
        tab_name = self.tabs.tabText(index)
        key = f"show_help_{tab_name.lower()}"
        show_popup = self.settings.value(key, True, type=bool)

        if not show_popup:
            return  # User has disabled this popup

        self.show_info_popup(tab_name, key)

    # Open Jarvis
    def activate_jarvis(self) -> None:
        self.jarvis_gui.show()

    # Reset all tab popups
    def reset_all_popups(self) -> None:
        """Clears stored popup preferences."""
        reply = QMessageBox.question(
            self,
            "Reset Popups",
            "Are you sure you want to re-enable all help popups?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.settings.clear()
            QMessageBox.information(
                self, "Reset Complete", "All popups will appear again."
            )
            self.on_tab_changed(self.tabs.currentIndex())

    # Asks user for config file
    def load_config(self) -> None:
        config_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Scheduler Config File",
            "configs",
            "JSON Files (*.json);;All Files (*)",
        )

        if not config_path:
            QMessageBox.warning(
                self, "No Config File Selected", "Please select a valid config file"
            )
            return

        try:
            self.config = JsonConfig(config_path)
            QMessageBox.information(self, "Config Loaded", "Successfully loaded config")
            self.faculty_controller = FacultyEditorController(self.config)
            self.course_controller = CourseEditorController(self.config)
            self.generator_controller.update_config(self.config)
            self.generator_gui.update_config(self.config)
            self.room_controller = RoomEditorController(self.config)
            self.jarvis_gui = JarvisGUI(self.config)
            self.jarvis_gui.data_changed.connect(self.refresh)

            # Enables save and jarvis button
            self.save_config_button.setEnabled(True)
            self.jarvis_button.setEnabled(True)

            # Set memento config
            self.redo_button.setEnabled(True)
            self.undo_button.setEnabled(True)
            self.config.clear_stacks()

            # refresh GUI
            self.refresh()

        except Exception as error:
            QMessageBox.critical(self, "Load Error", str(error))

    def refresh(self) -> None:
        if self.config is None:
            return
        self.faculty_controller = FacultyEditorController(self.config)
        self.course_controller = CourseEditorController(self.config)
        self.room_controller = RoomEditorController(self.config)
        self.time_slot_controller = TimeSlotController(self.config)
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
        elif self.editor_combo_box.currentText() == "Time Slot":
            self.editor_content_area.addWidget(self.time_slot_controller.view)
        else:
            self.editor_content_area.addWidget(self.course_controller.view)

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

            # show first schedule
            if self.sc.mode == 0:
                self.sc.set_tables()
                self.schedule_table_widgets = self.sc.cur_widgets
                self.my_scroll.setWidget(self.sc.cur_widgets)
            else:
                self.sc.graph_schedule()
                self.schedule_table = self.sc.graph_widget
                self.my_scroll.setWidget(self.schedule_table)
            self.schedule_viewer_index.setText(str(self.sc.index + 1))
            self.schedule_viewer_label_len.setText("/" + str(self.sc.length))

            # save as list[list[courseinstance]]
            self.schedules = schedules

            # enable button
            self.schedule_viewer_savebutton.setEnabled(True)
            self.schedule_viewer_pdfbutton.setEnabled(True)

    def undo(self) -> None:
        try:
            self.config.undo()
        except IndexError as error:
            QMessageBox.information(self, "Undo Error", str(error))
        self.config.save()
        self.refresh()

    def redo(self) -> None:
        try:
            self.config.redo()
        except IndexError as error:
            QMessageBox.information(self, "Redo Error", str(error))
        self.config.save()
        self.refresh()
