
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtCore import QBasicTimer,  pyqtSlot
from PyQt5.QtWidgets import  QLabel, QWidget

from ui.Main_ui import *

class myQLabel(QLabel):
    def __init__(self,parent=None):
        super(myQLabel, self).__init__(parent)

    def paintEvent(self, QPaintEvent):
        super(myQLabel, self).paintEvent(QPaintEvent)
        painter = QPainter(self)
        # painter.setPen(QPen(Qt.red))
        # painter.drawArc(QRectF(50, 50, 10, 10), 0, 5760)
        # painter.drawRect(QRectF(50, 50, 100, 100) )

class Main_Paint(QWidget):
    def __init__(self,parent):
        super(Main_Paint, self).__init__()
        self.main_image_name="icons\\add.png"
        self.mode = 5

        self.initUI()
    
    def initUI(self):
        self.main_image = myQLabel(self)
        self.main_image.setPixmap(QPixmap(self.main_image_name))