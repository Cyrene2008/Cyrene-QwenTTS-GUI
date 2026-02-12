from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar, QFrame, QFileDialog
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from qfluentwidgets import (
    SubtitleLabel, PrimaryPushButton, ComboBox, StrongBodyLabel, 
    CaptionLabel, InfoBar, InfoBarPosition, PushButton, FluentIcon as FIF,
    CardWidget, BodyLabel, SmoothScrollArea, Slider
)

from app.core.backend import QwenTTSBackend
from app.core.config import QWEN_TTS_BASE_MODEL_LIST, QWEN_TTS_CUSTOM_VOICE_MODEL_LIST

class PlainTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QTextEdit { background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 5px; padding: 8px; selection-background-color: #009faa; color: black; }")

    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

class ModelLoader(QThread):
    finished = Signal(bool, str)

    def __init__(self, backend, model_name):
        super().__init__()
        self.backend = backend
        self.model_name = model_name

    def run(self):
        try:
            self.backend.load_model(self.model_name)
            self.finished.emit(True, f"Model {self.model_name} loaded.")
        except Exception as e:
            self.finished.emit(False, str(e))

class AudioGenerator(QThread):
    finished = Signal(bool, str, str) # success, message, file_path

    def __init__(self, backend, text, speaker):
        super().__init__()
        self.backend = backend
        self.text = text
        self.speaker = speaker

    def run(self):
        try:
            path = self.backend.generate_custom_voice(text=self.text, speaker=self.speaker)
            self.finished.emit(True, self.tr("Generation successful"), str(path))
        except Exception as e:
            self.finished.emit(False, str(e), "")

class GenerationInterface(SmoothScrollArea):
    def __init__(self, backend=None, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("generationInterface")
        self.backend = backend
        
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName("scrollWidget")
        self.scrollWidget.setStyleSheet("background-color: transparent;")
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: transparent; border: none;")
        self.viewport().setStyleSheet("background-color: transparent;")
        
        self.initUI()
        self.initAudioPlayer()
        
        if self.backend:
             self.onBackendReady()

    def setBackend(self, backend):
        self.backend = backend
        self.onBackendReady()

    def onBackendReady(self):
        current = self.modelCombo.currentText()
        if current:
            self.loadModel(current)

    def initUI(self):
        self.mainLayout = QVBoxLayout(self.scrollWidget)
        self.mainLayout.setContentsMargins(30, 30, 30, 30)
        self.mainLayout.setSpacing(20)
        
        self.titleLabel = SubtitleLabel(self.tr("语音生成"), self.scrollWidget)
        self.mainLayout.addWidget(self.titleLabel)
        
        self.settingsCard = CardWidget(self.scrollWidget)
        self.settingsLayout = QVBoxLayout(self.settingsCard)
        
        self.modelLayout = QHBoxLayout()
        self.modelLabel = StrongBodyLabel(self.tr("模型:"), self.scrollWidget)
        self.modelCombo = ComboBox(self.scrollWidget)
        self.modelCombo.addItems(QWEN_TTS_BASE_MODEL_LIST + QWEN_TTS_CUSTOM_VOICE_MODEL_LIST)
        self.modelCombo.currentTextChanged.connect(self.onModelChanged)
        self.modelLayout.addWidget(self.modelLabel)
        self.modelLayout.addWidget(self.modelCombo, 1)
        self.settingsLayout.addLayout(self.modelLayout)
        
        self.speakerLayout = QHBoxLayout()
        self.speakerLabel = StrongBodyLabel(self.tr("说话人:"), self.scrollWidget)
        self.speakerCombo = ComboBox(self.scrollWidget)
        self.speakerLayout.addWidget(self.speakerLabel)
        self.speakerLayout.addWidget(self.speakerCombo, 1)
        self.settingsLayout.addLayout(self.speakerLayout)
        
        self.speakerTipLabel = BodyLabel(self.tr("提示：预设说话人由模型提供。如需克隆/自定义音色，请使用左侧【声音克隆】功能。"), self.scrollWidget)
        self.speakerTipLabel.setStyleSheet("color: gray; font-size: 12px;")
        self.settingsLayout.addWidget(self.speakerTipLabel)
        
        self.mainLayout.addWidget(self.settingsCard)
        
        self.textLabel = StrongBodyLabel(self.tr("输入文本:"), self.scrollWidget)
        self.mainLayout.addWidget(self.textLabel)
        
        self.textEdit = PlainTextEdit(self.scrollWidget)
        self.textEdit.setPlaceholderText(self.tr("请输入要合成的文本..."))
        self.textEdit.setMinimumHeight(150)
        self.mainLayout.addWidget(self.textEdit)
        
        self.controlsLayout = QHBoxLayout()
        
        self.genBtn = PrimaryPushButton(FIF.PLAY_SOLID, self.tr("生成音频"), self.scrollWidget)
        self.genBtn.clicked.connect(self.startGeneration)
        self.controlsLayout.addWidget(self.genBtn)
        
        self.playBtn = PushButton(FIF.PLAY, self.tr("播放"), self.scrollWidget)
        self.playBtn.clicked.connect(self.playAudio)
        self.playBtn.setEnabled(False)
        self.controlsLayout.addWidget(self.playBtn)
        
        self.saveBtn = PushButton(FIF.SAVE, self.tr("另存为"), self.scrollWidget)
        self.saveBtn.clicked.connect(self.saveAudio)
        self.saveBtn.setEnabled(False)
        self.controlsLayout.addWidget(self.saveBtn)
        
        self.controlsLayout.addStretch(1)
        self.mainLayout.addLayout(self.controlsLayout)
        
        self.playerLayout = QHBoxLayout()
        self.slider = Slider(Qt.Orientation.Horizontal, self.scrollWidget)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)
        self.slider.sliderPressed.connect(self.onSliderPressed)
        self.slider.sliderReleased.connect(self.onSliderReleased)
        self.playerLayout.addWidget(self.slider, 1)
        
