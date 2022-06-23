import os
import sys

from PyQt5.QtWidgets import QApplication
from apps import *
from ui import *


if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = Detection_Label_Main_Window()
   app.exec_()