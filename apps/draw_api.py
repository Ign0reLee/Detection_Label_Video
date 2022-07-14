
from PyQt5.QtGui import QColor, QPainter, QImage, QPixmap, QPen, QBrush
from PyQt5.QtCore import  QPoint, QRect, QRectF, Qt
from PyQt5.QtWidgets import  QLabel, QWidget

from ui.Main_ui import *

CLASS_NAME = {0: "BackGround",
              1: "Duck",
              2: "Slapped",
              3: "Dead"}

CLASS_COLOR = {0: QColor(0, 0, 0),
               1: QColor(255, 0, 0),
               2: QColor(0, 255, 0),
               3: QColor(0, 0, 255)}

class myQLabel(QLabel):
    def __init__(self, parent=None):
        super(myQLabel, self).__init__(parent)
        self.rectangles = []
        self.labels     = []
        self.onBox      = False
        self.index      = None

    def paintEvent(self, QPaintEvent):
        super(myQLabel, self).paintEvent(QPaintEvent)
        painter = QPainter(self)
        
        for rect in self.rectangles:
            painter.setPen(QPen(rect.mainRect.qColor, 3, Qt.SolidLine))
            painter.drawRect(rect.mainRect.qBoxpts)

        if self.onBox:
            painter.setBrush(QBrush(self.rectangles[self.index].topLeft.qColor))
            for pts in self.rectangles[self.index].rectPts:
                painter.fillRect(pts.qBoxpts, QBrush(pts.qColor))

        painter.end()

        

class myQPaint(QWidget):
    def __init__(self):
        super(myQPaint, self).__init__()
        self.previousRect = QRect()
        self.Factor = QPoint(0, 55)
        self.resizes = (960, 540)
        self.initUI()
    
    def initUI(self):
        self.main_image = myQLabel(self)
    
    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        self.main_image.setPixmap(self.pixmap)
        
    def draw_img(self, img:QImage):
        self.pixmap = QPixmap(img)
        self.pixmap = self.pixmap.scaled(self.resizes[0], self.resizes[1], Qt.KeepAspectRatio)
        self.main_image.setPixmap(self.pixmap)
    
    def drawing_rect(self, start_points:QPoint, end_points:QPoint, label:int) -> None:
        box_points = QRectF(start_points + self.Factor, end_points + self.Factor)
        self.copy_pixmap = self.pixmap.copy()
        painter = QPainter(self.copy_pixmap)
        painter.setPen(QPen(CLASS_COLOR[label], 3, Qt.SolidLine))
        painter.drawRect(box_points)
        self.main_image.setPixmap(self.copy_pixmap)
        self.previousRect = box_points
        painter.end()
    
    # def drawing_points(self, box_index:int) -> None:
    #     # Make New Drawing Painter
    #     self.copy_pixmap = self.pixmap.copy()
    #     painter = QPainter(self.copy_pixmap)
    #     painter.setPen(QPen(QColor(255, 255, 255), 6, Qt.SolidLine))
    #     rect = self.main_image.rectangles[box_index]
    #     topLeft = rect.topLeft() + self.Factor
    #     botRgiht = rect.bottomRight() + self.Factor
    #     x1, y1, x2, y2 = topLeft.x(), topLeft.y(), botRgiht.x(), botRgiht.y()

    #     # Top 3 Points
    #     painter.drawPoint(topLeft)
    #     painter.drawPoint(QPoint((x1 + x2)//2, y1))
    #     painter.drawPoint(QPoint(x2, y1))
    #     # Middle 2 Points
    #     painter.drawPoint(QPoint(x1, (y1+y2)//2))
    #     painter.drawPoint(QPoint(x2, (y1+y2)//2))
    #     # Bottom 3 Points
    #     painter.drawPoint(QPoint(x1, y2))
    #     painter.drawPoint(QPoint((x1 + x2)//2, y2))
    #     painter.drawPoint(botRgiht)

    #     self.main_image.setPixmap(self.copy_pixmap)
   
     