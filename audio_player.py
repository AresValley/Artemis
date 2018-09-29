import os
import sys
from pydub import AudioSegment
from pygame import mixer
from PyQt5.QtCore import QTimer, QTimer
import qtawesome as qta


class AudioPlayer(object):
    """
    This is the audio player widget. The only public methods are the __init__
    method and set_audio_player, which loads the current file. Everything else
    is managed internally.
    """

    __time_step = 500 # Milliseconds.
    __delay_load_audio = 250 # Milliseconds

    def __init__(self, play, pause, stop, volume, audio_progress):
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
        self.__play.setIcon(qta.icon('fa5.play-circle',
                                   color = "#4facf1",
                                   color_disabled = '#7a7a7a'))
        self.__play.setIconSize(self.__play.size())
        self.__pause.setIcon(qta.icon('fa5.pause-circle',
                                    color = "#4facf1",
                                    color_disabled = '#7a7a7a'))
        self.__pause.setIconSize(self.__pause.size())
        self.__stop.setIcon(qta.icon('fa5.stop-circle',
                                   color = "#4facf1",
                                   color_disabled = '#7a7a7a'))
        self.__stop.setIconSize(self.__stop.size())

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
<<<<<<< HEAD
        if self.__load_timer.isActive():
            self.__load_timer.stop()
        self.fname = fname
        self.__load_timer.start(self.__delay_load_audio)

    def __set_audio_player(self):
        self.__load_timer.stop()
=======
        self.__first_call = True
>>>>>>> load_sound_on_request
        self.__reset_audio_widget()
        full_name = os.path.join('Data', 'Audio_wav', fname + '.wav')
        if os.path.exists(full_name):
<<<<<<< HEAD
            mixer.init(frequency = AudioSegment.from_wav(full_name).frame_rate)
=======
>>>>>>> load_sound_on_request
            self.__play.setEnabled(True)
            self.__audio_file = full_name

    def __play_audio(self):
        if not self.__paused:
            if self.__first_call:
                self.__first_call = False
                mixer.init(frequency = AudioSegment.from_wav(self.__audio_file).frame_rate,
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

    def __stop_audio(self):
        mixer.music.stop()
        self.__audio_progress.reset()
        self.__timer.stop()
        self.__enable_buttons(True, False, False)

    def __pause_audio(self):
        mixer.music.pause()
        self.__timer.stop()
        self.__paused = True
        self.__enable_buttons(True, False, False)

    def __enable_buttons(self, play_en, pause_en, stop_en):
        self.__play.setEnabled(play_en)
        self.__pause.setEnabled(pause_en)
        self.__stop.setEnabled(stop_en)
