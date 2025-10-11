import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QComboBox, QGridLayout, QVBoxLayout, QTabWidget, QMainWindow
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt
from scheduler.models import CourseInstance

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
        from scheduler_config_editor.view.generator_gui import setup_generator_tab

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
        self.editor_tab.layout = QGridLayout(self)
        self.editor_tab.setLayout(self.editor_tab.layout)

        #self.editor_label = QLabel()
        """self.editor_label.setText(
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
        )
        """

        #self.editor_tab.layout.addWidget(self.editor_label)
        #self.editor_tab.setLayout(self.editor_tab.layout)

        # Dropdown code
        # self.editor_combo_box.layout = QVBoxLayout(self)
        self.editor_combo_box = QComboBox()

        self.editor_combo_box.addItems(['Course', 'Room', 'Lab', 'Faculty'])

        self.editor_tab.layout.addWidget(self.editor_combo_box, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)


        # Code for testing testing.py with a button
        # self.button = QPushButton("Test button")
        # self.editor_tab.layout.addWidget(self.button)
        
        # self.button.clicked.connect(self.handleButton)

        self.schedule_viewer_tab.layout = QVBoxLayout(self)
        self.schedule_viewer_label = QLabel()
        self.schedule_viewer_label.setText("""
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢦⣶⣯⣓⢚⠻⢿⣶⡤⢒⡰⠴⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣯⡭⡕⠰⣈⠆⣉⠒⣄⠢⡹⢭⣿⡴⣈⡙⠦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣿⣿⢋⢒⡰⢈⠵⣄⠚⡤⢩⢄⢓⡰⡁⢎⠻⣵⡜⣌⢫⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡸⢋⣥⡿⢋⡔⣊⡴⡍⣶⣧⡍⡴⢧⣊⠖⡰⣉⠦⡙⠼⣷⣈⠦⢻⡦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠖⢛⣿⠱⣽⣿⢡⣳⣾⣏⣾⣽⣿⣿⣿⣾⣷⣽⣮⠱⣌⢖⣫⡳⢼⡆⢯⡱⢻⡵⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡯⣽⣿⣿⣳⣿⠿⠿⠻⠿⡻⢻⣿⣿⣿⣻⢿⣟⡜⣎⢶⣻⣗⢾⣡⡟⣭⢷⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⡼⠇⠀⠀⠀⠀⠁⠁⠉⠻⡟⢿⣿⣿⣯⣽⣷⣞⣿⣷⢻⣿⣷⣫⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⣸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠹⡞⠿⣿⣿⣿⣿⣯⡟⣿⣿⣷⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠼⡂⣿⣿⣿⣿⣟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣽⣻⣿⣿⣿⡟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⡟⠀⢀⢀⡀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠐⠉⣿⣿⣿⣞⣿⢿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⠀⠀⠀⠀⣀⠀⠆⠀⠀⠀⠀⠀⠀⢁⡰⠆⠀⠀⠀⣿⣿⣿⣿⣿⡎⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡏⠀⣴⡾⣦⣍⠘⣆⠀⠀⠀⠀⠀⣴⠛⢹⣿⡲⠀⢽⣿⣿⣿⢋⢱⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿⣿⣿⠘⠏⠀⢻⡏⠀⠀⡄⠀⠀⠀⠀⠙⠀⠘⠍⠀⠀⡸⣿⣟⣿⡬⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣇⠈⠀⠂⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠘⣩⣴⣿⡛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⢕⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠑⡀⠀⠀⠀⣸⣇⢠⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⡠⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠈⠙⠣⠋⠀⠀⠀⠀⠀⠀⠀⠀⣰⠙⣿⢿⡌⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠈⠀⠒⠒⠂⠀⠀⠄⠊⠀⠀⢀⢮⠃⠀⠃⢸⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠄⠀⠙⠃⠀⠀⠀⠀⠀⣠⠒⣭⠆⠀⠀⠀⣸⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣦⣀⠀⠀⠀⢀⣤⠚⡥⢋⡜⠁⠀⠀⢀⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⢿⢫⡝⣩⢋⠴⣉⡶⠏⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⡟⠀⢑⢾⣠⢋⣶⠉⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⠃⠀⠈⡆⢷⣘⠆⢀⡄⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⢀⠀⢰⣷⠈⡞⢀⣾⡿⠂⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢘⠂⡞⣿⣧⣶⣾⣿⠁⠀⠄⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢨⡰⠁⢿⣿⣷⣻⢾⠋⠀⠈⠄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠘⠕⠡⠈⢿⣷⣯⣟⠀⠀⠀⢁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⡀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠘⠀⠀⠀⠀⣼⡿⣿⣯⣷⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠁⠀⠀⠀⠀⣿⣿⣯⢷⣯⡧⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢀⣿⢿⣽⣻⡾⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣼⣟⡿⣞⣷⢿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⣸⣿⢯⣿⢿⣽⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣹⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣈⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⢰⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢀⡷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣼⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣶⣟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⡽⣞⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⠾⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣻⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡽⣶⣳⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        """)

        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_label)
        self.schedule_viewer_tab.setLayout(self.schedule_viewer_tab.layout)   


        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        def handle_generated_schedules(schedules: list[list[CourseInstance]]) -> None:
            pass # REPLACE WITH WHATEVER METHOD UPDATES VIEWER

        # GENERATOR
        setup_generator_tab(self, None, handle_generated_schedules)
        # GENERATOR END

    def handleButton(self) -> None:
        self.modifier = ModClass(self)
        self.modifier.test()

    # GENERATOR
    def handle_generated_schedules(schedules: list[list[CourseInstance]]) -> None:
        pass
    # GENERATOR END