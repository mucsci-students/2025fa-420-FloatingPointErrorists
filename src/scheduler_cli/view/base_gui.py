import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QMainWindow, QCheckBox, QComboBox
from PyQt6.QtGui import QGuiApplication

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
        def set_schedule_label(text):
            self.schedule_viewer_label.setText(text)

        self.schedule_viewer_tab.layout = QVBoxLayout(self)

        # text for Schedule Viewer Tab
        self.schedule_viewer_label = QLabel()
        set_schedule_label("""
Schedule
        """)
        
        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_label)

        #add courses dropdown box
        def course_dropdown_change(schedule):
            #GO TO SELECTED SCHEDULE FUNCTION HERE
            self.schedule_viewer_label.setText(schedule) #temp code

        dropdown = QComboBox()
        dropdown.setEditable(True)
        dropdown.addItems(["Hogg", "Hobb", "Zopetti"]) #temp code
        #on selection change
        self.schedule_viewer_tab.layout.addWidget(dropdown)

        #add prev_schedule button
        def schedule_back():
            #GO TO PREVIOUS SCHEDULE FUNCTION HERE
            self.schedule_viewer_label.setText("prev") #temp code

        self.schedule_viewer_button = QPushButton("backarrow")
        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_button)
        self.schedule_viewer_button.clicked.connect(schedule_back)

        #add next_schedule button
        #def schedule_forward():
        #    x = testFun()
        #    self.schedule_viewer_label.setText(x) #temp code

        self.schedule_viewer_button = QPushButton("forwardarrow")
        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_button) 
        sys.path.append('../controller')
        from viewer import testFun
        self.schedule_viewer_button.clicked.connect(testFun())

        #add index box
        def schedule_index_change(i):
            #GO TO INDEX SCHEDULE FUNCTION HERE
            self.schedule_viewer_label.setText(i) #temp code
        
        self.schedule_viewer_index = QLineEdit()
        self.schedule_viewer_index.setPlaceholderText("Enter Schedule Index")
        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_index)
        self.schedule_viewer_index.returnPressed.connect(lambda: schedule_index_change(self.schedule_viewer_index.text()))

        #add checkboxs
        checkbox1 = QCheckBox('json')
        self.schedule_viewer_tab.layout.addWidget(checkbox1)
        checkbox2 = QCheckBox('csv')
        self.schedule_viewer_tab.layout.addWidget(checkbox2)

        # Save button for Schedule Viewer Tab
        def on_schdeuler_click():
            r = ""
            if checkbox1.isChecked():
                #INSERT SAVE JSON FUNCTION HERE
                r = "json" #temp code
            if checkbox2.isChecked():
                #INSERT SAVE CSV FUNCTION HERE
                r = r + " csv" #temp code
            self.schedule_viewer_label.setText(r)


        self.schedule_viewer_button = QPushButton("Save")
        self.schedule_viewer_tab.layout.addWidget(self.schedule_viewer_button)
        self.schedule_viewer_button.clicked.connect(on_schdeuler_click)

        # Set layout
        self.schedule_viewer_tab.setLayout(self.schedule_viewer_tab.layout)   
        


        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)