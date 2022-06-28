
from PyQt5 import uic
<<<<<<< HEAD
from PyQt5.QtGui import QColor, QPainter, QImage, QPixmap, QPen
from PyQt5.QtCore import QBasicTimer, QPoint, QRect,  pyqtSlot, Qt
=======
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtCore import QBasicTimer,  pyqtSlot
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2
from PyQt5.QtWidgets import  QLabel, QWidget

from ui.Main_ui import *

class myQLabel(QLabel):
<<<<<<< HEAD
    def __init__(self, parent=None):
        super(myQLabel, self).__init__(parent)
        self.rectangles = []
=======
    def __init__(self,parent=None):
        super(myQLabel, self).__init__(parent)
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2

    def paintEvent(self, QPaintEvent):
        super(myQLabel, self).paintEvent(QPaintEvent)
        painter = QPainter(self)
<<<<<<< HEAD
        painter.setPen(QPen(QColor(255,0,0, 255), 3, Qt.SolidLine))
        print(self.rectangles)
        if self.rectangles:
            painter.drawRects(self.rectangles)
        painter.end()



class myQPaint(QWidget):
    def __init__(self):
        super(myQPaint, self).__init__()
        self.previousRect = QRect()
=======
        # painter.setPen(QPen(Qt.red))
        # painter.drawArc(QRectF(50, 50, 10, 10), 0, 5760)
        # painter.drawRect(QRectF(50, 50, 100, 100) )

class Main_Paint(QWidget):
    def __init__(self,parent):
        super(Main_Paint, self).__init__()
        self.main_image_name="icons\\add.png"
        self.mode = 5

>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2
        self.initUI()
    
    def initUI(self):
        self.main_image = myQLabel(self)
<<<<<<< HEAD

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
   
     
=======
        self.main_image.setPixmap(QPixmap(self.main_image_name))
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2
