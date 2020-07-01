from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout \
    , QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog \
        , QSpacerItem, QMenu, QMenuBar, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QRect
import sys


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AP Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon("player.png"))

        self.init_ui()
        self.show()


    def init_ui(self):
        # Create Media Player Object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    
        # Create video widget object
        videoWidget = QVideoWidget()

        # Create open button
        openBtn = QPushButton("Open Video")
        openBtn.clicked.connect(self.open_file)

        # Create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.playBtn.clicked.connect(self.play_video)

        # Create button for stopping the playback
        self.stopBtn = QPushButton()
        self.stopBtn.setEnabled(False)
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop_video)

        # Create time slider
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setRange(0,100)
        self.timeSlider.sliderMoved.connect(self.set_position)

        # Create volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0,100)
        self.volumeSlider.setValue(80)
        self.volumeSlider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.volumeSlider.sliderMoved.connect(self.set_volume)

        # Create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)

        # Create spacer item 
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        labelImage = QLabel(self)
        pixmap = QPixmap("volume.png")
        labelImage.setPixmap(pixmap)
        
        # set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.stopBtn)
        hboxLayout.addSpacerItem(self.spacerItem)
        hboxLayout.addWidget(labelImage)
        hboxLayout.addWidget(self.volumeSlider)

        # Create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videoWidget)
        vboxLayout.addWidget(self.timeSlider)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.time_position_changed)
        self.mediaPlayer.durationChanged.connect(self.time_duration_changed)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.play_video()


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()


    def stop_video(self):
        self.mediaPlayer.stop()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def time_position_changed(self, position):
        self.timeSlider.setValue(position)


    def time_duration_changed(self, duration):
        self.timeSlider.setRange(0, duration)


    def volume_position_changed(self, position):
        self.volumeSlider.setRange(position)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    
    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText(f"Error: {self.mediaPlayer.errorString()}")



app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
