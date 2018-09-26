import os
import sys
                             
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class AudioPlayer(object):
    def __init__(self, play, pause, stop, volume, audio_progress):
        self.play = play
        self.pause = pause
        self.stop = stop
        self.volume = volume
        self.audio_progress = audio_progress
        self.audio_file = None
        self.player = QMediaPlayer()
        self.player.setVolume(51)
        self.player.durationChanged.connect(self.set_max_progress_bar)
        self.player.positionChanged.connect(self.set_progress_bar)
        self.play.clicked.connect(self.audio)
        self.pause.clicked.connect(self.pause_audio)
        self.stop.clicked.connect(self.stop_audio)
        self.player.stateChanged.connect(self.reset_audio_widget)
        self.volume.valueChanged.connect(self.set_volume)

    def set_volume(self):
        self.player.setVolume(self.volume.value())

    def reset_audio_widget(self):
        if self.player.state() == QMediaPlayer.StoppedState:
            self.audio_progress.setValue(0)
            self.volume.setValue(51)
            self.pause.setEnabled(False)
            self.stop.setEnabled(False)

    def set_max_progress_bar(self):
        print(self.player.duration())
        self.audio_progress.setMaximum(self.player.duration())

    def set_progress_bar(self):
        print(self.player.position())
        self.audio_progress.setValue(self.player.position())

    def set_media_player(self):
        self.player.setMedia(QMediaContent(self.audio_file))

    def set_audio_player(self, fname):
        self.reset_audio_widget()
        self.play.setEnabled(False)
        full_name = os.path.join('Data', 'Audio', fname + '.mp3')
        if QFileInfo(full_name).exists():
            print('exists')
            self.play.setEnabled(True)
            self.audio_file = QUrl.fromLocalFile(full_name)
            self.set_media_player()
        else:
            print('not exists')

    def audio(self):
        self.player.play()
        self.stop.setEnabled(True)
        self.pause.setEnabled(True)

    def stop_audio(self):
        self.player.stop()

    def pause_audio(self):
        self.player.pause()
