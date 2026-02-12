# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from qfluentwidgets import SubtitleLabel, BodyLabel, PrimaryPushButton, FluentIcon as FIF
from ..common.resource import get_resource_path
import os

class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")
        self.initUI()

    def initUI(self):
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.setSpacing(20)
        
        self.logoLabel = QLabel(self)
        logoPath = get_resource_path("app/resource/images/Cyrene.png")
        if os.path.exists(logoPath):
            self.logoLabel.setPixmap(QPixmap(logoPath).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.vBoxLayout.addWidget(self.logoLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.titleLabel = SubtitleLabel(self.tr("Qwen TTS GUI"), self)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.welcomeLabel = BodyLabel(self.tr("欢迎使用 Cyrene QwenTTS 语音合成工具"), self)
        self.vBoxLayout.addWidget(self.welcomeLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.startBtn = PrimaryPushButton(FIF.MICROPHONE, self.tr("开始生成"), self)
        self.startBtn.setFixedWidth(200)
        self.startBtn.clicked.connect(self.onStartClicked)
        self.vBoxLayout.addWidget(self.startBtn, 0, Qt.AlignmentFlag.AlignCenter)
        
    def onStartClicked(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, 'switchTo'):
                parent.switchTo(parent.generationInterface)
                break
            parent = parent.parent()
