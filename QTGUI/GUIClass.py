import os
from datetime import datetime
from enum import IntEnum

import cv2
import numpy as np
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtWidgets import QDesktopWidget, QFileDialog, QMainWindow

import DetectionGUIForm
from Database import Database
from Detector import Detector
from ORMClass import VideoClass, DataClass
from QTGUI.TableClass import TableGUI


class State(IntEnum):
    INIT = 0
    IMAGE_DETECTION = 1
    VIDEO_DETECTION = 2
    REAL_TIME_DETECTION = 3


class GUI(QMainWindow, DetectionGUIForm.Ui_DetectionWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('安全帽检测')
        self.imagePath = ''
        self.videoPath = ''
        self.musicPath = './src/Beep.mp3'
        self.videoCap = None
        self.isVideoDetect = False
        self.isRealTimeDetect = False
        self.isMusicPlay = False
        self.timer = QTimer(self)
        self.center()
        self.bindFunction()
        self.detector = Detector()
        self.database = Database()
        self.tableWindow = None
        self.helmetIds = set()
        self.headIds = set()
        self.currentVideo = None
        self.frameList = []
        self.stateList = ['初始化', '图像检测', '视频检测', '实时检测']
        self.state = None
        self.stateChangeTo(State.INIT)
        self.music = QMediaContent(QUrl.fromLocalFile(os.path.abspath('./src/Beep.mp3')))
        self.player = QtMultimedia.QMediaPlayer(self)
        self.player.setMedia(self.music)
        self.player.setVolume(50.0)

    def openTableWindow(self):
        if self.tableWindow is None:
            self.tableWindow = TableGUI(self.database)
        self.tableWindow.setData()
        self.tableWindow.show()

    def center(self):  # 定义一个函数使得窗口居中显示
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2 - 100
        self.move(int(newLeft), int(newTop))

    def MOTInit(self):
        self.detector.tracker.clear()
        self.headIds.clear()
        self.helmetIds.clear()

    def stateChangeTo(self, newState):
        if newState is State.IMAGE_DETECTION:
            if self.state in [State.VIDEO_DETECTION, State.REAL_TIME_DETECTION]:
                if self.timer.isActive():
                    self.timer.stop()
                self.MOTInit()
        elif newState is State.VIDEO_DETECTION:
            self.MOTInit()
        elif newState is State.REAL_TIME_DETECTION:
            if self.state is State.VIDEO_DETECTION:
                if self.timer.isActive():
                    self.timer.stop()
            self.MOTInit()

        self.state = newState
        self.updateState()

    def bindFunction(self):

        self.importPicAction.triggered.connect(self.getImage)
        self.importVideoAction.triggered.connect(self.getVideo)
        self.videoDetectAction.toggled[bool].connect(self.setVideoDetect)
        self.imageDetectAction.triggered.connect(self.detectImage)
        self.openCameraAction.triggered.connect(self.getCamera)
        self.openAlertAction.toggled[bool].connect(self.setMusicPlay)
        self.exportDataAction.triggered.connect(self.openTableWindow)
        self.timer.timeout.connect(self.nextFrame)

    def getCamera(self):
        if not self.isRealTimeDetect:
            self.stateChangeTo(State.REAL_TIME_DETECTION)
            self.videoCap = cv2.VideoCapture(0)
            self.videoCap.set(cv2.CAP_PROP_FPS, 30)
            ret, videoFrame = self.videoCap.read()
            if ret:
                self.isRealTimeDetect = True
                videoFrame = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2RGB)
                videoImg = QImage(videoFrame.data, videoFrame.shape[1], videoFrame.shape[0], videoFrame.shape[1] * 3,
                                  QImage.Format_RGB888)
                self.showPanel.setPixmap(
                    QPixmap.fromImage(videoImg).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
            self.timer.start(1000 / 30)
            self.infoPanel.setText('open camera success')
            self.currentVideo = VideoClass(name='real_time', time=datetime.now().strftime("%Y-%m-%d%H:%M:%S"))
            self.currentVideo.id = self.database.insertResult(self.currentVideo)
        else:
            if self.videoCap is not None:
                self.isRealTimeDetect = False
                self.videoCap.release()

    def getImage(self):
        imageFile, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                   'E:\Yolo5\Safety_Helmet_Train_dataset\score\images\\test',
                                                   'Image files (*.jpg *.png *.jpeg)')
        if imageFile != '':
            self.stateChangeTo(State.IMAGE_DETECTION)
            scaledImage = QPixmap(imageFile).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio)
            self.showPanel.setPixmap(scaledImage)
            self.imagePath = imageFile
            self.infoPanel.setText('open image: {} success'.format(imageFile))
        else:
            self.infoPanel.setText('open image: {} error'.format(imageFile))

    def getVideo(self):
        videoFile, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                   'F:\Desktop\\1_20180419110414_rfusd',
                                                   'Video files (*.mp4 *.avi )')
        if videoFile != '':
            self.stateChangeTo(State.VIDEO_DETECTION)
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
                self.infoPanel.setText('open video: {} success'.format(videoFile))
                self.currentVideo = VideoClass(name=self.videoPath, time=datetime.now().strftime("%Y-%m-%d%H:%M:%S"))
                self.currentVideo.id = self.database.insertResult(self.currentVideo)
            else:
                self.infoPanel.setText('read video: {} error'.format(videoFile))
        else:
            self.infoPanel.setText('open video: {} error'.format(videoFile))

    def nextFrame(self):
        if self.state in [State.VIDEO_DETECTION, State.REAL_TIME_DETECTION]:
            if self.videoCap is not None:
                ret, videoFrame = self.videoCap.read()
                if ret:
                    videoFrame = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2RGB)
                    headNum = 0
                    helmetNum = 0
                    label = ''
                    if self.isVideoDetect:
                        result = self.detector.getTrackingResult(videoFrame)
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
                            # videoFrame=Image.fromarray(videoFrame)
                            # # print(type(temp))
                            # # print(type(videoFrame))
                            # draw = ImageDraw.Draw(videoFrame,mode='RGB')
                            # draw.rectangle(xy=[(info[0], info[1]), (info[2], info[3])],
                            #                outline=(int(255 * (1 - info[5])), int(255 * info[5]), 0), width=1)
                            # draw.text(xy=(info[0], info[1]),
                            #           text=label + '#' + str(int(info[4])), fill=(255, 0, 0))
                            # videoFrame = numpy.asarray(videoFrame)
                            cv2.rectangle(videoFrame, (int(info[0]), int(info[1])), (int(info[2]), int(info[3])),
                                          (255 * (1 - info[5]), 255 * info[5], 0), thickness=2)
                            cv2.putText(videoFrame, label + '#' + str(int(info[4])), (int(info[0]), int(info[1])),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        fontScale=0.75, color=(255, 0, 0),  thickness=2)

                            self.infoPanel.setText(
                                'Helmet Count: ' + str(helmetNum) + '\n' + 'Head Count:' + str(headNum))

                        # videoFrame = np.squeeze(result.render())
                    videoImg = QImage(videoFrame.data, videoFrame.shape[1], videoFrame.shape[0],
                                      videoFrame.shape[1] * 3, QImage.Format_RGB888)
                    self.showPanel.setPixmap(
                        QPixmap.fromImage(videoImg).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
                    if headNum > 0:
                        if self.state is State.VIDEO_DETECTION:
                            dtime = self.videoCap.get(cv2.CAP_PROP_POS_MSEC)
                            dtime = datetime.utcfromtimestamp(dtime / 1000.0).time().strftime("%H:%M:%S.%f")[0:-3]
                        else:
                            dtime = datetime.now()
                        if len(self.frameList) > 1000:
                            self.database.insertData(self.frameList)
                            self.frameList.clear()
                        self.frameList.append(
                            DataClass(vid=self.currentVideo.id, time=dtime, helmet=helmetNum, head=headNum,
                                      total=headNum + helmetNum))
                        if self.isMusicPlay:
                            # playsound(self.musicPath,block=False)
                            self.player.play()
                else:
                    self.timer.stop()
                    if self.state is State.VIDEO_DETECTION:
                        self.infoPanel.append('play video: {} done'.format(self.videoPath))
                    else:
                        self.infoPanel.append('real time video done')
                    if self.isVideoDetect:
                        self.infoPanel.append(
                            'Total Helmet: {}\nTotal Head:{}\nTotal Object:{}'.format(len(self.helmetIds),
                                                                                      len(self.headIds),
                                                                                      len(self.helmetIds) + len(
                                                                                          self.headIds)))
                        if len(self.frameList) > 0:
                            self.database.insertData(self.frameList)
                            self.frameList.clear()
                        self.currentVideo.helmet = len(self.helmetIds)
                        self.currentVideo.head = len(self.headIds)
                        self.currentVideo.total = self.currentVideo.head + self.currentVideo.helmet
                        self.database.updateResultCount(self.currentVideo)
                        self.infoPanel.append(
                            self.currentVideo.name + ' detection result saved to database successfully')

    def detectImage(self):
        if self.state is State.IMAGE_DETECTION:
            result = self.detector.getInferResultFromPath(self.imagePath)
            result.names[0] = 'head'
            img = np.squeeze(result.render())
            show_image = QImage(img.data, img.shape[1], img.shape[0], img.shape[1] * 3, QImage.Format_RGB888)
            self.showPanel.setPixmap(
                QPixmap.fromImage(show_image).scaled(self.showPanel.size(), QtCore.Qt.KeepAspectRatio))
            info = result.xyxy[0].cpu().numpy()
            helmet = 0
            for i in info:
                helmet = helmet + int(i[5])
            self.infoPanel.append(str(result))
            self.database.insert(self.imagePath, helmet, len(info) - helmet)
            self.infoPanel.append('image detection result saved to database successfully')

    def updateState(self):
        state1 = '系统状态: ' + self.stateList[int(self.state)] + '\t'
        temp = '开启' if self.isVideoDetect else '关闭'
        state2 = '安全帽检测状态:' + temp + '\t'
        temp = '开启' if self.isMusicPlay else '关闭'
        state3 = '警报状态:' + temp + '\t'
        state = state1 + state2 + state3
        if self.state is State.REAL_TIME_DETECTION:
            temp = '开启' if self.isRealTimeDetect else '关闭'
            state4 = '实时检测状态:' + temp + '\t'
            state = state + state4
        self.statusbar.showMessage(state)

    def setVideoDetect(self):
        if self.state in [State.VIDEO_DETECTION, State.REAL_TIME_DETECTION]:
            if self.videoDetectAction.isChecked():
                self.isVideoDetect = True
            else:
                self.isVideoDetect = False
            self.updateState()
            # if self.state is State.REAL_TIME_DETECTION and self

    def setMusicPlay(self):
        if self.state in [State.VIDEO_DETECTION, State.REAL_TIME_DETECTION]:
            if self.openAlertAction.isChecked():
                self.isMusicPlay = True
            else:
                self.isMusicPlay = False
            self.updateState()

    def exportData(self):
        self.database.query2Excel('result')
        self.infoPanel.append('Data saved successfully')
