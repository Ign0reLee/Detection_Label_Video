import os
import cv2
import sys
import numpy as np

from PyQt5 import uic
<<<<<<< HEAD
from PyQt5.QtGui import QPainter, QImage, QPixmap
from PyQt5.QtCore import QBasicTimer,  pyqtSlot, Qt, QPoint, QRect, QRectF 
from PyQt5.QtWidgets import  QFileDialog, QLabel,  QMainWindow, QMessageBox, QVBoxLayout, qApp
=======
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QBasicTimer,  pyqtSlot
from PyQt5.QtWidgets import  QFileDialog,  QMainWindow, QMessageBox, qApp
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2

from ui.Main_ui import *
from .draw_api import *


class Detection_Label_Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Value
<<<<<<< HEAD
        self.step         = 0
        self.startPoint   = QPoint()
        self.lastPoint    = QPoint()
        self.num_frames   = 0
        self.drawing      = False
        self.onFrame      = False
        self.timer        = QBasicTimer()
        self.main_layout  = QVBoxLayout()
        self.paint_widget = myQPaint()

        

=======
        self.step = 0
        self.num_frames = 0
        self.timer = QBasicTimer()
        self.frame = np.zeros((224,224,3))
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2

        # ui connect and ready
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        

        # Action Setting
        self.setAction()

        # Main Loop
        self.show()
    
    def setAction(self):
        r"""
        Additional Action Setting
        """
        # Main Menu
        self.main_ui.EXIT.setShortcut('Alt+F4')
        self.main_ui.EXIT.setStatusTip('Exit application')
        self.main_ui.EXIT.triggered.connect(qApp.quit)

        # Out Button Group
        self.main_ui.out_botton.accepted.connect(qApp.quit)
        self.main_ui.out_botton.button(QtWidgets.QDialogButtonBox.Ok).setShortcut("Ctrl+return")
        self.main_ui.out_botton.rejected.connect(qApp.quit)
        self.main_ui.out_botton.button(QtWidgets.QDialogButtonBox.Cancel).setShortcut("Alt+F4")

        # Video Setting Group
        self.main_ui.button_set_save_path.clicked.connect(self.on_folderOpen)
        self.main_ui.button_video_path.clicked.connect(self.on_videoOpen)
        self.main_ui.button_split_video.clicked.connect(self.on_split)

        # # Video Controllor Group
        self.main_ui.button_pause.clicked.connect(self.on_Pause)
        self.main_ui.button_pause.setShortcut("space")
        
        # Video Viewer
<<<<<<< HEAD
        # self.qp = QPainter(self.main_ui.frame_main_video).
        self.setMouseTracking(True)
        self.statusbar = self.statusBar()
        
=======
        # self.qp = QPainter(self.main_ui.frame_main_video)
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2
    
    @pyqtSlot()
    def on_folderOpen(self):
        r"""
        Set Save Path Button Event Handler
        """
        self.save_folder = QFileDialog.getExistingDirectory(self, "Select Directory", os.path.join("."))
        self.main_ui.text_save_path.setText(self.save_folder)
        self.main_ui.text_save_path.setStyleSheet("color:black;")
    
    @pyqtSlot()
    def on_videoOpen(self):
        r"""
        Set Video Path Button Event Handler
        """
        self.video_path =  QFileDialog.getOpenFileName(self, "Select Video", filter="*.mp4 *.avi")[0]
        self.main_ui.text_video_path.setText(self.video_path)
        self.main_ui.text_video_path.setStyleSheet("color:black;")
    
    @pyqtSlot()
    def on_split(self):
        r"""
        Set Video Spliter Button Event Handler
        """
        # GET Information
        self.split_fps = self.main_ui.text_FPS.toPlainText().lower()
        self.num_class = self.main_ui.text_class.toPlainText()
        self.nms_score = self.main_ui.text_NMS.toPlainText()

        # Check the error
        if self.check_video_error():
            return 
        
        self.video_spliter()

    @pyqtSlot()
    def on_Pause(self):
        r"""
        Pause Event Handler
        When Pausing Changing Start Event
        """
        if self.timer.isActive():
            self.timer.stop()
            self.main_ui.button_pause.setText("Start")

        else:
            self.timer.start(self.num_frames, self)
            self.main_ui.button_pause.setText("Pause")
         
    @pyqtSlot()
    def video_spliter(self):
        r"""
        Contorl Spliting Event
        """

        self.video = cv2.VideoCapture(self.video_path)
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = self.video.get(cv2.CAP_PROP_FPS)
        self.num_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        self.main_ui.seqBar_main_video.setMaximum(self.num_frames)

        print(width)
        print(height)
        print(frames_per_second)
        print(self.num_frames)
