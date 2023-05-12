from enum import Enum

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QFileDialog

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
        self.videoPath = ''
        self.videoCap = None
        self.isVideoDetect = False
        self.timer = QTimer(self)
        self.center()
        self.bindFunction()
        self.detector = Detector()
        self.helmetIds=set()
        self.headIds = set()
        self.frameCount=0

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2 - 100
        self.move(int(newLeft), int(newTop))

    def bindFunction(self):

        self.imageSelectBtn.clicked.connect(self.getImage)
        self.imageDetectionBtn.clicked.connect(self.detectImage)
        self.videoSelectBtn.clicked.connect(self.getVideo)
        self.videoDetectionBtn.clicked.connect(self.setVideoDetect)
        self.timer.timeout.connect(self.nextFrame)

    def getImage(self):
        imageFile, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                   'E:\Yolo5\Safety_Helmet_Train_dataset\score\images\\test',
                                                   'Image files (*.jpg *.png *.jpeg)')
        if imageFile != '':
            if self.timer.isActive():
                self.timer.stop()
            self.state = State.IMAGE_DETECTION
            scaledImage = QPixmap(imageFile).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio)
            self.showPanel.setPixmap(scaledImage)
            self.imagePath = imageFile
            self.infoPanel.append('open image: {} success'.format(imageFile))
        else:
            self.infoPanel.append('open image: {} error'.format(imageFile))

    def getVideo(self):
        videoFile, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                   'F:\Desktop\\1_20180419110414_rfusd',
                                                   'Video files (*.mp4 *.avi )')
        if videoFile != '':
            self.state = State.VIDEO_DETECTION
            self.videoPath = videoFile
            self.videoCap = cv2.VideoCapture(self.videoPath)
            ret, videoFrame = self.videoCap.read()
            if ret:
                videoFrame = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2RGB)
                videoImg = QImage(videoFrame.data, videoFrame.shape[1], videoFrame.shape[0], videoFrame.shape[1] * 3,
                                  QImage.Format_RGB888)
                self.showPanel.setPixmap(
                    QPixmap.fromImage(videoImg).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
                FPS = self.videoCap.get(cv2.CAP_PROP_FPS)
                self.timer.start(1000 / FPS)
                self.infoPanel.append('open video: {} success'.format(videoFile))
            else:
                self.infoPanel.append('read video: {} error'.format(videoFile))
        else:
            self.infoPanel.append('open video: {} error'.format(videoFile))

    def nextFrame(self):
        if self.state is State.VIDEO_DETECTION:
            if self.videoCap is not None:
                ret, videoFrame = self.videoCap.read()
                if ret:
                    videoFrame = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2RGB)
                    self.frameCount = self.frameCount+1
                    if self.isVideoDetect:
                        result = self.detector.getTrackingResult(videoFrame)
                        headNum = 0
                        helmetNum = 0
                        label = ''
                        for info in result:
                            # print(info)
                            if info[5] == 1:
                                label = 'helmet'
                                self.helmetIds.add(info[4])
                                helmetNum = helmetNum + 1
                            elif info[5] == 0:
                                label = 'head'
                                headNum = headNum + 1
                                self.headIds.add(info[4])
                            cv2.rectangle(videoFrame, (int(info[0]), int(info[1])), (int(info[2]), int(info[3])),
                                          (255 * (1 - info[5]), 255 * info[5], 0), thickness=1)
                            cv2.putText(videoFrame, label + '#' + str(int(info[4])), (int(info[0]), int(info[1])),
                                        cv2.FONT_HERSHEY_PLAIN,
                                        1.2, (255, 0, 0), 1)

                            self.infoPanel.setText('Helmet Count: ' + str(helmetNum) +'\n'+ 'Head Count:' + str(headNum))


                        # videoFrame = np.squeeze(result.render())
                    videoImg = QImage(videoFrame.data, videoFrame.shape[1], videoFrame.shape[0],
                                      videoFrame.shape[1] * 3, QImage.Format_RGB888)
                    self.showPanel.setPixmap(
                        QPixmap.fromImage(videoImg).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
                else:
                    self.timer.stop()
                    self.infoPanel.append('play video: {} done'.format(self.videoPath))
                    self.infoPanel.append('Total Helmet: {}\nTotal Head:{}\nTotal Object:{}'.format(len(self.helmetIds),len(self.headIds),len(self.helmetIds)+len(self.headIds)))
                    self.detector.tracker.clear()
                    self.frameCount=0

    def detectImage(self):
        if self.state is State.IMAGE_DETECTION:
            result = self.detector.getInferResultFromPath(self.imagePath)
            img = np.squeeze(result.render())
            show_image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.showPanel.setPixmap(
                QPixmap.fromImage(show_image).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
            self.infoPanel.append(str(result))

    def setVideoDetect(self):
        if self.state is State.VIDEO_DETECTION:
            self.isVideoDetect = not self.isVideoDetect
