# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\detectionWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DetectionWindow(object):
    def setupUi(self, DetectionWindow):
        DetectionWindow.setObjectName("DetectionWindow")
        DetectionWindow.resize(1013, 776)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/system.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DetectionWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(DetectionWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.showPanel = QtWidgets.QLabel(self.centralwidget)
        self.showPanel.setLineWidth(0)
        self.showPanel.setText("")
        self.showPanel.setPixmap(QtGui.QPixmap(".\\src/Camera.png"))
        self.showPanel.setAlignment(QtCore.Qt.AlignCenter)
        self.showPanel.setObjectName("showPanel")
        self.verticalLayout_3.addWidget(self.showPanel)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.VLine = QtWidgets.QFrame(self.centralwidget)
        self.VLine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.VLine.setLineWidth(3)
        self.VLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.VLine.setObjectName("VLine")
        self.verticalLayout_2.addWidget(self.VLine)
        self.infoPanel = QtWidgets.QTextBrowser(self.centralwidget)
        self.infoPanel.setObjectName("infoPanel")
        self.verticalLayout_2.addWidget(self.infoPanel)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.setStretch(0, 8)
        self.verticalLayout_3.setStretch(1, 2)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        DetectionWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DetectionWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        DetectionWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DetectionWindow)
        self.statusbar.setObjectName("statusbar")
        DetectionWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(DetectionWindow)
        self.toolBar.setObjectName("toolBar")
        DetectionWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.importPicAction = QtWidgets.QAction(DetectionWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/pic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.importPicAction.setIcon(icon1)
        self.importPicAction.setObjectName("importPicAction")
        self.importVideoAction = QtWidgets.QAction(DetectionWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.importVideoAction.setIcon(icon2)
        self.importVideoAction.setObjectName("importVideoAction")
        self.exportDataAction = QtWidgets.QAction(DetectionWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/export.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportDataAction.setIcon(icon3)
        self.exportDataAction.setObjectName("exportDataAction")
        self.openAlertAction = QtWidgets.QAction(DetectionWindow)
        self.openAlertAction.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/ring.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openAlertAction.setIcon(icon4)
        self.openAlertAction.setObjectName("openAlertAction")
        self.openCameraAction = QtWidgets.QAction(DetectionWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/Camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openCameraAction.setIcon(icon5)
        self.openCameraAction.setObjectName("openCameraAction")
        self.videoDetectAction = QtWidgets.QAction(DetectionWindow)
        self.videoDetectAction.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/videoDetect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.videoDetectAction.setIcon(icon6)
        self.videoDetectAction.setObjectName("videoDetectAction")
        self.showInfoAction = QtWidgets.QAction(DetectionWindow)
        self.showInfoAction.setObjectName("showInfoAction")
        self.imageDetectAction = QtWidgets.QAction(DetectionWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/picDetect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.imageDetectAction.setIcon(icon7)
        self.imageDetectAction.setObjectName("imageDetectAction")
        self.menu.addAction(self.importPicAction)
        self.menu.addAction(self.importVideoAction)
        self.menu.addAction(self.openCameraAction)
        self.menu_2.addAction(self.exportDataAction)
        self.menu_2.addAction(self.openAlertAction)
        self.menu_2.addAction(self.videoDetectAction)
        self.menu_2.addAction(self.imageDetectAction)
        self.menu_3.addAction(self.showInfoAction)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.toolBar.addAction(self.importPicAction)
        self.toolBar.addAction(self.importVideoAction)
        self.toolBar.addAction(self.openCameraAction)
        self.toolBar.addAction(self.imageDetectAction)
        self.toolBar.addAction(self.videoDetectAction)
        self.toolBar.addAction(self.openAlertAction)
        self.toolBar.addAction(self.exportDataAction)

        self.retranslateUi(DetectionWindow)
        QtCore.QMetaObject.connectSlotsByName(DetectionWindow)

    def retranslateUi(self, DetectionWindow):
        _translate = QtCore.QCoreApplication.translate
        DetectionWindow.setWindowTitle(_translate("DetectionWindow", "MainWindow"))
        self.menu.setTitle(_translate("DetectionWindow", "文件"))
        self.menu_2.setTitle(_translate("DetectionWindow", "功能"))
        self.menu_3.setTitle(_translate("DetectionWindow", "关于"))
        self.toolBar.setWindowTitle(_translate("DetectionWindow", "toolBar"))
        self.importPicAction.setText(_translate("DetectionWindow", "导入图片"))
        self.importVideoAction.setText(_translate("DetectionWindow", "导入视频"))
        self.exportDataAction.setText(_translate("DetectionWindow", "导出结果"))
        self.openAlertAction.setText(_translate("DetectionWindow", "检测警报"))
        self.openCameraAction.setText(_translate("DetectionWindow", "实时输入"))
        self.videoDetectAction.setText(_translate("DetectionWindow", "视频检测"))
        self.videoDetectAction.setToolTip(_translate("DetectionWindow", "视频检测"))
        self.showInfoAction.setText(_translate("DetectionWindow", "系统介绍"))
        self.imageDetectAction.setText(_translate("DetectionWindow", "图像检测"))
from src import icons_rc
