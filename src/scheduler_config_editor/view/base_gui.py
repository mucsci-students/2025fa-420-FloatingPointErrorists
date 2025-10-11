import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QMainWindow, QCheckBox, QComboBox, QFileDialog
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

sys.path.append('../controller')
from scheduler_config_editor.controller.testing import ModClass
from scheduler_config_editor.controller.schedule_controller import SchedulerController 
from scheduler_config_editor.model.schedule_handler import ScheduleHandler
from scheduler_config_editor.view.schedule_window import newWindow 

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

        # Temporary labels for each tab to show that they work lmao
        self.editor_tab.layout = QVBoxLayout(self)
        self.editor_label = QLabel()
        self.editor_label.setText("""
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠒⢒⡶⠒⠈⠐⠂⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢚⡟⢁⠔⠁⠀⣀⠔⠊⠉⠉⠺⡦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡜⠁⠋⡰⠃⠀⢀⠜⠁⠀⠀⠀⠀⠀⣉⣉⡙⢦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⠞⠀⢀⡞⠁⠀⣠⣯⣶⣖⠒⢢⡠⠒⣽⣭⡟⣷⠉⡡⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡎⠀⠀⡞⠀⠀⢰⢻⣿⢷⣼⣧⠼⠤⠤⠽⠷⠛⢋⡿⡁⠀⠀⠀
⠀⠀⠀⠀⠀⡜⠀⠀⢰⠃⠀⠀⡟⣿⡯⢭⣁⣀⡀⠀⠀⠀⣀⣀⠼⡄⡇⠀⠀⠀
⠀⠀⠀⠀⣰⠁⠀⠀⠘⡆⠀⠀⡗⢿⣯⣿⡶⣿⡛⠿⠿⡟⠛⣄⢯⠀⡇⠀⠀⠀
⠀⠀⠀⢠⠃⠀⠀⠀⠀⠘⣄⠀⠘⢄⡉⠛⠯⣓⣛⣛⡛⠓⢚⡡⠞⡰⠉⡆⠀⠀
⠀⠀⢀⠇⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠈⠲⢤⣤⣤⣬⠽⠟⠁⣠⠞⠀⢸⠀⠀⠀
⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠵⣦⡀⠀⠈⠙⠣⡄⣠⠖⠁⠀⢠⢻⠀⠀⠀
⠀⠀⡞⢀⡦⠭⢔⡄⠀⠀⠀⠀⠀⠀⠀⠈⠓⢦⡀⠀⠈⢧⠀⠀⠀⠎⠈⢣⠀⠀
⠀⡴⢻⠘⡑⢐⠎⡝⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⢸⡄⠀⠀⠀⠀⠈⡦⡀
⢸⠀⠘⢦⠈⠁⢰⣜⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⢸⠀⠀⢀⣀⡤⠞⠁⡧
⠈⠢⡀⠀⠙⠦⢌⣁⣀⣀⠀⠀⠀⢀⣀⣀⣀⠤⠖⢉⡠⠋⠉⠉⠉⠀⠀⣀⠔⠁
⠀⠀⠈⠙⠒⠢⠤⠤⠤⠭⠭⠭⠭⠥⠤⠤⠤⠔⠚⠁⠈⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
        """)

        self.editor_tab.layout.addWidget(self.editor_label)
        self.editor_tab.setLayout(self.editor_tab.layout)

        self.button = QPushButton("Test button")
        self.editor_tab.layout.addWidget(self.button)
        
        self.button.clicked.connect(self.handleButton)

        self.generator_tab.layout = QVBoxLayout(self)
        self.generator_label = QLabel()
        self.generator_label.setText("""
 ⠀⠀⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬛⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬛⬛⬛⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬜⬜⬜⬜⬛🟨🟨🟫🟫🟨🟨⬛🟨🟫🟨🟨⬛🟨⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬛⬛⬛🟨🟫🟫🟫🟨⬛⬛⬜⬛⬛⬛🟨🟨🟨🟨🟨🟨🟫🟫🟫🟨⬛⬛🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬛🟨🟨🟨🟨🟫🟫🟨🟨⬛⬛⬛🟦⬛🟨🟨🟫🟫🟫🟨🟨🟨🟨🟨⬛🟨🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛🟨🟨⬛⬛🟨🟨🟨⬛⬛🟦🟦🟦🟦⬛🟨🟫🟫⬛⬛🟨🟨🟨⬛⬛🟨🟨🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛🟨⬛⬛🟨🟨⬛⬛⬛🟦🟦🟦🟦🟦⬛🟨⬛⬛⬛🟨🟨⬛⬛⬛⬛🟨🟨🟨🟫🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛🟦🟦🟦⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟫🟫🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬛🟨🟨⬛🟨⬛🟨🟨🟨⬛⬛⬛🟨🟨🟨🟨🟨🟨⬛🟨⬛🟨🟨🟨⬛🟨🟫🟫🟨⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜
⬜⬛🟨⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨⬛⬛⬛⬛🟨🟨🟨⬛🟨🟫🟫🟨⬛⬜⬜⬜⬜⬜⬜⬛🟨🟨⬛⬜⬜⬜
⬜⬜⬛⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬛🟨🟨⬛🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬛🟨⬛🟨⬛⬜⬜⬜
⬜⬛⬜🟦🟦⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜🟦⬜⬛🟨⬛🟨🟨🟫🟨🟨⬛⬜⬛⬛⬛🟨⬛⬛🟨⬛⬜⬜⬜
⬜⬛🟦⬛🟦⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜🟦⬛🟦⬛🟨🟨⬛🟨🟫🟨🟨⬛⬛⬜⬜⬜⬛⬜⬛🟨⬛⬛⬜⬜
⬜⬛⬜🟦🟦⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬜⬜⬜🟦🟦🟦⬛🟨🟨⬛🟨🟨🟨🟨⬛⬜⬜⬜⬜⬛⬜⬛🟨⬛🟨⬛⬜
⬜⬜⬛⬜⬜⬜⬛🟨⬛🟨⬛🟨🟨🟨🟨🟨⬛⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛🟨🟨🟨🟨⬛⬜⬜⬜⬜⬛⬜⬛🟨⬛⬛🟨⬛
⬜⬜⬜⬛⬛⬛🟨⬛🟨🟨⬛🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛🟨🟨🟨🟨⬛🟨🟨🟨🟫⬛⬜⬜⬜⬛⬛⬛🟨🟨⬛🟨⬛⬜
⬜⬜⬜⬜⬛🟨⬛🟨🟨⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟫⬛⬛⬛⬛🟫🟫⬛🟨⬛🟨⬛⬜⬜
⬜⬜⬜⬜⬛⬛🟨🟨⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟫🟫🟨🟨🟨⬛⬛⬛🟨🟨⬛⬜⬜⬜
⬜⬜⬜⬛🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨⬛⬜⬛🟨⬛⬛⬛⬜⬜
⬜⬜⬜⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟫🟨⬛⬜⬜⬛🟫⬛🟫⬛⬜
⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨🟨⬛🟫🟫🟫🟫🟫🟫⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨⬛⬜⬛🟫⬛🟫⬛⬜
⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨🟨⬛🟫⬛⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨⬛⬜⬜⬛🟫🟫⬛⬜⬜
⬜⬜⬜⬜⬜⬛🟨🟨🟨🟨🟨⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨⬛🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛🟨🟨⬛⬜⬜⬛🟫⬛⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟨🟨🟨⬛⬛🟨🟨🟨⬛⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛🟨⬛⬜⬛⬛⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬛🟨🟨⬛⬜⬛⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛⬜⬜⬜⬜⬜⬛🟫⬛🟫🟫⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟫🟫🟫⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛🟫⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟫🟫⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨🟫⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⠀⠀⠀⠀⠀
        """)

        self.generator_tab.layout.addWidget(self.generator_label)
        self.generator_tab.setLayout(self.generator_tab.layout)  



