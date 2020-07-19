from PyQt5.QtWidgets import QApplication,QStackedLayout, QWidget, QPushButton,QCheckBox, QHBoxLayout \
    , QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog \
        , QSpacerItem, QMenu, QMenuBar, QAction, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QRect, QTextStream, QFile
import sys
import xlrd
from xlrd import open_workbook
from BreezeStyleSheets import breeze_resources



class NewDialog(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Tags List")
        N = len(main_window.time)
        self.setGeometry(350, 100, 200, N*10)
        layout = QVBoxLayout()
        self.buttons=[QPushButton() for i in range(N)]
        set_d = [50*i for i in range(N)]

        for i in range(len(main_window.subject)):
            self.buttons[i].setText(main_window.subject[i])

        for i in range(N): # setting each button to its corresponding function
            x = self.buttons[i]
            y=int(main_window.time[i])
            x.clicked.connect((lambda y: lambda: self.go_to(y))(y))
            layout.addWidget(x)
        
        self.setLayout(layout)

    def go_to(self, time): #last version edit
        self.main_window.mediaPlayer.setPosition(1000*time)
        self.close()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = True
        self.setWindowTitle("Advanced Programming Player")
        self.setGeometry(350, 100, 800, 600)
        self.setWindowIcon(QIcon("player.png"))
        ############
        # SIAVASH
        ############
        # self.palette = self.palette()
        # self.palette.setColor(QPalette.Window, QColor('lavenderblush'))#(142, 145, 20))
        # self.setPalette(self.palette)
        ############

        file = QFile(":/light.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())

        self.time=[]
        self.subject=[]
        self.init_ui()
        self.show()


    def init_ui(self):
        self.flag = True
        # Create Media Player Object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    
        # Create video widget object
        videoWidget = QVideoWidget()   #difference between media player and widget object

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


        
        #Creating button for getting tags
        self.tagBtn=QPushButton("Import tags")
        self.tagBtn.setEnabled(True)
        self.tagBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.tagBtn.clicked.connect(self.getTags)

        #Create button for changing theme
        self.tmBtn=QPushButton('Dark')
        self.tmBtn.setEnabled(True)
        self.tmBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.tmBtn.clicked.connect(self.set_theme)

        #Create button for playback speed #New
        self.pbkBtn= QCheckBox("2X")
        self.pbkBtn.setChecked(False)
        self.pbkBtn.toggled.connect(self.set_rate) 

        #Creat button for switching the window #New
        self.btn_switch=QPushButton("Tags")
        self.btn_switch.clicked.connect(self.switch_window)
        
        # Create time slider
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setRange(0,100)
        self.timeSlider.setEnabled(False)
        self.timeSlider.sliderMoved.connect(self.set_position)

        # Create current and total time labels
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.currentTimeLabel.setText("<font color='black'>00:00")
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
        hboxLayout.addWidget(self.tagBtn)
        hboxLayout.addWidget(self.tmBtn)
        hboxLayout.addWidget(self.btn_switch)
        hboxLayout.addWidget(self.pbkBtn)
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
        #self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
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

    def time_position_changed(self,position):

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

    def getTags(self): # Opens the excel file and stores time and subject
        filename, _ = QFileDialog.getOpenFileName(self)
        wb = open_workbook(filename)

        for s in wb.sheets():
            values = []
            for row in range(s.nrows):
                for col in range(s.ncols):
                    values.append(s.cell(row,col).value)

        self.time =[values[i] for i in range(len(values)) if i%2==0] #storing time in time list
        self.subject=[values[i] for i in range(len(values)) if i%2!=0] #storing corresponding subjects in subject list
        #print(self.time)    #just for verification     
        #print(self.subject) #just for verification purpose

    def set_theme(self):
        if not self.flag:
            # self.palette.setColor(QPalette.Window, QColor('lavenderblush'))
            # self.palette.setColor(QPalette.Button, QColor('lightsalmon'))
            file = QFile(":/light.qss")
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            self.tmBtn.setText("Dark")
        else:
            # self.palette.setColor(QPalette.Window, QColor('gray'))
            # self.palette.setColor(QPalette.Button, QColor('darkgray'))
            file = QFile(":/dark.qss")
            file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
            self.tmBtn.setText("Light")
        # self.setPalette(self.palette)
        self.flag = not self.flag
    
    def set_rate(self): # sometimes it becomes laggy ---#New
        if self.pbkBtn.isChecked():
            self.mediaPlayer.setPlaybackRate(2)
        if not self.pbkBtn.isChecked():
            self.mediaPlayer.setPlaybackRate(1)
    
    def switch_window(self): #New/last version edit
        self.tag_window = NewDialog(self)
        self.tag_window.show()
    
    #def handleButton(self): #last version edit
        #self.go_to(eval(self.time[3]))
        
  
            
            
        

def time_format(ms):
    # Converting the input to the standard time format
    s = round(ms / 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = Window()
sys.exit(app.exec_())