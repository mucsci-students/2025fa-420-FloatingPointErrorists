import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QMainWindow, QCheckBox, QComboBox
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import Qt

sys.path.append('../controller')
from scheduler_cli.controller.Tomtest import ModClass
from scheduler_cli.controller.viewer_controller import viewerClass

"""Simple Gui Window Initializer"""

class SimpleGUI(QMainWindow):

    def __init__(self):
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
    my_layout: QVBoxLayout

    def __init__(self, parent):

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

        #type checking tabs
        self.schedule_viewer_tab.my_layout = QVBoxLayout()

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
        def set_schedule_label(text: str) -> None:
            self.schedule_viewer_label.setText(text)

        #main layout
        self.schedule_viewer_tab.my_layout = QVBoxLayout()

        #add top layout
        view_top_layout = QHBoxLayout(self)

        #add view_by_courses button
        def view_by_courses() -> None:
            self.modifier = viewerClass(self)
            self.modifier.change_schedule('Courses') #temp code GET COURSE SCHEDULE HERE

        self.schedule_viewer_button = QPushButton("Courses")
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(view_by_courses)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_faulty button
        def view_by_faulty() -> None:
            self.modifier = viewerClass(self)
            self.modifier.change_schedule('Faculty') #temp code GET FAULTY SCHEDULE HERE

        self.schedule_viewer_button = QPushButton("Faculty")
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(view_by_faulty)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #add view_by_room button
        def view_by_room() -> None:
            self.modifier = viewerClass(self)
            self.modifier.change_schedule('Rooms') #temp code GET ROOM SCHEDULE HERE

        self.schedule_viewer_button = QPushButton("Room")
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(view_by_room)
        view_top_layout.addWidget(self.schedule_viewer_button)  

        #end top layout
        view_top_layout.addStretch()
        self.schedule_viewer_tab.my_layout.addLayout(view_top_layout) 

        # text for Schedule Viewer Tab
        self.schedule_viewer_label = QLabel()
        set_schedule_label("""
Schedule
        """)
        
        self.schedule_viewer_tab.my_layout.addWidget(self.schedule_viewer_label)

        #push next widgets to bottom
        self.schedule_viewer_tab.my_layout.addStretch(1)

        #add bot layout
        view_bot_layout = QHBoxLayout()
        view_bot_layout.addStretch()

        #add prev_schedule button
        def schedule_back() -> None:
            self.modifier = viewerClass(self)
            self.modifier.change_schedule('<==') #temp code GET PREV SCHEDULE HERE

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
            self.modifier = viewerClass(self)
            self.modifier.change_schedule(i) #temp code GET SCHEDULE BY INDEX HERE
        
        self.schedule_viewer_index = QLineEdit()
        self.schedule_viewer_index.setPlaceholderText("0")
        self.schedule_viewer_index.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.schedule_viewer_index.setFixedSize(30, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        
        self.schedule_viewer_index.returnPressed.connect(lambda: schedule_index_change(self.schedule_viewer_index.text()))
        view_bot_layout.addWidget(self.schedule_viewer_index)

        #add label static suffix
        self.schedule_viewer_label_static2 = QLabel()
        self.schedule_viewer_label_static2.setText("/" + "n") #temp code ADD TOTAL NUMBER OF SCHEDULES HERE
        view_bot_layout.addWidget(self.schedule_viewer_label_static2)

        #add next_schedule button
        def schedule_forward() -> None:
            self.modifier = viewerClass(self)
            self.modifier.change_schedule('==>') #temp code GET NEXT SCHEDULE HERE

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
            r = ""
            if checkbox1.isChecked():
                #INSERT SAVE JSON FUNCTION HERE
                r = "json" #temp code
            if checkbox2.isChecked():
                #INSERT SAVE CSV FUNCTION HERE
                r = r + " csv" #temp code
            self.schedule_viewer_label.setText(r)

        self.schedule_viewer_button = QPushButton("Save")
        self.schedule_viewer_button.setFixedSize(80, 30)  # width, height in pixels CURRENTLY NOT RELATIVE
        self.schedule_viewer_button.clicked.connect(save_button) 
        view_bot_right_layout.addWidget(self.schedule_viewer_button)

        # Load button
        def load_button() -> None:
            self.modifier = viewerClass(self)
            self.schedule_viewer_label.setText("load_button") #temp code LOAD SCHEDULE HERE
        
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

    def handleButton(self):
        self.modifier = ModClass(self)
        self.modifier.test()