<<<<<<< HEAD
        print(self.main_ui.frame_main_video.geometry())
        print(self.main_ui.frame_main_video.frameGeometry().bottomRight().x())
        print(self.main_ui.frame_main_video.frameGeometry().bottomRight().y())

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.onFrame:
            self.drawing = True
            self.startPoint = self.endPoint = event.pos()
            

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)
        self.statusbar.showMessage(f"Mouse Pos = ({event.x()}, {event.y()}), global = ({event.globalX()}, {event.globalY()}), On Frame = {self.onFrame}, Drawing = {self.drawing}")
        if event.pos().x() < self.main_ui.frame_main_video.frameGeometry().bottomRight().x() and \
            event.pos().y() <  self.main_ui.frame_main_video.frameGeometry().bottomRight().y():
            self.onFrame = True
        else:
            self.onFrame = False
            self.drawing = False

        if self.drawing and event.buttons and Qt.LeftButton:
            self.endPoint = event.pos()
            # self.paint_widget.main_image.box_pos = QRect(self.startPoint, self.endPoint)
            self.paint_widget.drawing_rect(self.startPoint, self.endPoint)
            self.update()
            self.paint_widget.main_image.update()
            self.main_layout.update()

        
    def mouseReleaseEvent(self, event)->None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.drawing:
            
            self.drawing = False
            self.endPoint = event.pos()
            
            self.startPoint -= self.main_ui.frame_main_video.frameGeometry().topLeft()
            self.endPoint   -= self.main_ui.frame_main_video.frameGeometry().topLeft()
            self.startPoint -= self.main_ui.Group_Main_Video_Viewer.frameGeometry().topLeft()
            print(self.startPoint)
            print(self.endPoint)
            self.paint_widget.main_image.rectangles.append(QRectF(self.startPoint, self.endPoint))
            self.paint_widget.main_image.update()
            
        self.startPoint = self.endPoint = QPoint()
 
=======
    
   
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2
    
            
    def timerEvent(self, e):
        r"""
        Timer Event Handler
        """
        self.hasFrame, self.frame = self.video.read()
        if self.step > self.num_frames or (not self.hasFrame):
            self.timer.stop()
            return
        img = self.toQImage(self.frame)
<<<<<<< HEAD
        self.paint_widget.draw_img(img)
        self.paint_widget.main_image.update()
        self.main_layout.addWidget(self.paint_widget.main_image)
        self.main_layout.update()
        self.main_ui.frame_main_video.setLayout(self.main_layout)
        self.main_ui.seqBar_main_video.setValue(self.step)
        self.main_ui.seqBar_main_video.setFormat(f"{self.step} / {self.num_frames}")
        self.step = self.step +1

=======

        self.qp.drawImage(self.rect(), img)

        self.main_ui.frame_main_video.update()
        self.main_ui.seqBar_main_video.setValue(self.step)
        self.main_ui.seqBar_main_video.setFormat(f"{self.step} / {self.num_frames}")
        self.step = self.step +1
    

    def paintEvent(self, event):
        self.main_ui.frame_main_video.paintEvent(event)
        self.qp = QPainter(self)
        # self.qp.end()
>>>>>>> 11891b11762af252c6849e652a11f32ee118a2d2

    def toQImage(self, img, copy=False):
        r"""
        Make Numpy Image to QImage
        """
        if img is None:
            return QImage()

        if img.dtype == np.uint8:
            if len(img.shape) == 2:
                qim = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(self.gray_color_table)
                return qim.copy() if copy else qim
                
            elif len(img.shape) == 3:
                if img.shape[2] == 3:
                    qim = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif img.shape[2] == 4:
                    qim = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if copy else qim


    def check_video_error(self):
        r"""
        Check the error of Video Setting
        If find error return False
        """
        try:
            self.num_class = int(self.num_class)
        except:
            QMessageBox.critical(self, "Class Error!", "Set class must be integer types")
            return True
        try:
            self.nms_score = float(self.nms_score)
        except:
            QMessageBox.critical(self, "NMS Error!", "Set NMS must be floating-point types")
            return True
        try:
            if self.split_fps != "none":
                self.split_fps = int(self.split_fps)
            else:
                self.split_fps = None
        except:
            QMessageBox.critical(self, "FPS Error!", "Set FPS must be integer types")
            return True
        
        try :
            if not os.path.exists(self.video_path):
                raise ValueError
        except:
            QMessageBox.critical(self, "Video Path Error!", "Please set the Video Path using open video button!")
            return True
        
        try :
            if not os.path.exists(self.save_folder):
                raise ValueError
        except:
            QMessageBox.critical(self, "Save Folder Path Error!", "Please set the Save Folder Path using save path button!")
            return True

        return False
   
        
        

        



    # def read_video(self):
        

    
        
    