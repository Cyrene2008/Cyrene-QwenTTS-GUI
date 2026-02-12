from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QProgressBar, QFileDialog
from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from qfluentwidgets import (
    SubtitleLabel, PrimaryPushButton, StrongBodyLabel, 
    CaptionLabel, InfoBar, InfoBarPosition, PushButton, FluentIcon as FIF,
    CardWidget, LineEdit, CheckBox, SmoothScrollArea, Slider
)

class PlainTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QTextEdit { background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(0, 0, 0, 0.1); border-radius: 5px; padding: 8px; selection-background-color: #009faa; color: black; }")

    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

class CloneGenerator(QThread):
    finished = Signal(bool, str, str) # success, message, file_path

    def __init__(self, backend, text, ref_audio, ref_text=None):
        super().__init__()
        self.backend = backend
        self.text = text
        self.ref_audio = ref_audio
        self.ref_text = ref_text

    def run(self):
        try:
            x_vector = False
            if not self.ref_text:
                x_vector = True
            
            path = self.backend.generate_voice_clone(
                text=self.text, 
                ref_audio=self.ref_audio,
                ref_text=self.ref_text,
                x_vector_only_mode=x_vector
            )
            self.finished.emit(True, self.tr("生成成功"), str(path))
        except Exception as e:
            self.finished.emit(False, str(e), "")

class CloneInterface(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("cloneInterface")
        self.backend = None
        self.current_audio_path = None
        self.ref_audio_path = None
        
        self.scrollWidget = QWidget()
        self.scrollWidget.setObjectName("scrollWidget")
        self.scrollWidget.setStyleSheet("background-color: transparent;")
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: transparent; border: none;")
        self.viewport().setStyleSheet("background-color: transparent;")
        
        self.initUI()
        self.initAudioPlayer()

    def setBackend(self, backend):
        self.backend = backend

    def initUI(self):
        self.mainLayout = QVBoxLayout(self.scrollWidget)
        self.mainLayout.setContentsMargins(30, 30, 30, 30)
        self.mainLayout.setSpacing(20)
        
        self.titleLabel = SubtitleLabel(self.tr("声音克隆"), self.scrollWidget)
        self.mainLayout.addWidget(self.titleLabel)
        
        self.settingsCard = CardWidget(self.scrollWidget)
        self.settingsLayout = QVBoxLayout(self.settingsCard)
        
        self.refLayout = QHBoxLayout()
        self.refLabel = StrongBodyLabel(self.tr("参考音频:"), self.scrollWidget)
        self.refPathEdit = LineEdit(self.scrollWidget)
        self.refPathEdit.setPlaceholderText(self.tr("请选择参考音频文件..."))
        self.refPathEdit.setReadOnly(True)
        self.refPathEdit.setStyleSheet("LineEdit { color: black; }")
        self.browseBtn = PushButton(FIF.FOLDER, self.tr("浏览"), self.scrollWidget)
        self.browseBtn.clicked.connect(self.browseAudio)
        
        self.refLayout.addWidget(self.refLabel)
        self.refLayout.addWidget(self.refPathEdit, 1)
        self.refLayout.addWidget(self.browseBtn)
        self.settingsLayout.addLayout(self.refLayout)
        
        self.refTextLabel = StrongBodyLabel(self.tr("参考音频文本 (可选):"), self.scrollWidget)
        self.settingsLayout.addWidget(self.refTextLabel)
        self.refTextEdit = LineEdit(self.scrollWidget)
        self.refTextEdit.setPlaceholderText(self.tr("输入参考音频的内容 (如果留空则仅使用音色特征)..."))
        self.refTextEdit.setStyleSheet("LineEdit { color: black; }")
        self.settingsLayout.addWidget(self.refTextEdit)
        
        self.mainLayout.addWidget(self.settingsCard)
        
        self.textLabel = StrongBodyLabel(self.tr("输入文本:"), self.scrollWidget)
        self.mainLayout.addWidget(self.textLabel)
        
        self.textEdit = PlainTextEdit(self.scrollWidget)
        self.textEdit.setPlaceholderText(self.tr("请输入要合成的文本..."))
        self.textEdit.setMinimumHeight(150)
        # self.textEdit.setStyleSheet("QTextEdit { color: black; }")
        self.mainLayout.addWidget(self.textEdit)
        
        self.controlsLayout = QHBoxLayout()
        
        self.genBtn = PrimaryPushButton(FIF.MICROPHONE, self.tr("开始克隆"), self.scrollWidget)
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

    def browseAudio(self):
        fname, _ = QFileDialog.getOpenFileName(self, self.tr("选择音频文件"), "", "Audio Files (*.wav *.mp3 *.flac *.ogg)")
        if fname:
            self.ref_audio_path = fname
            self.refPathEdit.setText(fname)

    def startGeneration(self):
        if not self.backend: 
            self.showError(self.tr("后端未连接"))
            return
            
        if not self.ref_audio_path:
            self.showError(self.tr("请先选择参考音频"))
            return

        text = self.textEdit.toPlainText().strip()
        if not text:
            self.showError(self.tr("请输入合成文本"))
            return
            
        ref_text = self.refTextEdit.text().strip()
        if not ref_text:
            ref_text = None
        
        self.genBtn.setEnabled(False)
        self.progressBar.show()
        
        self.generator = CloneGenerator(self.backend, text, self.ref_audio_path, ref_text)
        self.generator.finished.connect(self.onGenerationFinished)
        self.generator.start()

    def onGenerationFinished(self, success, msg, path):
        self.progressBar.hide()
        self.genBtn.setEnabled(True)
        
        if success:
            self.showSuccess(self.tr("克隆成功"))
            self.current_audio_path = path
            self.playBtn.setEnabled(True)
            self.saveBtn.setEnabled(True)
            self.playAudio()
        else:
            self.showError(self.tr("克隆失败: {msg}").format(msg=msg))

    def saveAudio(self):
        if hasattr(self, 'current_audio_path') and self.current_audio_path:
            savePath, _ = QFileDialog.getSaveFileName(self, self.tr("保存音频"), "cloned.wav", "Audio Files (*.wav)")
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
            try:
                self.playBtn.clicked.disconnect()
            except: pass
            self.playBtn.clicked.connect(self.pauseAudio)

    def pauseAudio(self):
        self.player.pause()
        self.volumeSlider.setValue(self.audioOutput.volume())
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
