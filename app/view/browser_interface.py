# coding:utf-8
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from qfluentwidgets import SubtitleLabel, PushButton, FluentIcon as FIF, InfoBar, InfoBarPosition, CardWidget, TransparentToolButton, Slider
from app.core.config import OUTPUT_PATH

class BrowserInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("browserInterface")
        self.initUI()
        self.initAudioPlayer()
        
    def initUI(self):
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)
        
        self.headerLayout = QHBoxLayout()
        self.titleLabel = SubtitleLabel(self.tr("音频浏览"), self)
        self.headerLayout.addWidget(self.titleLabel)
        self.headerLayout.addStretch(1)
        
        self.openFolderBtn = PushButton(FIF.FOLDER, self.tr("打开文件夹"), self)
        self.openFolderBtn.clicked.connect(self.openOutputFolder)
        self.headerLayout.addWidget(self.openFolderBtn)
        
        self.refreshBtn = PushButton(FIF.SYNC, self.tr("刷新"), self)
        self.refreshBtn.clicked.connect(self.refreshList)
        self.headerLayout.addWidget(self.refreshBtn)
        
        self.vBoxLayout.addLayout(self.headerLayout)
        
        self.listWidget = QListWidget(self)
        self.listWidget.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                padding: 10px;
                color: black;
            }
            QListWidget::item {
                height: 50px;
                border-radius: 5px;
                padding-left: 10px;
                color: black;
            }
            QListWidget::item:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QListWidget::item:selected {
                background-color: rgba(0, 0, 0, 0.1);
                color: black;
            }
        """)
        self.listWidget.itemDoubleClicked.connect(self.playSelected)
        self.vBoxLayout.addWidget(self.listWidget)
        
        self.playerCard = CardWidget(self)
        self.playerCard.setFixedHeight(80)
        self.playerLayout = QHBoxLayout(self.playerCard)
        self.playerLayout.setContentsMargins(20, 10, 20, 10)
        
        self.currentLabel = QLabel(self.tr("未选择音频"), self)
        self.currentLabel.setStyleSheet("color: black;")
        self.playerLayout.addWidget(self.currentLabel)
        self.playerLayout.addStretch(1)
        
        self.playBtn = TransparentToolButton(FIF.PLAY, self)
        self.playBtn.clicked.connect(self.togglePlay)
        self.playBtn.setIconSize(QSize(32, 32))
        self.playBtn.setEnabled(False)
        self.playerLayout.addWidget(self.playBtn)
        
        self.slider = Slider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        self.slider.sliderPressed.connect(self.onSliderPressed)
        self.slider.sliderReleased.connect(self.onSliderReleased)
        self.playerLayout.addWidget(self.slider, 1)
        
        self.timeLabel = QLabel("00:00 / 00:00", self)
        self.playerLayout.addWidget(self.timeLabel)
        
        # self.playerLayout.addStretch(1) # Removed extra stretch
        
        self.vBoxLayout.addWidget(self.playerCard)
        
        self.refreshList()
    
    def showEvent(self, event):
        self.refreshList()
        super().showEvent(event)

    def initAudioPlayer(self):
        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(100)
        self.player.mediaStatusChanged.connect(self.onMediaStatusChanged)
        self.player.positionChanged.connect(self.onPositionChanged)
        self.player.durationChanged.connect(self.onDurationChanged)
        
    def onPositionChanged(self, position):
        if not self.slider.isSliderDown():
            self.slider.setValue(position)
        self.updateTimeLabel()

    def onDurationChanged(self, duration):
        self.slider.setRange(0, duration)
        self.updateTimeLabel()
    
    def setPosition(self, position):
        self.player.setPosition(position)
        
    def onSliderPressed(self):
        self.player.pause()
        
    def onSliderReleased(self):
        self.player.setPosition(self.slider.value())
        self.player.play()
        self.playBtn.setIcon(FIF.PAUSE)
        
    def updateTimeLabel(self):
        position = self.player.position()
        duration = self.player.duration()
        
        def formatTime(ms):
            seconds = (ms // 1000) % 60
            minutes = (ms // 60000)
            return f"{minutes:02}:{seconds:02}"
            
        self.timeLabel.setText(f"{formatTime(position)} / {formatTime(duration)}")

    def refreshList(self):
        self.listWidget.clear()
        if not os.path.exists(OUTPUT_PATH):
            return
            
        files = [f for f in os.listdir(OUTPUT_PATH) if f.lower().endswith(('.wav', '.mp3', '.flac'))]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_PATH, x)), reverse=True)
        
        for f in files:
            item = QListWidgetItem(f)
            item.setIcon(QIcon(FIF.MUSIC.path()))
            self.listWidget.addItem(item)
            
    def openOutputFolder(self):
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(OUTPUT_PATH)))
        
    def playSelected(self, item):
        filename = item.text()
        filepath = os.path.join(OUTPUT_PATH, filename)
        if os.path.exists(filepath):
            self.player.setSource(QUrl.fromLocalFile(filepath))
            self.player.play()
            self.currentLabel.setText(filename)
            self.playBtn.setIcon(FIF.PAUSE)
            self.playBtn.setEnabled(True)
            
    def togglePlay(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.playBtn.setIcon(FIF.PLAY)
        else:
            self.player.play()
            self.playBtn.setIcon(FIF.PAUSE)
            
    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playBtn.setIcon(FIF.PLAY)