        self.timeLabel = CaptionLabel("00:00 / 00:00", self.scrollWidget)
        self.playerLayout.addWidget(self.timeLabel)
        self.mainLayout.addLayout(self.playerLayout)
        
        self.progressBar = QProgressBar(self.scrollWidget)
        self.progressBar.setRange(0, 0)
        self.progressBar.hide()
        self.mainLayout.addWidget(self.progressBar)
        
        self.mainLayout.addStretch(1)

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
        self.playBtn.setText(self.tr("暂停"))
        
    def updateTimeLabel(self):
        position = self.player.position()
        duration = self.player.duration()
        
        def formatTime(ms):
            seconds = (ms // 1000) % 60
            minutes = (ms // 60000)
            return f"{minutes:02}:{seconds:02}"
            
        self.timeLabel.setText(f"{formatTime(position)} / {formatTime(duration)}")

    def setVolume(self, volume):
        self.audioOutput.setVolume(volume)

    def loadModel(self, model_name):
        if not self.backend: 
            self.showError(self.tr("后端未连接"))
            return
        
        self.genBtn.setEnabled(False)
        self.modelCombo.setEnabled(False)
        self.progressBar.show()
        self.showInfo(self.tr("正在加载模型 {model_name} (如果首次使用可能需要下载)...").format(model_name=model_name), InfoBarPosition.TOP_RIGHT)
        
        self.loader = ModelLoader(self.backend, model_name)
        self.loader.finished.connect(self.onModelLoaded)
        self.loader.start()

    def onModelChanged(self, text):
        self.loadModel(text)

    def onModelLoaded(self, success, msg):
        self.progressBar.hide()
        self.genBtn.setEnabled(True)
        self.modelCombo.setEnabled(True)
        
        if success:
            self.showSuccess(self.tr("模型加载成功"))
            # Update speakers
            try:
                speakers = self.backend.get_supported_speakers()
                self.speakerCombo.clear()
                if speakers:
                    self.speakerCombo.addItems(speakers)
                    self.speakerCombo.setCurrentIndex(0)
                else:
                    self.speakerCombo.addItem(self.tr("默认"))
            except:
                self.speakerCombo.addItem(self.tr("默认"))
        else:
            self.showError(self.tr("模型加载失败: {msg}").format(msg=msg))

    def startGeneration(self):
        if not self.backend: 
            self.showError(self.tr("后端未连接"))
            return
            
        text = self.textEdit.toPlainText().strip()
        if not text:
            self.showError(self.tr("请输入一些文本。"))
            return
            
        speaker = self.speakerCombo.currentText()
        
        self.genBtn.setEnabled(False)
        self.progressBar.show()
        
        self.generator = AudioGenerator(self.backend, text, speaker)
        self.generator.finished.connect(self.onGenerationFinished)
        self.generator.start()

    def onGenerationFinished(self, success, msg, path):
        self.progressBar.hide()
        self.genBtn.setEnabled(True)
        
        if success:
            self.showSuccess(self.tr("生成成功"))
            self.current_audio_path = path
            self.playBtn.setEnabled(True)
            self.saveBtn.setEnabled(True)
            # Auto play
            self.playAudio()
        else:
            self.showError(self.tr("生成失败: {msg}").format(msg=msg))

    def saveAudio(self):
        if hasattr(self, 'current_audio_path') and self.current_audio_path:
            savePath, _ = QFileDialog.getSaveFileName(self, self.tr("保存音频"), "generated.wav", "Audio Files (*.wav)")
            if savePath:
                try:
                    import shutil
                    shutil.copy(self.current_audio_path, savePath)
                    self.showSuccess(self.tr("保存成功"))
                except Exception as e:
                    self.showError(self.tr("保存失败: {e}").format(e=e))

    def playAudio(self):
        if hasattr(self, 'current_audio_path') and self.current_audio_path:
            self.player.setSource(QUrl.fromLocalFile(self.current_audio_path))
            self.player.play()
            self.playBtn.setIcon(FIF.PAUSE)
            self.playBtn.setText(self.tr("暂停"))
            # Disconnect previous clicked
            try:
                self.playBtn.clicked.disconnect()
            except: pass
            self.playBtn.clicked.connect(self.pauseAudio)

    def pauseAudio(self):
        self.player.pause()
        self.playBtn.setIcon(FIF.PLAY)
        self.playBtn.setText(self.tr("播放"))
        try:
            self.playBtn.clicked.disconnect()
        except: pass
        self.playBtn.clicked.connect(self.playAudio)

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playBtn.setIcon(FIF.PLAY)
            self.playBtn.setText(self.tr("播放"))
            try:
                self.playBtn.clicked.disconnect()
            except: pass
            self.playBtn.clicked.connect(self.playAudio)

    def showInfo(self, text, position=InfoBarPosition.TOP_RIGHT):
        InfoBar.info(
            title='',
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=position,
            duration=2000,
            parent=self
        )

    def showSuccess(self, text):
        InfoBar.success(
            title='',
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def showError(self, text):
        InfoBar.error(
            title='',
            content=text,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )
