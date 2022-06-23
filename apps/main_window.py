import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QMainWindow, QPushButton, qApp
from ui.Main_ui import *


class Detection_Label_Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # ui connect and ready
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)

        # # Action Setting
        self.setActtion()

        # # Set My Menu
        # self.setMyMenu()

        # Show Main UI
        self.show()
    
    def setActtion(self):
        # Main Menu
        self.main_ui.EXIT.setShortcut('Alt+F4')
        self.main_ui.EXIT.setStatusTip('Exit application')
        self.main_ui.EXIT.triggered.connect(qApp.quit)
    
    # def setMyMenu(self):
    #     self.EXIT
    #     self.main_ui.EXIT.addAction(self.exitAction)