# Schedule Viewer Tab #########################################################################################
        
        sc = SchedulerController()

        def set_schedule_label(text: str) -> None:
            self.schedule_viewer_label.setText(text)

        def set_len_label(text: str) -> None:
            self.schedule_viewer_label_len.setText(text)

        #main layout
        self.schedule_viewer_tab.my_layout = QVBoxLayout()

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
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
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
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
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
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
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
        self.schedule_viewer_button.setFixedSize(100, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(popoutwindow)
        view_top_layout.addWidget(self.schedule_viewer_button) 

        #end top layout
        view_top_layout.addStretch()
        self.schedule_viewer_tab.my_layout.addLayout(view_top_layout) 

        # text for Schedule Viewer Tab
        self.schedule_viewer_label = QLabel()
        set_schedule_label("""Schedule by course will be shown here""")    
        self.schedule_viewer_tab.my_layout.addWidget(self.schedule_viewer_label)

        #push next widgets to bottom
        self.schedule_viewer_tab.my_layout.addStretch(1)

        #add bot layout
        view_bot_layout = QHBoxLayout()
        view_bot_layout.addStretch()

        #add prev_schedule button
        def schedule_back() -> None:
            sc.previous_schedule()
            self.schedule_viewer_label.setText(sc.get_format())
            self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))

        self.schedule_viewer_button = QPushButton("<--")
        self.schedule_viewer_button.setFixedSize(40, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(schedule_back)
        view_bot_layout.addWidget(self.schedule_viewer_button)

        #add label static text
        self.schedule_viewer_label_static = QLabel()
        self.schedule_viewer_label_static.setText("Schedule:")
        view_bot_layout.addWidget(self.schedule_viewer_label_static)

        #add index box
        def schedule_index_change(i: str) -> None:
            try:
                i = int(i)
                if i < 1:
                    sc.index = 0
                elif i > sc.length:
                    sc.index = sc.length - 1
                else:
                    sc.index = i - 1

                self.schedule_viewer_label.setText(sc.get_format())
                self.schedule_viewer_index.setPlaceholderText(str(sc.index + 1))

            except:
                pass
                    
        self.schedule_viewer_index = QLineEdit()
        self.schedule_viewer_index.setPlaceholderText("x")
        self.schedule_viewer_index.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.schedule_viewer_index.setFixedSize(30, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        
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
        self.schedule_viewer_button.setFixedSize(40, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
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
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
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
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(load_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        #end bot right sub layout
        view_bot_right_layout.addStretch()
        view_bot_layout.addLayout(view_bot_right_layout)

        #end bot layout
        self.schedule_viewer_tab.my_layout.addLayout(view_bot_layout)

        # Set final layout

        self.schedule_viewer_tab.setLayout(self.schedule_viewer_tab.my_layout)   
       
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def handleButton(self) -> None:
        self.modifier = ModClass(self)
        self.modifier.test()