import numpy as np

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import  QPoint, QRectF,  Qt
from PyQt5.QtWidgets import  QApplication

CLASS_NAMES = {0: "BackGround",
              1: "Duck",
              2: "Slapped",
              3: "Dead"}

CLASS_COLORS = {0: (0, 0, 0),
               1: (255, 0, 0),
               2: (0, 255, 0),
               3: (0, 0, 255)}


class BaseRect(object):
    def __init__(self, start_points:QPoint, end_points:QPoint, label:int) -> None:
        # Python Parameters
        self.Boxpts  = (start_points.x(), start_points.y(), end_points.x(), end_points.y())
        self.x1, self.y1, self.x2, self.y2 = self.Boxpts
        self.label   = label
        self.name    = CLASS_NAMES[label]
        self.color   = CLASS_COLORS[label]

        # PyQt Parameters
        self.qBoxpts = QRectF(start_points, end_points)
        self.qColor  = QColor(self.color[0], self.color[1], self.color[2])
    
    def checkInBox(self, mouseX:int, mouseY:int, margine:int = 0)->bool:
        # Check Mouse Pos In-Box or not
        if self.x1 - margine <= mouseX and mouseX <= self.x2 + margine and self.y1 - margine <= mouseY and mouseY <= self.y2 + margine:
            return True
        else:
            return False
    
    def updateLabel(self) -> None:
        # Python Parameters
        self.name    = CLASS_NAMES[self.label]
        self.color   = CLASS_COLORS[self.label]

        # PyQt Parameters
        self.qColor  = QColor(self.color[0], self.color[1], self.color[2])
    
    def updatePos(self) -> None:
        # Python Parameters
        self.Boxpts  = (self.qBoxpts.topLeft().x(), self.qBoxpts.topLeft().y(), self.qBoxpts.bottomRight().x(), self.qBoxpts.bottomRight().y())
        self.x1, self.y1, self.x2, self.y2 = self.Boxpts

        

class verRect(BaseRect):
    def __init__(self, start_points:QPoint, end_points:QPoint, label:int) -> None:
        super(verRect, self).__init__(start_points, end_points, label)
        self.qColor = QColor(255,255,255)
    
    def checkInBox(self, mouseX: int, mouseY: int, margine: int = 0) -> bool:
        if super().checkInBox(mouseX, mouseY, margine):
            QApplication.setOverrideCursor(QCursor(Qt.SizeVerCursor))
            return True
        else:
            return False

    def updatePos(self) -> None:
        return super().updatePos()

class horRect(BaseRect):
    def __init__(self, start_points:QPoint, end_points:QPoint, label:int) -> None:
        super().__init__(start_points, end_points, label)
        self.qColor = QColor(255,255,255)
    
    def  checkInBox(self, mouseX: int, mouseY: int, margine: int = 0) -> bool:
        if super().checkInBox(mouseX, mouseY, margine):
            QApplication.setOverrideCursor(QCursor(Qt.SizeHorCursor))
            return True
        else:
            return False

    def updatePos(self) -> None:
        return super().updatePos()


class digRect(BaseRect):
    def __init__(self,  start_points:QPoint, end_points:QPoint, label:int, left:bool=True) -> None:
        super().__init__(start_points, end_points, label)
        self.qColor = QColor(255,255,255)
        self.left = left
    
    def checkInBox(self, mouseX: int, mouseY: int, margine: int = 0) -> bool:
        if super().checkInBox(mouseX, mouseY, margine):
            if self.left:
                QApplication.setOverrideCursor(QCursor(Qt.SizeFDiagCursor))
            else:
                QApplication.setOverrideCursor(QCursor(Qt.SizeBDiagCursor))
            return True
        else:
            return False
    def updatePos(self) -> None:
        return super().updatePos()



