import os
import cv2
import sys
import numpy as np

from PyQt5 import uic
from PyQt5.QtGui import QKeySequence, QPainter, QImage, QPixmap
from PyQt5.QtCore import QBasicTimer,  pyqtSlot, Qt, QPoint, QRect, QRectF 
from PyQt5.QtWidgets import  QFileDialog, QLabel,  QMainWindow, QMessageBox, QVBoxLayout, qApp

from ui.Main_ui import *
from .draw_api import *


class Detection_Label_Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Value
        self.step         = 0
        self.label        = 1
        self.startPoint   = QPoint()
        self.lastPoint    = QPoint()
        self.num_frames   = 0
        self.drawing      = False
        self.onFrame      = False
        self.onBox        = False
        self.boxNum       = -1
        self.timer        = QBasicTimer()
        self.main_layout  = QVBoxLayout()
        self.paint_widget = myQPaint()
        self.setMouseTracking(True)


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
        self.main_ui.button_pause.setShortcut(QKeySequence("S"))
        
        # Video Viewer
        self.setMouseTracking(True)
        self.main_ui.centralwidget.setMouseTracking(True)
        self.main_ui.frame_main_video.setMouseTracking(True)
        self.statusbar = self.statusBar()
        self.mouseFactor = QPoint(20,50)

        # Set Label Combo Box
        for label in CLASS_NAME.values():
            self.main_ui.text_label_selected.addItem(label)
            self.main_ui.text_label_change.addItem(label)
        
        # Box Controll Group
        self.main_ui.button_label_change.clicked.connect(self.on_Chnage_Label)
        self.main_ui.button_box_delete.clicked.connect(self.on_Box_Delete)
        self.main_ui.button_box_delete.setShortcut("del")

        # Combobox Initialize
        self.setting_combobox()
        self.main_ui.text_label_change.currentIndexChanged.connect(self.setting_combobox)
        self.main_ui.text_label_selected.currentIndexChanged.connect(self.setting_combobox)
    
    
    # =====================================================================================================================
    #                                               Qt Button Controller
    # =====================================================================================================================
    
    
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
    def on_Chnage_Label(self):
        r"""
        Change Label When Box Selected
        """
        now_label = self.main_ui.text_label_change.currentIndex()
        self.paint_widget.main_image.labels[self.boxNum] = now_label
        self.paint_widget.main_image.update()
    
    @pyqtSlot()
    def on_Box_Delete(self):
        r"""
        Button Controll For Box Delete
        """
        try:
            del self.paint_widget.main_image.rectangles[self.boxNum]
            del self.paint_widget.main_image.labels[self.boxNum]
            self.onBox = self.paint_widget.main_image.onBox = False
            self.boxNum = self.paint_widget.main_image.index = None
            self.paint_widget.main_image.update()
        except:
            QMessageBox.critical(self, "Box Selected Error!", "Please select the box!")


         
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
    
    def setting_combobox(self):
        # Setting for label setting combobox back ground color
        self.label = self.main_ui.text_label_selected.currentIndex()
        now_color = (CLASS_COLOR[self.label].red(), CLASS_COLOR[self.label].green(), CLASS_COLOR[self.label].blue(), 100)
        now_text_color = (255, 255, 255) if self.label == 0 else (0, 0, 0)
        self.main_ui.text_label_selected.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")
        self.main_ui.text_label_selected.show()

        # Setting for label setting combobox back ground color
        now_label = self.main_ui.text_label_change.currentIndex()
        now_color = (CLASS_COLOR[now_label].red(), CLASS_COLOR[now_label].green(), CLASS_COLOR[now_label].blue(), 100)
        now_text_color = (255, 255, 255) if now_label == 0 else (0, 0, 0)
        self.main_ui.text_label_change.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")
        self.main_ui.text_label_change.show()

    
    #=====================================================================================================================
    #                                                Mouse Evnet Handler
    #=====================================================================================================================

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)

        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor

        # Combobox setting
        self.setting_combobox()

        # Pressed If On Frame and Clicked Left Button - > Drawing Method
        if event.button() == Qt.LeftButton and self.onFrame:
            self.drawing = True
            self.original_point = event.pos()
            self.startPoint = self.endPoint = mousePos
            print(f"Press Original Point : ({self.original_point})")
            print(f"Press Correction Point : ({self.startPoint}), ({self.endPoint})")
        
        # Pressed If On Box and Clicked Right Button -> Box Controll Method
        if event.button() == Qt.RightButton:
            mouseX, mouseY = mousePos.x(), mousePos.y()
            for index, rect in enumerate(self.paint_widget.main_image.rectangles):
                x1, y1, x2, y2 = rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()
                if x1 <= mouseX and mouseX <= x2 and y1 <= mouseY and mouseY <= y2:
                    if self.boxNum != index:
                        self.onBox = True
                        self.boxNum = index
                    else:
                        self.onBox = True if not self.onBox else False
                        self.boxNum = -1

                    # Main Box Controll Combobox Update
                    now_label = self.paint_widget.main_image.labels[self.boxNum]
                    now_color = (CLASS_COLOR[now_label].red(), CLASS_COLOR[now_label].green(), CLASS_COLOR[now_label].blue(), 100)
                    now_text_color = (255, 255, 255) if now_label == 0 else (0, 0, 0)
                    self.main_ui.text_label_change.setCurrentIndex(now_label)
                    self.main_ui.text_label_change.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")

                    # Main Image Update
                    self.paint_widget.main_image.onBox = self.onBox
                    self.paint_widget.main_image.index = self.boxNum
                    self.paint_widget.main_image.update()
 
            

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)
        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor
        self.statusbar.showMessage(f"Mouse Pos = ({event.x()}, {event.y()}), global = ({event.globalX()}, {event.globalY()}), local = ({event.localPos().x()}, {event.localPos().y()}), On Frame = {self.onFrame}, Drawing = {self.drawing}, onBox = {self.onBox}")
        
        if mousePos.x() < self.main_ui.frame_main_video.frameGeometry().bottomRight().x() and \
            mousePos.y() <  self.main_ui.frame_main_video.frameGeometry().bottomRight().y():
            self.onFrame = True
        else:
            self.onFrame = False
            self.drawing = False

        if self.drawing and event.buttons and Qt.LeftButton:
            self.endPoint =  mousePos
            print(f"Moving Original Point : ({self.original_point})")
            print(f"Moving Point : ({self.startPoint}), ({self.endPoint})")
            self.paint_widget.drawing_rect(self.startPoint, self.endPoint, self.label)
            self.update()
            self.paint_widget.main_image.update()
            self.main_layout.update()

        
    def mouseReleaseEvent(self, event)->None:
        super().mouseReleaseEvent(event)
        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            self.endPoint = mousePos

            print(f"Release Original Point : ({self.original_point})")
            print(f"Release Point : ({self.startPoint}), ({self.endPoint})")
            self.paint_widget.main_image.rectangles.append(QRectF(self.startPoint, self.endPoint))
            self.paint_widget.main_image.labels.append(self.label)
            self.paint_widget.main_image.onBox = self.onBox =  True
            self.paint_widget.main_image.index = self.boxNum = len(self.paint_widget.main_image.rectangles) - 1
            print(f"Main Rectangles : {self.paint_widget.main_image.rectangles}")
            print(f"Main Labels     : {self.paint_widget.main_image.labels}")
            self.paint_widget.main_image.update()
            # self.paint_widget.drawing_points(self.boxNum)
            
        self.startPoint = self.endPoint = QPoint()
 
    
    #=====================================================================================================================
    #                                            Timer Event
    #=====================================================================================================================
    
            
    def timerEvent(self, e):
        r"""
        Timer Event Handler
        """
        #Initialize Paint Rectangle
        self.paint_widget.main_image.rectangles = []
        self.paint_widget.main_image.labels     = []

        # Error Checker
        try:
            self.hasFrame, self.frame = self.video.read()
            if self.step > self.num_frames or (not self.hasFrame):
                self.timer.stop()
                return

        except:
            QMessageBox.critical(self, "Splitting Error!", "Please click split button before the run!")
            self.timer.stop()
            return
        
        # Run Image to QTImage
        img = self.toQImage(self.frame)

        # Main Widget Update
        self.paint_widget.draw_img(img)
        self.paint_widget.main_image.update()

        # Main Layout Update
        self.main_layout.addWidget(self.paint_widget.main_image)
        self.main_layout.update()

        # Main Frame Update
        self.main_ui.frame_main_video.setLayout(self.main_layout)

        # Sequence Bar Controll
        self.main_ui.seqBar_main_video.setValue(self.step)
        self.main_ui.seqBar_main_video.setFormat(f"{self.step} / {self.num_frames}")
        self.step = self.step +1

    
    #=====================================================================================================================
    #                                            Other Controller
    #=====================================================================================================================
    

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
        

    
        
    