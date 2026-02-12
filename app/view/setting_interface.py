# coding:utf-8
from PySide6.QtCore import Qt, Signal, QProcess
from PySide6.QtWidgets import QWidget, QLabel, QPushButton as PushButton
from qfluentwidgets import (SettingCardGroup, ComboBoxSettingCard, FluentIcon as FIF, 
                            InfoBar, ScrollArea, ExpandLayout, Theme, setTheme, InfoBarPosition)
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
import sys
import os

from ..common.config import cfg, Language


class SettingInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.setObjectName("settingInterface")
        self.scrollWidget.setObjectName("scrollWidget")

        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('个性化'), self.scrollWidget)

        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('语言'),
            self.tr('设置界面语言'),
            texts=['简体中文', 'English'],
            parent=self.personalGroup
        )
        
        # Add Restart Button to language card
        self.restartBtn = PushButton(self.tr('关闭程序'), self.languageCard)
        self.restartBtn.clicked.connect(self.closeApp)
        self.restartBtn.hide() # Initially hidden
        self.languageCard.hBoxLayout.addWidget(self.restartBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.languageCard.hBoxLayout.addSpacing(16)

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.scrollWidget.setStyleSheet("QWidget#scrollWidget { background-color: transparent; }")
        self.setStyleSheet("SettingInterface { background-color: transparent; }")

        # add items to group
        self.personalGroup.addSettingCard(self.languageCard)
        
        # Connect signal
        self.languageCard.comboBox.currentIndexChanged.connect(self.onLanguageChanged)

        # add groups to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)

    def onLanguageChanged(self):
        InfoBar.success(
            title=self.tr('配置已更新'),
            content=self.tr('重启程序后生效'),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        self.restartBtn.show()

    def closeApp(self):
        # Save config
        cfg.save()
        sys.exit()
