import numpy as np
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QDesktopWidget, QLabel, QFileDialog
from enum import Enum
import GUIForm
from Detector import Detector


class State(Enum):
    INIT = 0
    IMAGE_DETECTION = 1
    VIDEO_DETECTION = 2
    REAL_TIME_DETECTION = 3


class GUI(QWidget, GUIForm.Ui_HelmetDetection):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('安全帽检测')
        self.state = State.INIT
        self.imagePath = ''
        self.center()
        self.bindFunction()
        self.detector = Detector()

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2 - 100
        self.move(int(newLeft), int(newTop))

    def setPosition(self):
        self.showPanel.resize(800, 600)

    def bindFunction(self):

        self.imageSelectBtn.clicked.connect(self.getImage)
        self.imageDetectionBtn.clicked.connect(self.detectImage)

    def getImage(self):
        imageFile, _ = QFileDialog.getOpenFileName(self, 'Open file', 'E:\Yolo5\Safety_Helmet_Train_dataset\score\images\\test', 'Image files (*.jpg *.png *.jpeg)')
        if imageFile != '':
            self.state = State.IMAGE_DETECTION
            scaledImage = QPixmap(imageFile).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio)
            self.showPanel.setPixmap(scaledImage)
            self.imagePath = imageFile
            self.infoPanel.append('open image: {} success'.format(imageFile))
        else:
            self.infoPanel.append('open image: {} error'.format(imageFile))

    def detectImage(self):
        if self.state is State.IMAGE_DETECTION:
            result = self.detector.getInferResult(self.imagePath)
            img = np.squeeze(result.render())
            show_image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.showPanel.setPixmap(QPixmap.fromImage(show_image).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
            self.infoPanel.append(str(result))
