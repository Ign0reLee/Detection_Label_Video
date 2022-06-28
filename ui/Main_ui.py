# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Detection Auto Labeling with Detectron!")
        MainWindow.resize(1080, 960)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Group_Output_Viewer = QtWidgets.QScrollArea(self.centralwidget)
        self.Group_Output_Viewer.setGeometry(QtCore.QRect(10, 680, 160, 190))
        self.Group_Output_Viewer.setWidgetResizable(True)
        self.Group_Output_Viewer.setObjectName("Group_Output_Viewer")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 158, 188))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scr_bar_output = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_3)
        self.scr_bar_output.setGeometry(QtCore.QRect(145, 0, 15, 190))
        self.scr_bar_output.setOrientation(QtCore.Qt.Vertical)
        self.scr_bar_output.setObjectName("scr_bar_output")
        self.lst_box_output = QtWidgets.QListWidget(self.scrollAreaWidgetContents_3)
        self.lst_box_output.setGeometry(QtCore.QRect(0, 0, 145, 190))
        self.lst_box_output.setObjectName("lst_box_output")
        self.Group_Output_Viewer.setWidget(self.scrollAreaWidgetContents_3)
        self.Group_Main_Video_Viewer = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Main_Video_Viewer.setGeometry(QtCore.QRect(10, 0, 1060, 500))
        self.Group_Main_Video_Viewer.setMouseTracking(True)
        self.Group_Main_Video_Viewer.setObjectName("Group_Main_Video_Viewer")
        self.seqBar_main_video = QtWidgets.QProgressBar(self.Group_Main_Video_Viewer)
        self.seqBar_main_video.setGeometry(QtCore.QRect(0, 475, 1060, 23))
        self.seqBar_main_video.setProperty("value", 0)
        self.seqBar_main_video.setObjectName("seqBar_main_video")
        self.frame_main_video = QtWidgets.QFrame(self.Group_Main_Video_Viewer)
        self.frame_main_video.setGeometry(QtCore.QRect(0, 20, 1060, 450))
        self.frame_main_video.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main_video.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main_video.setObjectName("frame_main_video")
        self.button_back_ten = QtWidgets.QPushButton(self.centralwidget)
        self.button_back_ten.setGeometry(QtCore.QRect(410, 830, 80, 80))
        self.button_back_ten.setObjectName("button_back_ten")
        self.Group_Box_Controll = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Box_Controll.setGeometry(QtCore.QRect(430, 510, 320, 150))
        self.Group_Box_Controll.setMouseTracking(True)
        self.Group_Box_Controll.setObjectName("Group_Box_Controll")
        self.button_box_delete = QtWidgets.QPushButton(self.Group_Box_Controll)
        self.button_box_delete.setGeometry(QtCore.QRect(265, 100, 50, 40))
        self.button_box_delete.setObjectName("button_box_delete")
        self.text_label_change = QtWidgets.QComboBox(self.Group_Box_Controll)
        self.text_label_change.setGeometry(QtCore.QRect(10, 45, 250, 30))
        self.text_label_change.setObjectName("text_label_change")
        self.button_label_change = QtWidgets.QPushButton(self.Group_Box_Controll)
        self.button_label_change.setGeometry(QtCore.QRect(265, 40, 50, 40))
        self.button_label_change.setObjectName("button_label_change")
        self.tag_label_change = QtWidgets.QLabel(self.Group_Box_Controll)
        self.tag_label_change.setGeometry(QtCore.QRect(10, 25, 80, 20))
        self.tag_label_change.setLineWidth(11)
        self.tag_label_change.setObjectName("tag_label_change")
        self.button_front_30 = QtWidgets.QPushButton(self.centralwidget)
        self.button_front_30.setGeometry(QtCore.QRect(590, 830, 80, 80))
        self.button_front_30.setObjectName("button_front_30")
        self.out_botton = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.out_botton.setGeometry(QtCore.QRect(660, 870, 400, 50))
        self.out_botton.setOrientation(QtCore.Qt.Horizontal)
        self.out_botton.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.out_botton.setObjectName("out_botton")
        self.button_pause = QtWidgets.QPushButton(self.centralwidget)
        self.button_pause.setGeometry(QtCore.QRect(500, 830, 80, 80))
        self.button_pause.setObjectName("button_pause")
        self.Group_File_Setting = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_File_Setting.setGeometry(QtCore.QRect(10, 510, 400, 150))
        self.Group_File_Setting.setObjectName("Group_File_Setting")
        self.button_video_path = QtWidgets.QPushButton(self.Group_File_Setting)
        self.button_video_path.setGeometry(QtCore.QRect(10, 25, 50, 40))
        self.button_video_path.setObjectName("button_video_path")
        self.text_video_path = QtWidgets.QTextEdit(self.Group_File_Setting)
        self.text_video_path.setEnabled(False)
        self.text_video_path.setGeometry(QtCore.QRect(70, 25, 320, 40))
        self.text_video_path.setObjectName("text_video_path")
        self.tag_FPS_3 = QtWidgets.QLabel(self.Group_File_Setting)
        self.tag_FPS_3.setGeometry(QtCore.QRect(70, 80, 40, 15))
        self.tag_FPS_3.setObjectName("tag_FPS_3")
        self.text_FPS = QtWidgets.QTextEdit(self.Group_File_Setting)
        self.text_FPS.setGeometry(QtCore.QRect(10, 70, 50, 30))
        self.text_FPS.setObjectName("text_FPS")
        self.text_NMS = QtWidgets.QTextEdit(self.Group_File_Setting)
        self.text_NMS.setGeometry(QtCore.QRect(100, 70, 50, 30))
        self.text_NMS.setObjectName("text_NMS")
        self.tag_NMS_3 = QtWidgets.QLabel(self.Group_File_Setting)
        self.tag_NMS_3.setGeometry(QtCore.QRect(160, 80, 40, 15))
        self.tag_NMS_3.setObjectName("tag_NMS_3")
        self.tag_class_3 = QtWidgets.QLabel(self.Group_File_Setting)
        self.tag_class_3.setGeometry(QtCore.QRect(250, 80, 40, 15))
        self.tag_class_3.setObjectName("tag_class_3")
        self.text_class = QtWidgets.QTextEdit(self.Group_File_Setting)
        self.text_class.setGeometry(QtCore.QRect(190, 70, 50, 30))
        self.text_class.setObjectName("text_class")
        self.button_split_video = QtWidgets.QPushButton(self.Group_File_Setting)
        self.button_split_video.setGeometry(QtCore.QRect(300, 70, 90, 30))
        self.button_split_video.setObjectName("button_split_video")
        self.text_save_path = QtWidgets.QTextEdit(self.Group_File_Setting)
        self.text_save_path.setEnabled(False)
        self.text_save_path.setGeometry(QtCore.QRect(70, 105, 320, 40))
        self.text_save_path.setObjectName("text_save_path")
        self.button_set_save_path = QtWidgets.QPushButton(self.Group_File_Setting)
        self.button_set_save_path.setGeometry(QtCore.QRect(10, 105, 50, 40))
        self.button_set_save_path.setObjectName("button_set_save_path")
        self.Group_Label_Setting = QtWidgets.QGroupBox(self.centralwidget)
        self.Group_Label_Setting.setGeometry(QtCore.QRect(780, 510, 300, 150))
        self.Group_Label_Setting.setMouseTracking(True)
        self.Group_Label_Setting.setObjectName("Group_Label_Setting")
        self.text_label_selected = QtWidgets.QComboBox(self.Group_Label_Setting)
        self.text_label_selected.setGeometry(QtCore.QRect(20, 45, 250, 30))
        self.text_label_selected.setObjectName("text_label_selected")
        self.button_label_add = QtWidgets.QPushButton(self.Group_Label_Setting)
        self.button_label_add.setGeometry(QtCore.QRect(197, 80, 70, 70))
        self.button_label_add.setObjectName("button_label_add")
        self.text_label_names = QtWidgets.QTextEdit(self.Group_Label_Setting)
        self.text_label_names.setGeometry(QtCore.QRect(90, 115, 100, 30))
        self.text_label_names.setObjectName("text_label_names")
        self.tag_label_colored = QtWidgets.QLabel(self.Group_Label_Setting)
        self.tag_label_colored.setGeometry(QtCore.QRect(10, 80, 80, 30))
        self.tag_label_colored.setAlignment(QtCore.Qt.AlignCenter)
        self.tag_label_colored.setObjectName("tag_label_colored")
        self.tag_label_names = QtWidgets.QLabel(self.Group_Label_Setting)
        self.tag_label_names.setGeometry(QtCore.QRect(20, 120, 80, 15))
        self.tag_label_names.setObjectName("tag_label_names")
        self.tag_label_selected = QtWidgets.QLabel(self.Group_Label_Setting)
        self.tag_label_selected.setGeometry(QtCore.QRect(20, 25, 80, 20))
        self.tag_label_selected.setLineWidth(11)
        self.tag_label_selected.setObjectName("tag_label_selected")
        self.text_label_color = QtWidgets.QTextEdit(self.Group_Label_Setting)
        self.text_label_color.setGeometry(QtCore.QRect(90, 80, 100, 30))
        self.text_label_color.setObjectName("text_label_color")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 20))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.EXIT = QtWidgets.QAction(MainWindow)
        self.EXIT.setObjectName("EXIT")
        self.menufile.addAction(self.EXIT)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Group_Main_Video_Viewer.setTitle(_translate("MainWindow", "Main Video"))
        self.button_back_ten.setText(_translate("MainWindow", "-10s"))
        self.Group_Box_Controll.setTitle(_translate("MainWindow", "Box Control   "))
        self.button_box_delete.setText(_translate("MainWindow", "Delete\n"
"Box"))
        self.button_label_change.setText(_translate("MainWindow", "Change\n"
"Label"))
        self.tag_label_change.setText(_translate("MainWindow", "Now Label"))
        self.button_front_30.setText(_translate("MainWindow", "30s"))
        self.button_pause.setText(_translate("MainWindow", "Start"))
        self.Group_File_Setting.setTitle(_translate("MainWindow", "Video Setting"))
        self.button_video_path.setText(_translate("MainWindow", "open\n"
"video"))
        self.tag_FPS_3.setText(_translate("MainWindow", "FPS"))
        self.text_FPS.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">None</p></body></html>"))
        self.text_NMS.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.5</p></body></html>"))
        self.tag_NMS_3.setText(_translate("MainWindow", "NMS"))
        self.tag_class_3.setText(_translate("MainWindow", "Classes"))
        self.text_class.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3</p></body></html>"))
        self.button_split_video.setText(_translate("MainWindow", "split"))
        self.button_set_save_path.setText(_translate("MainWindow", "save \n"
"path"))
        self.Group_Label_Setting.setTitle(_translate("MainWindow", "Label Setting"))
        self.button_label_add.setText(_translate("MainWindow", "Add \n"
"Label"))
        self.tag_label_colored.setText(_translate("MainWindow", "Label Color \n"
" (R,G,B)"))
        self.tag_label_names.setText(_translate("MainWindow", "Label Name"))
        self.tag_label_selected.setText(_translate("MainWindow", "Selected Label"))
        self.text_label_color.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">255, 0, 0</p></body></html>"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.EXIT.setText(_translate("MainWindow", "끝내기"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