class rectInfo(object):
    def __init__(self, **kwargs)->None:
        r"""
        """
        self.ptsSize  = kwargs["ptsSize"] // 2
        self.label    = kwargs["label"]
        self.mainRect = BaseRect(kwargs["start_points"], kwargs["end_points"], kwargs["label"]) 
        

        self.__boxPTS__()
        self.setPoint()
        self.direction = (((1, 1),  (0,0)),
                           ((0, 1), (0, 0)),
                           ((0, 1), (1, 0)),
                           ((1, 0), (0, 0)),
                           ((0, 0), (1, 0)), 
                           ((1, 0), (0, 1)),
                           ((0, 0), (0, 1)),
                           ((0, 0), (1, 1)))

    def __boxPTS__(self) -> None:
        # All Box Points Calculation
        self.minX1 = self.mainRect.x1 - self.ptsSize
        self.maxX1 = self.mainRect.x1 + self.ptsSize
        self.minY1 = self.mainRect.y1 - self.ptsSize
        self.maxY1 = self.mainRect.y1 + self.ptsSize
        self.minX2 = self.mainRect.x2 - self.ptsSize
        self.maxX2 = self.mainRect.x2 + self.ptsSize
        self.minY2 = self.mainRect.y2 - self.ptsSize
        self.maxY2 = self.mainRect.y2 + self.ptsSize
        self.minMidX = ((self.mainRect.x1 + self.mainRect.x2) // 2) - self.ptsSize
        self.maxMidX = ((self.mainRect.x1 + self.mainRect.x2) // 2) + self.ptsSize
        self.minMidY = ((self.mainRect.y1 + self.mainRect.y2) // 2) - self.ptsSize
        self.maxMidY = ((self.mainRect.y1 + self.mainRect.y2) // 2) + self.ptsSize

    def setPoint(self) -> None:
        self.topLeft  = digRect(QPoint(self.minX1, self.minY1), QPoint(self.maxX1, self.maxY1), label=self.label, left=True)
        self.topMid   = verRect(QPoint(self.minMidX, self.minY1), QPoint(self.maxMidX, self.maxY1), label=self.label)
        self.topRight = digRect(QPoint(self.minX2, self.minY1), QPoint(self.maxX2, self.maxY1), label=self.label, left=False)
        self.midLeft  = horRect(QPoint(self.minX1, self.minMidY), QPoint(self.maxX1, self.maxMidY), label=self.label)
        self.midRight = horRect(QPoint(self.minX2, self.minMidY), QPoint(self.maxX2, self.maxMidY), label=self.label)
        self.botLeft  = digRect(QPoint(self.minX1, self.minY2), QPoint(self.maxX1, self.maxY2), label=self.label, left=False)
        self.botMid   = verRect(QPoint(self.minMidX, self.minY2), QPoint(self.maxMidX, self.maxY2), label=self.label)
        self.botRight = digRect(QPoint(self.minX2, self.minY2), QPoint(self.maxX2, self.maxY2), label=self.label, left=True)
        self.rectPts  = (self.topLeft, self.topMid, self.topRight, self.midLeft, self.midRight, self.botLeft, self.botMid, self.botRight)


    def checkInBox(self, mouseX: int, mouseY: int, margine: int = 0) -> bool:
        return self.mainRect.checkInBox(mouseX, mouseY, margine)

    def moveBoxes(self, movePts:QPoint) -> None:
        self.mainRect.qBoxpts.moveTo(self.mainRect.qBoxpts.topLeft() - movePts)
        self.mainRect.updatePos()
        for rect in self.rectPts:
            rect.qBoxpts.moveTo(rect.qBoxpts.topLeft() - movePts)
            rect.updatePos()

    def extendBoxes(self, movePts:QPoint, direction:int) -> None:
        x, y = movePts.x(), movePts.y()
        topML = QPoint((x * self.direction[direction][0][0]), (y * self.direction[direction][0][1]))
        botMR = QPoint((x * self.direction[direction][1][0]), (y * self.direction[direction][1][1]))
        topLeft = self.mainRect.qBoxpts.topLeft() - topML 
        botRgiht = self.mainRect.qBoxpts.bottomRight() - botMR
        self.mainRect.qBoxpts = QRectF(topLeft, botRgiht)
        self.mainRect.updatePos()
        self.__boxPTS__()
        self.setPoint()
