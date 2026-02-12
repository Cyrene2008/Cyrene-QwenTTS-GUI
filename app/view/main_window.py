from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsOpacityEffect, QApplication, QLabel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QVideoSink
from PySide6.QtCore import QUrl, Qt, Property, QPropertyAnimation, QEasingCurve, QRectF, QTimer, QThread, Signal
from PySide6.QtGui import QPainter, QIcon, QPixmap

from .generation_interface import GenerationInterface
from .design_interface import DesignInterface
from .clone_interface import CloneInterface
from .browser_interface import BrowserInterface
from .setting_interface import SettingInterface
from .about_interface import AboutInterface
from .wizard_interface import WizardInterface
from .home_interface import HomeInterface

from app.core.env_manager import EnvManager
from app.core.backend import QwenTTSBackend
from qfluentwidgets import FluentWindow, FluentIcon as FIF, NavigationItemPosition, InfoBar, InfoBarPosition, InfoBarManager
from ..common.config import cfg
from ..common.resource import get_resource_path
import os

class BackendThread(QThread):
    finished = Signal(bool, object, str)

    def run(self):
        try:
            backend = QwenTTSBackend()
            self.finished.emit(True, backend, "")
        except Exception as e:
            self.finished.emit(False, None, str(e))

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        
        self.initVideoBackground()
        
        self.backend = None
        
        self.generationInterface = GenerationInterface(self.backend, self)
        self.designInterface = DesignInterface(self)
        self.cloneInterface = CloneInterface(self)
        self.browserInterface = BrowserInterface(self)
        self.settingInterface = SettingInterface(self)
        self.aboutInterface = AboutInterface(self)
        self.wizardInterface = WizardInterface(self)
        self.wizardInterface.openSettings.connect(self.onOpenSettings)
        self.homeInterface = HomeInterface(self)

        self.initNavigation()
        self.initWindow()
        
        self.stackedWidget.addWidget(self.wizardInterface)
        
        self.initSplash()
        
        self.stackedWidget.currentChanged.connect(self.onInterfaceChanged)
        
        self.initMask()

    def onOpenSettings(self):
        self.switchTo(self.settingInterface)
        self.navigationInterface.show()

    def checkEnvironment(self):
        self.envManager = EnvManager()
        self.envManager.finished.connect(self.onEnvCheckFinished)
        self.envManager.start()

    def onEnvCheckFinished(self, valid, msg):
        if valid:
            self.initBackend()
            if self.stackedWidget.currentWidget() == self.wizardInterface:
                self.switchTo(self.generationInterface)
                self.navigationInterface.show()
        else:
            # Show Wizard
            self.showError(self.tr("Environment check failed: ") + msg)
            self.switchTo(self.wizardInterface)
            self.navigationInterface.hide()

    def initBackend(self):
        self.backendThread = BackendThread()
        self.backendThread.finished.connect(self.onBackendInitFinished)
        self.backendThread.start()
        
        InfoBar.info(
            title=self.tr("Initializing Backend"),
            content=self.tr("Starting QwenTTS service..."),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )

    def onBackendInitFinished(self, success, backend, msg):
        if success:
            self.backend = backend
            self.generationInterface.setBackend(self.backend)
            self.cloneInterface.setBackend(self.backend)
            self.designInterface.setBackend(self.backend)
            
            self.showSuccess(
                title=self.tr("Backend Ready"),
                content=self.tr("QwenTTS service started successfully."),
                duration=3000
            )
            
            try:
                device_info = self.backend.get_device_info()
                if not device_info.get("cuda_available", False):
                     self.showWarning(
                        title=self.tr("性能警告 (Performance Warning)"),
                        content=self.tr("检测到 CUDA 不可用，当前正在使用 CPU 进行推理，速度将会非常慢。\n请确保您已安装兼容的 GPU 和驱动程序，并安装了正确的 PyTorch 版本。"),
                        duration=10000
                    )
                else:
                    self.showSuccess(
                        title=self.tr("检测到 GPU (GPU Detected)"),
                        content=self.tr("正在使用 GPU 运行: {name}").format(name=device_info.get("device_name", "Unknown")),
                        duration=3000
                    )
            except:
                pass

        else:
            self.showError(self.tr("Failed to start backend: ") + msg)

    def showSuccess(self, title, content, duration=3000):
        w = InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=duration,
            parent=self
        )
        w.raise_()

    def showWarning(self, title, content, duration=5000):
        w = InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=duration,
            parent=self
        )
        w.raise_()

    def showError(self, text):
        w = InfoBar.error(
            title=self.tr('Error'),
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=self
        )
        w.raise_()

    def initVideoBackground(self):
        self.videoWidget = VideoBackgroundWidget(self)
        self.videoWidget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.player = QMediaPlayer(self)
        self.audioOutput = QAudioOutput(self)
        self.player.setAudioOutput(self.audioOutput)
        self.player.setVideoOutput(self.videoWidget.videoSink)
        
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.audioOutput.setVolume(0) 
        
        videoPath = get_resource_path("app/resource/video/BgVideo.mp4")
        self.player.setSource(QUrl.fromLocalFile(videoPath))
        
        self.player.stop()
        
        self.videoWidget.lower()

    def onBgVideoStatusChanged(self, status):
        pass 

    def initMask(self):
        self.maskWidget = QWidget(self)
        self.maskWidget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.maskWidget.setStyleSheet("background-color: white;")
        self.maskEffect = QGraphicsOpacityEffect(self.maskWidget)
        self.maskWidget.setGraphicsEffect(self.maskEffect)
        self.maskEffect.setOpacity(0)
        self.maskWidget.hide()
        
        self.maskAnim = QPropertyAnimation(self.maskEffect, b"opacity")
        self.maskAnim.setDuration(300)
        self.maskAnim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.maskWidget.stackUnder(self.stackedWidget)

    def initSplash(self):
        self.splashWidget = QWidget(self)
        self.splashWidget.resize(self.size())
        self.splashWidget.setStyleSheet("background-color: black;")
        self.splashWidget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
        self.stackedWidget.hide()
        self.navigationInterface.hide()
        self.titleBar.hide()
        
        self.splashLoopWidget = VideoBackgroundWidget(self.splashWidget)
        self.splashLoopWidget.resize(self.size())
        self.splashLoopWidget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.splashTransWidget = VideoBackgroundWidget(self.splashWidget)
        self.splashTransWidget.resize(self.size())
        self.splashTransWidget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.splashTransWidget.hide()
        
        self.splashPlayer = QMediaPlayer(self)
        self.splashAudio = QAudioOutput(self)
        self.splashPlayer.setAudioOutput(self.splashAudio)
        self.splashPlayer.setVideoOutput(self.splashLoopWidget.videoSink)
        self.splashAudio.setVolume(100)
        self.splashPlayer.errorOccurred.connect(self.onSplashError)
        
        self.transPlayer = QMediaPlayer(self)
        self.transAudio = QAudioOutput(self)
        self.transPlayer.setAudioOutput(self.transAudio)
        self.transPlayer.setVideoOutput(self.splashTransWidget.videoSink)
        self.transPlayer.errorOccurred.connect(self.onSplashError)
        self.transPlayer.mediaStatusChanged.connect(self.checkTransEnd)
        self.splashTransWidget.videoSink.videoFrameChanged.connect(self.onTransFrameChanged)
        
        self.inTrans = False
        self.fadeStarted = False
        
        loopPath = get_resource_path("app/resource/video/SplashLoop.mp4")
        transPath = get_resource_path("app/resource/video/SplashTrans.mp4")
        
        if os.path.exists(loopPath) and os.path.exists(transPath):
            self.splashPlaceholder = QLabel(self.splashWidget)
            self.splashPlaceholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.splashPlaceholder.setStyleSheet("background-color: black;")
            logoPath = get_resource_path("app/resource/images/Cyrene.png")
            if os.path.exists(logoPath):
                self.splashPlaceholder.setPixmap(QPixmap(logoPath).scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.splashPlaceholder.resize(self.size())
            self.splashPlaceholder.show()
            self.splashPlaceholder.raise_()
            
            self.splashPlayer.mediaStatusChanged.connect(self.onSplashLoopStatusChanged)

            self.splashPlayer.setSource(QUrl.fromLocalFile(loopPath))
            self.splashPlayer.setLoops(QMediaPlayer.Loops.Infinite)
            self.splashPlayer.play()
            
            self.transPlayer.setSource(QUrl.fromLocalFile(transPath))
            
            self.splashWidget.mousePressEvent = self.onSplashClicked
            self.splashWidget.show()
            self.splashWidget.raise_()
        else:
            self.finishSplash()

    def onSplashLoopStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.BufferedMedia or status == QMediaPlayer.MediaStatus.LoadedMedia:
            # Video ready, hide placeholder
            if hasattr(self, 'splashPlaceholder'):
                self.splashPlaceholder.hide()
                self.splashPlaceholder.deleteLater()
                del self.splashPlaceholder

    def onSplashError(self):
        self.finishSplash()

    def onSplashClicked(self, e):
        if self.inTrans:
            return
            
        self.inTrans = True
        
        QTimer.singleShot(50, self.transPlayer.play)
        
        self.splashSafetyTimer = QTimer(self)
        self.splashSafetyTimer.setSingleShot(True)
        self.splashSafetyTimer.timeout.connect(self.finishSplash)
        self.splashSafetyTimer.start(8000)

    def onTransFrameChanged(self):
        if not hasattr(self, 'splashTransWidget'):
            return
            
        if self.inTrans and not self.splashTransWidget.isVisible():
            self.splashTransWidget.show()
            self.splashTransWidget.raise_()
            if hasattr(self, 'splashPlayer'):
                self.splashPlayer.stop()
            if hasattr(self, 'splashLoopWidget'):
                self.splashLoopWidget.hide()

    def startSplashFadeOut(self):
        if self.fadeStarted:
            return
        self.fadeStarted = True
        
        if hasattr(self, 'player'):
             self.player.play()
             
        self.splashEffect = QGraphicsOpacityEffect(self.splashWidget)
        self.splashWidget.setGraphicsEffect(self.splashEffect)
        self.splashAnim = QPropertyAnimation(self.splashEffect, b"opacity")
        self.splashAnim.setDuration(800)
        self.splashAnim.setStartValue(1.0)
        self.splashAnim.setEndValue(0.0)
        self.splashAnim.setEasingCurve(QEasingCurve.Type.InQuad)
        self.splashAnim.finished.connect(self.finishSplash)
        self.splashAnim.start()

    def checkTransEnd(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if hasattr(self, 'splashTransWidget'):
                image = self.splashTransWidget.grabFramebuffer()
                if not image.isNull():
                    self.splashSnapshotLabel = QLabel(self.splashWidget)
                    self.splashSnapshotLabel.resize(self.size())
                    self.splashSnapshotLabel.setPixmap(QPixmap.fromImage(image))
                    self.splashSnapshotLabel.show()
                    self.splashSnapshotLabel.raise_()
            
            if hasattr(self, 'transPlayer'):
                self.transPlayer.stop()
            if hasattr(self, 'splashTransWidget'):
                self.splashTransWidget.hide()
                
            if not self.fadeStarted:
                self.startSplashFadeOut()

    def finishSplash(self):
        if hasattr(self, 'splashSafetyTimer'):
            self.splashSafetyTimer.stop()
            self.splashSafetyTimer.deleteLater()
            del self.splashSafetyTimer

        if hasattr(self, 'splashWidget'):
            self.splashWidget.hide()
            self.splashWidget.deleteLater()
            del self.splashWidget
            
        if hasattr(self, 'splashPlayer'):
            self.splashPlayer.deleteLater()
            del self.splashPlayer
            
        if hasattr(self, 'transPlayer'):
            self.transPlayer.deleteLater()
            del self.transPlayer
            
        if hasattr(self, 'splashLoopWidget'):
            self.splashLoopWidget.deleteLater()
            del self.splashLoopWidget
            
        if hasattr(self, 'splashTransWidget'):
            self.splashTransWidget.deleteLater()
            del self.splashTransWidget

        self.stackedWidget.show()
        if self.stackedWidget.currentWidget() != self.wizardInterface:
            self.navigationInterface.show()
        self.titleBar.show()
        self.titleBar.raise_()

        self.activateWindow()
        
        if hasattr(self, 'player') and self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.player.play()
            
        QTimer.singleShot(500, self.checkEnvironment)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'videoWidget'):
            self.videoWidget.resize(self.size())
            self.videoWidget.move(0, 0)
            self.videoWidget.lower() 
            
        if hasattr(self, 'maskWidget'):
            self.maskWidget.resize(self.size())
            self.maskWidget.move(0, 0)
            self.maskWidget.stackUnder(self.stackedWidget) 
            self.videoWidget.stackUnder(self.maskWidget)
            
            if self.stackedWidget.isVisible():
                self.stackedWidget.raise_()
            if self.navigationInterface.isVisible():
                self.navigationInterface.raise_()
            if self.titleBar.isVisible():
                self.titleBar.raise_()
            
        if hasattr(self, 'splashWidget') and self.splashWidget.isVisible():
            self.splashWidget.resize(self.size())
            self.splashWidget.raise_()
            if hasattr(self, 'splashLoopWidget'):
                self.splashLoopWidget.resize(self.size())
            if hasattr(self, 'splashTransWidget'):
                self.splashTransWidget.resize(self.size())
            if hasattr(self, 'splashPlaceholder') and self.splashPlaceholder.isVisible():
                self.splashPlaceholder.resize(self.size())
                self.splashPlaceholder.raise_()
            
            QTimer.singleShot(0, self.splashWidget.raise_)


    def onInterfaceChanged(self, index):
        widget = self.stackedWidget.widget(index)
        targetOpacity = 0.0
        
        if widget in [self.generationInterface, self.designInterface, self.cloneInterface, self.browserInterface]:
            targetOpacity = 0.3
        elif widget == self.aboutInterface:
            targetOpacity = 0.5
        elif widget == self.wizardInterface:
            targetOpacity = 0.8
        elif widget == self.homeInterface:
            targetOpacity = 0.0
        else:
            targetOpacity = 0.3
            
        self.maskWidget.show()
        self.maskAnim.stop()
        self.maskAnim.setStartValue(self.maskEffect.opacity())
        self.maskAnim.setEndValue(targetOpacity)
        self.maskAnim.start()

    def closeEvent(self, event):
        if self.backend:
            self.backend.shutdown()
        
        if hasattr(self, 'player'):
            self.player.stop()
        if hasattr(self, 'splashPlayer'):
            self.splashPlayer.stop()
            
        super().closeEvent(event)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.addSubInterface(self.generationInterface, FIF.MICROPHONE, self.tr('Voice Generation'))
        self.addSubInterface(self.designInterface, FIF.EDIT, self.tr('Voice Design'))
        self.addSubInterface(self.cloneInterface, FIF.PEOPLE, self.tr('Voice Clone'))
        self.addSubInterface(self.browserInterface, FIF.MUSIC_FOLDER, self.tr('Audio Browser'))
        
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Settings'), position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.aboutInterface, FIF.INFO, self.tr('About'), position=NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1280, 720) 
        self.setMinimumSize(1280, 720)
        self.setWindowTitle('QwenTTS Cyrene GUI')
        self.setWindowIcon(QIcon(get_resource_path("app/resource/images/Cyrene.ico")))
        
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        
        self.titleBar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.titleBar.setStyleSheet("background-color: transparent;")
        
        self.windowEffect.setMicaEffect(self.winId(), False) 
        
        self.stackedWidget.setStyleSheet("background: transparent;")
        self.stackedWidget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.navigationInterface.setObjectName("navigationInterface")
        self.navigationInterface.setStyleSheet("#navigationInterface { background: transparent; }")


class VideoBackgroundWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.videoSink = QVideoSink(self)
        self.videoSink.videoFrameChanged.connect(self.onVideoFrameChanged)
        self._image = None
        
        self._target_rect = None
        self._last_size = None
        self._last_img_size = None

    def onVideoFrameChanged(self, frame):
        image = frame.toImage()
        if image.isNull():
            return
        self._image = image
        self.update()

    def resizeEvent(self, e):
        self._target_rect = None
        super().resizeEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
        if self._image is None or self._image.isNull():
            painter.fillRect(self.rect(), Qt.GlobalColor.black)
            return
            
        img_w = self._image.width()
        img_h = self._image.height()
        
        if img_w == 0 or img_h == 0:
            painter.fillRect(self.rect(), Qt.GlobalColor.black)
            return
            
        current_size = self.size()
        current_img_size = (img_w, img_h)
        
        if (self._target_rect is None or 
            self._last_size != current_size or 
            self._last_img_size != current_img_size):
            
            w = self.width()
            h = self.height()
            
            scale = max(w / img_w, h / img_h)
            draw_w = img_w * scale
            draw_h = img_h * scale
            x = (w - draw_w) / 2
            y = (h - draw_h) / 2
            
            self._target_rect = QRectF(x, y, draw_w, draw_h)
            self._last_size = current_size
            self._last_img_size = current_img_size
            
        painter.drawImage(self._target_rect, self._image)
