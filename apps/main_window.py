import os
import cv2
import sys
import json
import numpy as np

from PyQt5 import uic
from PyQt5.QtGui import QKeySequence, QPainter, QImage, QPixmap, QCursor
from PyQt5.QtCore import QBasicTimer, QEvent, QModelIndex, pyqtSignal,  pyqtSlot, Qt, QPoint, QRect, QRectF 
from PyQt5.QtWidgets import  QApplication, QFileDialog, QLabel,  QMainWindow, QMessageBox, QVBoxLayout, qApp

from ui.Main_ui import *
from .myShape import *
from .draw_api import *

OS = sys.platform
if OS == "win32" or OS == "win64":
    SPLITER = "\\"
else:
    SPLITER = "/"
print(f"OS system... {OS}, spliting by {SPLITER}")

class Detection_Label_Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set Value
        self.step         = 0
        self.label        = 1
        self.startPoint   = QPoint()
        self.lastPoint    = QPoint()
        self.mouseOri     = QPoint()
        self.num_frames   = 0
        self.direction    = 0
        self.drawing      = False
        self.onFrame      = False
        self.onBox        = False
        self.onCntrl      = False
        self.box_move     = False
        self.extend_box   = False
        self.save_folder  = None
        self.json_data    = None
        self.boxNum       = -1
        self.timer        = QBasicTimer()
        self.main_layout  = QVBoxLayout()
        self.paint_widget = myQPaint()
        self.moveFactor   = 20
        self.resizeFactor = 2
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
        self.main_ui.EXIT.triggered.connect(self.on_End)

        # Out Button Group
        self.main_ui.out_botton.accepted.connect(self.on_End)
        self.main_ui.out_botton.button(QtWidgets.QDialogButtonBox.Ok).setShortcut("Ctrl+return")
        self.main_ui.out_botton.rejected.connect(self.on_End)
        self.main_ui.out_botton.button(QtWidgets.QDialogButtonBox.Cancel).setShortcut("Alt+F4")

        # Video Setting Group
        self.main_ui.button_set_save_path.clicked.connect(self.on_folderOpen)
        self.main_ui.button_video_path.clicked.connect(self.on_videoOpen)
        self.main_ui.button_split_video.clicked.connect(self.on_split)

        # # Video Controllor Group
        self.main_ui.button_pause.clicked.connect(self.on_Pause)

        # Video Viewer
        self.setMouseTracking(True)
        self.main_ui.centralwidget.setMouseTracking(True)
        self.main_ui.frame_main_video.setMouseTracking(True)
        self.paint_widget.setMouseTracking(True)
        self.paint_widget.main_image.setMouseTracking(True)
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

        # list box clicked event initlaize
        self.main_ui.lst_box_output.clicked.connect(self.click_lst_box)
    
    
    # =====================================================================================================================
    #                                               Qt Button Controller
    # =====================================================================================================================
    @pyqtSlot()
    def on_End(self):
        if self.save_folder and self.json_data:
            self.saveImage()
            self.updateJson()
            self.makeJson()
        qApp.quit()
    
    @pyqtSlot()
    def on_folderOpen(self):
        r"""
        Set Save Path Button Event Handler
        """
        self.save_folder = QFileDialog.getExistingDirectory(self, "Select Directory", os.path.join("."))
        self.main_ui.text_save_path.setText(self.save_folder)
        self.main_ui.text_save_path.setStyleSheet("color:black;")
        self.main_ui.button_set_save_path.clearFocus()

    
    @pyqtSlot()
    def on_videoOpen(self):
        r"""
        Set Video Path Button Event Handler
        """
        self.video_path =  QFileDialog.getOpenFileName(self, "Select Video", filter="*.mp4 *.avi")[0]
        self.main_ui.text_video_path.setText(self.video_path)
        self.main_ui.text_video_path.setStyleSheet("color:black;")
        self.main_ui.button_video_path.clearFocus()
    
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
        self.main_ui.text_FPS.clearFocus()
        self.main_ui.text_class.clearFocus()
        self.main_ui.text_NMS.clearFocus()
        self.main_ui.button_split_video.clearFocus()

    @pyqtSlot()
    def on_Pause(self):
        r"""
        Pause Event Handler
        When Pausing Changing Start Event
        """
        if self.timer.isActive():
            self.timer.stop()
            self.main_ui.button_pause.setText("Start")
            self.main_ui.button_pause.clearFocus()

        else:
            self.timer.start(self.num_frames, self)
            self.main_ui.button_pause.setText("Pause")
            self.main_ui.button_pause.clearFocus()

    @pyqtSlot()        
    def on_Chnage_Label(self):
        r"""
        Change Label When Box Selected
        """
        now_label = self.main_ui.text_label_change.currentIndex()
        self.paint_widget.main_image.rectangles[self.boxNum].mainRect.label = now_label
        self.paint_widget.main_image.rectangles[self.boxNum].mainRect.updateLabel()

        self.main_ui.lst_box_output.setCurrentRow(self.boxNum)      
        sel_items = self.main_ui.lst_box_output.selectedItems()
        for item in sel_items:
            item.setText(CLASS_NAME[now_label])
        self.paint_widget.main_image.update()
    
    @pyqtSlot()
    def on_Box_Delete(self):
        r"""
        Button Controll For Box Delete
        """        

        try:
            self.main_ui.lst_box_output.takeItem(self.boxNum)
            del self.paint_widget.main_image.rectangles[self.boxNum]
            self.onBox = self.paint_widget.main_image.onBox = False
            self.boxNum = self.paint_widget.main_image.index = None
    
            self.paint_widget.main_image.update()
        except:
            QMessageBox.critical(self, "Box Selected Error!", "Please select the box!")
        
        self.main_ui.lst_box_output.clearFocus()
       

         
    @pyqtSlot()
    def video_spliter(self):
        r"""
        Contorl Spliting Event
        """
        # Initialize step
        self.step         = 0

        # Load Video and update info
        self.video        = cv2.VideoCapture(self.video_path)
        self.width_video  = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height_video = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = self.video.get(cv2.CAP_PROP_FPS)
        self.num_frames   = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        # For Save
        names             = self.video_path.split(SPLITER)
        self.saveImgName  = f"{names[-2].split('_')[-1]}_{names[-1].replace('.mp4', '')}" 

        # For Sequence Bar Setting
        self.main_ui.seqBar_main_video.setMaximum(self.num_frames)

        # Initialize Json File
        self.initJson()

        # set Factor
        self.paint_widget.resizes = (self.width_video// self.resizeFactor, self.height_video//self.resizeFactor)
        if self.width_video <= self.height_video:
            self.resizeFactor = self.width_video / self.paint_widget.resizes[0]
        else:
            self.resizeFactor = self.height_video / self.paint_widget.resizes[1]

        print(self.width_video)
        print(self.height_video)
        print(frames_per_second)
        print(self.num_frames)
        print(self.resizeFactor)
  
    def click_lst_box(self):
        r"""
        control lst box clicked
        """
        self.onBox = True
        self.boxNum = int(self.main_ui.lst_box_output.currentIndex().row())
        self.paint_widget.main_image.onBox = self.onBox
        self.paint_widget.main_image.index = self.boxNum
        self.paint_widget.main_image.update()


    def setting_combobox(self):
        # Setting for label setting combobox back ground color
        self.label = self.main_ui.text_label_selected.currentIndex()
        now_color = (CLASS_COLOR[self.label].red(), CLASS_COLOR[self.label].green(), CLASS_COLOR[self.label].blue(), 100)
        now_text_color = (255, 255, 255) if self.label == 0 else (0, 0, 0)
        self.main_ui.text_label_selected.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")
        self.main_ui.text_label_selected.show()
        self.main_ui.text_label_selected.clearFocus()

        # Setting for label setting combobox back ground color
        now_label = self.main_ui.text_label_change.currentIndex()
        now_color = (CLASS_COLOR[now_label].red(), CLASS_COLOR[now_label].green(), CLASS_COLOR[now_label].blue(), 100)
        now_text_color = (255, 255, 255) if now_label == 0 else (0, 0, 0)
        self.main_ui.text_label_change.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")
        self.main_ui.text_label_change.show()
        self.main_ui.text_label_change.clearFocus()
        

    
    #=====================================================================================================================
    #                                            Key and Mouse Evnet Handler
    #=====================================================================================================================
    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)

        if event.key() == Qt.Key_Control:
            self.onCntrl = True

        elif event.key() == Qt.Key_S:
            self.main_ui.button_pause.click()
        
        elif event.key() == Qt.Key_Delete:
            self.main_ui.button_box_delete.click()
        
        elif event.key() == Qt.Key_Left and self.onBox:
            self.paint_widget.main_image.rectangles[self.boxNum].moveBoxes(QPoint(1, 0))
            self.paint_widget.main_image.update()

        elif event.key() == Qt.Key_Right and self.onBox:
            self.paint_widget.main_image.rectangles[self.boxNum].moveBoxes(QPoint(-1, 0))
            self.paint_widget.main_image.update()
            
        elif event.key() == Qt.Key_Up and self.onBox:
            self.paint_widget.main_image.rectangles[self.boxNum].moveBoxes(QPoint(0, 1))
            self.paint_widget.main_image.update()
            
        elif event.key() == Qt.Key_Down and self.onBox:
            self.paint_widget.main_image.rectangles[self.boxNum].moveBoxes(QPoint(0, -1))
            self.paint_widget.main_image.update()
            

    
    def keyReleaseEvent(self, event) -> None:
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Control:
            self.onCntrl = False
      


    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor
        mouseX, mouseY = mousePos.x(), mousePos.y()

        # Combobox setting
        self.setting_combobox()

        # Pressed If On Frame and Clicked Left Button + Cntrl Button - > Drawing Method
        if event.button() == Qt.LeftButton and self.onFrame and self.onCntrl:
            self.drawing = True
            self.original_point = event.pos()
            self.startPoint = self.endPoint = mousePos
        
        if event.button() == Qt.LeftButton and  self.onBox:
            self.mouseOri = mousePos
 
            

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)
        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor
        self.statusbar.showMessage(f"Mouse Pos = ({event.x()}, {event.y()}), global = ({event.globalX()}, {event.globalY()}), local = ({event.localPos().x()}, {event.localPos().y()}), On Frame = {self.onFrame}, Drawing = {self.drawing}, onBox = {self.onBox}")
        

        if mousePos.x() < self.main_ui.frame_main_video.frameGeometry().bottomRight().x() and \
            mousePos.y() <  self.main_ui.frame_main_video.frameGeometry().bottomRight().y():
            self.onFrame = True
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
        else:
            self.onFrame = False
            self.drawing = False
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        if self.drawing and event.buttons and Qt.LeftButton and self.onCntrl:
            self.endPoint =  mousePos
            self.paint_widget.drawing_rect(self.startPoint, self.endPoint, self.label)
            self.update()
            self.paint_widget.main_image.update()
            self.main_layout.update()

        if self.onBox:
            mouseX, mouseY = mousePos.x(), mousePos.y()
            rect = self.paint_widget.main_image.rectangles[self.boxNum]
            
            if self.extend_box:
                rect.extendBoxes(self.mouseOri - mousePos, self.direction)
                self.paint_widget.main_image.update()
                self.mouseOri -= (self.mouseOri - mousePos)

            else:
                if  not rect.checkInBox(mouseX, mouseY):
                    for index, pts in enumerate(rect.rectPts):
                        if pts.checkInBox(mouseX, mouseY, 3):
                            if event.buttons() == Qt.LeftButton and not self.box_move:
                                self.box_move = False
                                self.extend_box = True
                                self.direction = index
                            break
                else:
                    QApplication.setOverrideCursor(QCursor(Qt.SizeAllCursor))
                    if event.buttons() == Qt.LeftButton and not self.extend_box:
                        
                        self.box_move = True
                        self.extend_box = False
                        rect.moveBoxes(self.mouseOri - mousePos)
                        self.paint_widget.main_image.update()
                        self.mouseOri -= (self.mouseOri - mousePos)
                
            
        
    def mouseReleaseEvent(self, event)->None:
        super().mouseReleaseEvent(event)
        
        # Mouse Pose Editor
        mousePos = event.pos() - self.mouseFactor
        mouseX, mouseY = mousePos.x(), mousePos.y()

        # Pressed If On Box and Clicked Left Button -> Box Controll Method
        if event.button() == Qt.LeftButton and self.onFrame  \
           and (not self.drawing) and self.paint_widget.main_image.rectangles:
            mouseX, mouseY = mousePos.x(), mousePos.y()
            for index, rect in enumerate(self.paint_widget.main_image.rectangles):
                if rect.checkInBox(mouseX, mouseY):
                    if self.boxNum != index or self.box_move or self.extend_box:
                        self.onBox = True
                        self.boxNum = index
                    else:
                        self.onBox = True if not self.onBox else False
                        self.boxNum = -1
                        
                    # Main Box Controll Combobox Update
                    now_label = rect.mainRect.label
                    now_color = CLASS_COLORS[now_label]
                    now_text_color = (255, 255, 255) if now_label == 0 else (0, 0, 0)
                    self.main_ui.text_label_change.setCurrentIndex(now_label)
                    self.main_ui.text_label_change.setStyleSheet(f"background-color: rgba{now_color}; color : rgb{now_text_color}")
                    self.main_ui.text_label_change.clearFocus()

                    # Main Image Update
                    self.paint_widget.main_image.onBox = self.onBox
                    self.paint_widget.main_image.index = self.boxNum
                    self.paint_widget.main_image.update()

        # Drawing End If Drawing and Clicked Left Button + Ctrl -> Box Drawing End Method
        if event.button() == Qt.LeftButton and self.drawing and self.onCntrl:
            # Intialize Parameter
            self.drawing = False
            self.endPoint = mousePos
            self.paint_widget.main_image.clear()
            self.paint_widget.main_image.setPixmap(self.paint_widget.pixmap)
            self.paint_widget.setMouseTracking(True)

            # Add Rectangles
            self.paint_widget.main_image.rectangles.append(rectInfo(start_points=self.startPoint, end_points=self.endPoint, label=self.label, ptsSize=6))
            self.main_ui.lst_box_output.addItem(CLASS_NAME[self.label])
            self.paint_widget.main_image.onBox = self.onBox =  True
            self.paint_widget.main_image.index = self.boxNum = len(self.paint_widget.main_image.rectangles) - 1

            # Update Last Drawing
            self.paint_widget.main_image.update()
            self.paint_widget.update()
        
        if self.box_move:
            self.box_move = False
            # self.paint_widget.main_image.rectangles[self.boxNum].mainRect.qBoxpts
        
        if self.extend_box:
            self.extend_box = False
        

            
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
        self.paint_widget.main_image.onBox = self.onBox =  False

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
        
        if self.step:
            # Save Image Update Label
            self.saveImage()
            self.updateJson()
        
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
    def saveImage(self) -> None:
        self.saveImgName += f"_{self.step - 1}.png"
        cv2.imwrite(os.path.join(self.save_folder, "out_dir", "images", self.saveImgName), self.frame)

    def initJson(self) -> None:
        if not os.path.exists(os.path.join(self.save_folder, "out_dir")):
            os.mkdir(os.path.join(self.save_folder, "out_dir"))
            os.mkdir(os.path.join(self.save_folder, "out_dir", "images"))
            os.mkdir(os.path.join(self.save_folder, "out_dir", "annotations"))

            self.json_data = {'info': 'DuckFarm dataset',
                'images': [],
                'licenses':'...',
                'categories' : [{'id': 1, 'name': 'duck'}, {'id': 2, 'name': 'slapped'}, {'id': 3, 'name': 'dead'}],
                'annotations': []
            }
            self.makeJson()

        else:
            with open(os.path.join(self.save_folder, "out_dir", "annotations", "labels.json"), 'r') as json_file:
                self.json_data = json.load(json_file)


    def makeJson(self) -> None:
        with open(os.path.join(self.save_folder, "out_dir", "annotations", "labels.json"), 'w') as json_file:
            json.dump(self.json_data, json_file)
    
    def updateJson(self) -> None:
        self.json_data["images"].append({'id': len(self.json_data["images"]), 'width': self.width_video, 'height': self.height_video, 'file_name': self.saveImgName})
        for rects in self.paint_widget.main_image.rectangles:
            rect = rects.mainRect
            self.json_data["annotations"].append({
                "id": len(self.json_data["annotations"]),
                "image_id": len(self.json_data["images"])  -1,
                'category_id': rect.label,
                'bbox': [rect.x1 * self.resizeFactor, (rect.y1 + self.paint_widget.Factor.y())* self.resizeFactor,
                         rect.x2 * self.resizeFactor, (rect.y2 + self.paint_widget.Factor.y()) * self.resizeFactor],
                'area': (rect.x2 - rect.x1) * (rect.y2 - rect.y1) * self.resizeFactor * self.resizeFactor,
                'iscrowd': 0
            })

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
        

    
        
    