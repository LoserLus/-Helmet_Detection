# from PyQt5.QtCore import QUrl, Qt
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtMultimedia import *
# from PyQt5.QtMultimediaWidgets import QVideoWidget
# from PyQt5.QtWidgets import QVBoxLayout, QSlider, QPushButton, QHBoxLayout, QWidget
# from PyQt5.QtWidgets import QApplication, QWidget
# import sys
# class My_widget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.player = QMediaPlayer()
#         self.videowidget = QVideoWidget()  # 定义视频显示的widget
#         self.resize(700, 700)
#         self.layout = QVBoxLayout()
#         self.h_layout = QHBoxLayout()
#         self.layout.addWidget(self.videowidget)
#         self.btn_start = QPushButton()
#         self.btn_start.setText("开始")
#         self.btn_stop = QPushButton()
#         self.btn_stop.setText("暂停")
#         self.Slider = QSlider(Qt.Horizontal, self)
#         self.Slider.setRange(0, 100)
#         self.Slider.show()
#         self.layout.addWidget(self.btn_start)
#         self.layout.addWidget(self.btn_stop)
#         self.layout.addWidget(self.Slider)
#         self.player.durationChanged.connect(self.print_data)
#         self.btn_stop.clicked.connect(self.play_pause)
#         self.btn_start.clicked.connect(self.play_start)
#         self.Slider.valueChanged.connect(self.slider_change)
#         self.player.positionChanged.connect(self.player_change)
#         self.setLayout(self.layout)
#     def show_video(self):
#         self.show()
#         self.player.setVideoOutput(self.videowidget)  # 视频播放输出的widget，就是上面定义的
#         self.videopath = "F:\Desktop\\1_20180419110414_rfusd\测试视频1.mp4"
#         frame =QMediaContent(QUrl.fromLocalFile(self.videopath))
#         frame = QMediaContent(frame)
#         self.player.setMedia(frame)  # 选取视频文件
#         self.player.play()  # 播放视频
#         self.btn_start.setEnabled(False)
#
#     def print_data(self):
#         self.Slider.setRange(0, self.player.duration())
#
#     def player_change(self):
#         self.Slider.setValue(int(self.Slider.value()))
#
#     def slider_change(self):
#         self.player.setPosition(float(self.Slider.value()))
#
#     def play_pause(self):
#         self.player.pause()
#         self.btn_start.setEnabled(True)
#
#     def play_start(self):
#         self.btn_start.setEnabled(False)
#         self.player.play()
#         self.btn_stop.setEnabled(True)
#
#     def closeEvent(self,event):
#         self.play_pause()
#
# app = QApplication(sys.argv)
# window = My_widget()
# window.show_video()
# sys.exit(app.exec_())
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget
# 创建应用程序和主窗口
# app = QApplication([])
# window = QWidget()
#
# # 创建标签和视频控件
# label = QLabel()
# video_widget = QVideoWidget()
#
# # 将标签和视频控件添加到水平布局中
# layout = QHBoxLayout(window)
# layout.addWidget(label)
# layout.addWidget(video_widget)
#
# # 设置布局参数
# layout.setAlignment(Qt.AlignCenter)
# layout.setContentsMargins(0, 0, 0, 0)
#
# # 显示窗口
# window.show()
#
# # 运行应用程序
# app.exec_()
from Detector import Detector
import cv2

detect = Detector()
imgPath = 'D:\BaiduNetdiskDownload\VOC2028\VOC2028\JPEGImages\\000032.jpg'
image = cv2.imread(imgPath)
det, track = detect.getTrackingResult(image)
print(det)
print('***************************')
print(track)
for info in track:
    print(info)
    cv2.rectangle(image, (int(info[0]), int(info[1])), (int(info[2]), int(info[3])), (255, 0, 0), thickness=1)
    cv2.putText(image, '#' + str(info[4]), (int(info[0]), int(info[1])), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)
cv2.namedWindow("Hello", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Hello", image)
cv2.waitKey(0)

