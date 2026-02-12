from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QButtonGroup, QStackedWidget, QTextEdit
from PySide6.QtCore import Qt, Signal
import sys
from qfluentwidgets import (
    SubtitleLabel, BodyLabel, PrimaryPushButton, PushButton, 
    ProgressBar, IndeterminateProgressBar, InfoBar, ComboBox,
    TransparentToolButton, FluentIcon as FIF
)
from app.core.env_manager import EnvManager

class WizardInterface(QWidget):
    openSettings = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("wizardInterface")
        
        self.env_manager = EnvManager()
        self.env_manager.progress.connect(self.onProgress)
        self.env_manager.finished.connect(self.onFinished)
        
        self.initUI()
        
    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(50, 50, 50, 50)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.stackedWidget = QStackedWidget(self)
        self.mainLayout.addWidget(self.stackedWidget)
        
        # Page 1: Intro
        self.pageIntro = QWidget()
        self.introLayout = QVBoxLayout(self.pageIntro)
        self.introLayout.setSpacing(20)
        self.introLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.titleLabel = SubtitleLabel(self.tr("初次运行环境配置 (Environment Setup)"), self)
        self.introLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.descLabel = BodyLabel(self.tr("检测到缺少必要组件 (PyTorch, CUDA 等)。\n请选择下载源以安装环境。\n(Missing components detected. Please install environment.)"), self)
        self.descLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.introLayout.addWidget(self.descLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Intro Buttons
        self.introBtnLayout = QHBoxLayout()
        self.introBtnLayout.setSpacing(20)
        self.introBtnLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.installBtn = PrimaryPushButton(self.tr("安装 GPU 版本 (Install GPU)"), self)
        self.installBtn.setFixedWidth(200)
        self.installBtn.clicked.connect(self.goToMirrorPage)
        
        self.skipBtn = PushButton(self.tr("安装 CPU 版本 (Install CPU)"), self)
        self.skipBtn.setFixedWidth(200)
        self.skipBtn.setToolTip(self.tr("安装 PyTorch CPU 版本 (无 CUDA)"))
        self.skipBtn.clicked.connect(self.goToMirrorPageCPU)
        
        self.useSystemBtn = PushButton(self.tr("使用系统 Python (System)"), self)
        self.useSystemBtn.setFixedWidth(200)
        self.useSystemBtn.setToolTip(self.tr("使用当前系统 Python 环境"))
        self.useSystemBtn.clicked.connect(self.onUseSystem)
        
        self.introBtnLayout.addWidget(self.installBtn)
        self.introBtnLayout.addWidget(self.skipBtn)
        self.introBtnLayout.addWidget(self.useSystemBtn)
        
        self.introLayout.addLayout(self.introBtnLayout)
        
        # Bottom Settings Button
        self.introLayout.addStretch(1)
        self.bottomLayout = QHBoxLayout()
        self.settingsBtn = TransparentToolButton(FIF.SETTING, self)
        self.settingsBtn.setToolTip(self.tr("设置 (Settings)"))
        self.settingsBtn.clicked.connect(self.openSettings.emit)
        self.bottomLayout.addWidget(self.settingsBtn)
        self.bottomLayout.addStretch(1)
        self.introLayout.addLayout(self.bottomLayout)
        
        self.stackedWidget.addWidget(self.pageIntro)
        
        # Page 2: Mirror Selection
        self.pageMirror = QWidget()
        self.mirrorLayout = QVBoxLayout(self.pageMirror)
        self.mirrorLayout.setSpacing(20)
        self.mirrorLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.mirrorTitle = SubtitleLabel(self.tr("选择镜像源 (Select Mirror)"), self)
        self.mirrorLayout.addWidget(self.mirrorTitle, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.mirrorComboBox = ComboBox(self)
        self.mirrorComboBox.addItem(self.tr("阿里云镜像 (推荐)"), "aliyun")
        self.mirrorComboBox.addItem(self.tr("官方源 (PyPI)"), "official")
        self.mirrorComboBox.setFixedWidth(300)
        self.mirrorComboBox.setCurrentIndex(0) # Default to Aliyun
        
        self.mirrorLayout.addWidget(self.mirrorComboBox, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Mirror Buttons
        self.mirrorBtnLayout = QHBoxLayout()
        self.mirrorBtnLayout.setSpacing(20)
        self.mirrorBtnLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.backBtn = PushButton(self.tr("返回 (Back)"), self)
        self.backBtn.clicked.connect(self.goBackToIntro)
        
        self.confirmInstallBtn = PrimaryPushButton(self.tr("确认安装 (Confirm)"), self)
        self.confirmInstallBtn.clicked.connect(self.startInstall)
        
        self.mirrorBtnLayout.addWidget(self.backBtn)
        self.mirrorBtnLayout.addWidget(self.confirmInstallBtn)
        self.mirrorLayout.addLayout(self.mirrorBtnLayout)
        
        self.stackedWidget.addWidget(self.pageMirror)
        
        # Page 3: Progress
        self.pageProgress = QWidget()
        self.progressLayout = QVBoxLayout(self.pageProgress)
        self.progressLayout.setSpacing(20)
        self.progressLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progressTitle = SubtitleLabel(self.tr("正在安装环境..."), self)
        self.progressLayout.addWidget(self.progressTitle, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.statusLabel = BodyLabel(self.tr("准备中..."), self)
        self.progressLayout.addWidget(self.statusLabel, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.progressBar = ProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(400)
        self.progressLayout.addWidget(self.progressBar, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.logText = QTextEdit(self)
        self.logText.setReadOnly(True)
        self.logText.setPlaceholderText(self.tr("Installation logs will appear here..."))
        # Fix style: Black text, disable wrapping for cleaner logs, modern scrollbar
        self.logText.setStyleSheet("""
            QTextEdit {
                color: black;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                font-family: Consolas, "Courier New", monospace;
                font-size: 12px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        self.logText.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.progressLayout.addWidget(self.logText)
        
        self.exitBtn = PrimaryPushButton(self.tr("退出程序"), self)
        self.exitBtn.clicked.connect(lambda: sys.exit(0))
        self.exitBtn.hide()
        self.progressLayout.addWidget(self.exitBtn, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.stackedWidget.addWidget(self.pageProgress)
        
        self.stackedWidget.setCurrentIndex(0)
        
    def goToMirrorPage(self):
        self.env_manager.cpu_mode = False
        self.stackedWidget.setCurrentIndex(1)
        
    def goToMirrorPageCPU(self):
        self.env_manager.cpu_mode = True
        self.stackedWidget.setCurrentIndex(1)
        
    def goBackToIntro(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def startInstall(self):
        mirror = "https://pypi.org/simple"
        # Check index as well to ensure it works even if currentData fails
        if self.mirrorComboBox.currentData() == "aliyun" or self.mirrorComboBox.currentIndex() == 0:
            mirror = "https://mirrors.aliyun.com/pypi/simple/"
            
        self.stackedWidget.setCurrentIndex(2)
        self.logText.clear()
        self.logText.append(f"Selected Mirror: {mirror}")
        self.env_manager.set_install_mode(mirror)
        self.env_manager.start()
        
    def onUseSystem(self):
        self.stackedWidget.setCurrentIndex(2)
        self.statusLabel.setText(self.tr("Checking system environment..."))
        from app.common.config import ROOT_PATH
        marker_file = ROOT_PATH / "use_system_python.marker"
        with open(marker_file, "w") as f:
            f.write("1")
        self.env_manager.use_system_python = True
        self.env_manager.skip_cuda_check = True
        valid, msg = self.env_manager.check_env()
        if valid:
             self.onFinished(True, self.tr("System environment verified"))
        else:
             try:
                 import os
                 os.remove(marker_file)
             except: pass
             self.env_manager.use_system_python = False
             self.onFinished(False, self.tr("System environment missing dependencies: {msg}").format(msg=msg))

    def onProgress(self, msg, value):
        self.statusLabel.setText(msg)
        self.progressBar.setValue(value)
        self.logText.append(msg)
        # Auto scroll to bottom
        scrollbar = self.logText.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def onFinished(self, success, msg):
        if success:
            self.statusLabel.setText(self.tr("Installation complete! Please restart the program."))
            self.progressBar.setValue(100)
            InfoBar.success(
                title=self.tr('Success'),
                content=self.tr('Environment configured. Please restart to load new environment.'),
                orient=Qt.Orientation.Horizontal,
                isClosable=False,
                duration=-1,
                parent=self
            )
            self.exitBtn.show()
        else:
            self.statusLabel.setText(self.tr("Installation failed: {msg}").format(msg=msg))
            InfoBar.error(
                title=self.tr('Failed'),
                content=msg,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                duration=-1,
                parent=self
            )
            # Add a "Back" button to retry? Or just let them restart.
            # For now, maybe just show a back button in progress page if failed
            if not hasattr(self, 'retryBtn'):
                self.retryBtn = PushButton(self.tr("Retry"), self)
                self.retryBtn.clicked.connect(self.goBackToIntro)
                self.progressLayout.addWidget(self.retryBtn, 0, Qt.AlignmentFlag.AlignCenter)
            self.retryBtn.show()
