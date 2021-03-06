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
        self.setGeometry(350, 100, 800, 600)
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
        self.timeSlider.setEnabled(False)
        self.timeSlider.sliderMoved.connect(self.set_position)

        # Create current and total time labels
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.currentTimeLabel.setText("00:00")
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.totalTimeLabel.setText("00:00")


        # Create volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0,100)
        self.volumeSlider.setValue(80)
        self.volumeSlider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.volumeSlider.setEnabled(False)
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

        # set the time labels to another hbox layout
        hboxLayout2 = QHBoxLayout()
        hboxLayout2.setContentsMargins(0,0,0,0)
        hboxLayout2.addWidget(self.currentTimeLabel)
        hboxLayout2.addWidget(self.timeSlider)
        hboxLayout2.addWidget(self.totalTimeLabel)

        # Create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videoWidget)
        vboxLayout.addLayout(hboxLayout2)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)

        # Media player signals
        # self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.time_position_changed)
        self.mediaPlayer.durationChanged.connect(self.time_duration_changed)


    def open_file(self):
        # Opening the file using the file dialog and qurl
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
            self.timeSlider.setEnabled(True)
            self.volumeSlider.setEnabled(True)
            
            # When the file dialog is opened the video starts to play automatically
            self.play_video()


    def play_video(self):
        # Changing the state of the playback when the play/pause button is pressed
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:

            # Setting the icon of the play/pause button and pausing the playback
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.mediaPlayer.pause()

        else:

            # Setting the icon of the play/pause button, 
            # the volume of the player and starting the playback
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.mediaPlayer.setVolume(80)
            self.mediaPlayer.play()


    def stop_video(self):
        # Disabling all the sliders and buttons except the openVideo button
        self.playBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        self.timeSlider.setEnabled(False)
        self.volumeSlider.setEnabled(False)

        # Stopping the playback
        self.mediaPlayer.stop()


    def time_position_changed(self, position):

        # Setting the value of the time slider and currentTimeLabel 
        self.timeSlider.setValue(position)
        self.currentTimeLabel.setText(time_format(position))


    def time_duration_changed(self, duration):

        # Setting the range of time slider and the value of totalTimeLabel 
        self.timeSlider.setRange(0, duration)
        self.totalTimeLabel.setText(time_format(duration))


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    
    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText(f"Error: {self.mediaPlayer.errorString()}")



def time_format(ms):
    # Converting the input to the standard time format
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))



app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
