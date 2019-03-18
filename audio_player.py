import os
import sys
from pydub import AudioSegment
from pygame import mixer
from PyQt5.QtCore import QTimer, QTimer, pyqtSlot, QObject

import constants
import qtawesome as qta


class AudioPlayer(QObject): # Maybe useless inheriting from QObject
    """
    This is the audio player widget. The only public methods are the __init__
    method and set_audio_player, which loads the current file. Everything else
    is managed internally.
    """

    __time_step = 500 # Milliseconds.

    def __init__(self, play, pause, stop, volume, audio_progress, active_color, inactive_color):
        super().__init__()
        self.__paused = False
        self.__first_call = True
        self.__play = play
        self.__pause = pause
        self.__stop = stop
        self.__volume = volume
        self.__audio_progress = audio_progress
        self.__audio_file = None
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__update_bar)
        self.__play.clicked.connect(self.__play_audio)
        self.__pause.clicked.connect(self.__pause_audio)
        self.__stop.clicked.connect(self.__stop_audio)
        self.__volume.valueChanged.connect(self.__set_volume)
        self.__play.setIconSize(self.__play.size())
        self.__pause.setIconSize(self.__pause.size())
        self.__stop.setIconSize(self.__stop.size())
        self.refresh_btns_colors(active_color, inactive_color)

    def refresh_btns_colors(self, active_color, inactive_color):
        self.__play.setIcon(qta.icon('fa5.play-circle',
                                     color = active_color,
                                     color_disabled = inactive_color))
        self.__pause.setIcon(qta.icon('fa5.pause-circle',
                                      color = active_color,
                                      color_disabled = inactive_color))
        self.__stop.setIcon(qta.icon('fa5.stop-circle',
                                     color = active_color,
                                     color_disabled = inactive_color))

    @pyqtSlot()
    def __set_volume(self):
        if mixer.get_init():
            mixer.music.set_volume(self.__volume.value() / self.__volume.maximum())

    def __reset_audio_widget(self):
        if mixer.get_init():
            if mixer.music.get_busy():
                mixer.music.stop()
                self.__timer.stop()
            mixer.quit()
        self.__audio_progress.reset()
        self.__enable_buttons(False, False, False)
        self.__paused = False

    @pyqtSlot()
    def __update_bar(self):
        pos = mixer.music.get_pos()
        if pos == -1:
            self.__timer.stop()
            self.__audio_progress.reset()
            self.__enable_buttons(True, False, False)
        else:
            self.__audio_progress.setValue(pos)

    def __set_max_progress_bar(self):
        self.__audio_progress.setMaximum(
            mixer.Sound(self.__audio_file).get_length() * 1000
        )

    def set_audio_player(self, fname = ""):
        self.__first_call = True
        self.__reset_audio_widget()
        full_name = os.path.join(constants.DATA_FOLDER, constants.AUDIO_FOLDER, fname + '.ogg')
        if os.path.exists(full_name):
            self.__play.setEnabled(True)
            self.__audio_file = full_name

    @pyqtSlot()
    def __play_audio(self):
        if not self.__paused:
            if self.__first_call:
                self.__first_call = False
                mixer.init(frequency = AudioSegment.from_ogg(self.__audio_file).frame_rate,
                           buffer = 2048)
                mixer.music.load(self.__audio_file)
                self.__set_volume()
                self.__set_max_progress_bar()
            mixer.music.play()
        else:
            mixer.music.unpause()
            self.__paused = False
        self.__timer.start(self.__time_step)
        self.__enable_buttons(False, True, True)

    @pyqtSlot()
    def __stop_audio(self):
        mixer.music.stop()
        self.__audio_progress.reset()
        self.__timer.stop()
        self.__enable_buttons(True, False, False)

    @pyqtSlot()
    def __pause_audio(self):
        mixer.music.pause()
        self.__timer.stop()
        self.__paused = True
        self.__enable_buttons(True, False, False)

    def __enable_buttons(self, play_en, pause_en, stop_en):
        self.__play.setEnabled(play_en)
        self.__pause.setEnabled(pause_en)
        self.__stop.setEnabled(stop_en)
