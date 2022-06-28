
from PyQt5 import uic
from PyQt5.QtGui import QColor, QPainter, QImage, QPixmap, QPen
from PyQt5.QtCore import QBasicTimer, QPoint, QRect,  pyqtSlot, Qt
from PyQt5.QtWidgets import  QLabel, QWidget

from ui.Main_ui import *

class myQLabel(QLabel):
    def __init__(self, parent=None):
        super(myQLabel, self).__init__(parent)
        self.rectangles = []

    def paintEvent(self, QPaintEvent):
        super(myQLabel, self).paintEvent(QPaintEvent)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255,0,0, 255), 3, Qt.SolidLine))
        print(self.rectangles)
        if self.rectangles:
            painter.drawRects(self.rectangles)
        painter.end()



class myQPaint(QWidget):
    def __init__(self):
        super(myQPaint, self).__init__()
        self.previousRect = QRect()
        self.initUI()
    
    def initUI(self):
        self.main_image = myQLabel(self)

    def draw_img(self, img:QImage):
        self.pixmap = QPixmap(img)
        self.pixmap = self.pixmap.scaled(1060, 500, Qt.KeepAspectRatio)
        self.main_image.setPixmap(self.pixmap)
    
    def drawing_rect(self, start_points:QPoint, end_points:QPoint) -> None:
        box_points = QRect(start_points, end_points)
        self.copy_pixmap = self.pixmap.copy()
        painter = QPainter(self.copy_pixmap)
        painter.setPen(QPen(QColor(255,0,0, 255), 3, Qt.SolidLine))
        painter.drawRect(box_points)
        self.main_image.setPixmap(self.copy_pixmap)

        self.previousRect = box_points
   
     