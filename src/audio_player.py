import os
from pygame import mixer
from PyQt5.QtCore import QTimer, pyqtSlot, QObject

from constants import Constants
import qtawesome as qta


class AudioPlayer(QObject):
    """Subclass QObject. Audio player widget for the audio samples.

    The only public methods are the __init__
    method, set_audio_player, which loads the current file and refresh_btns_colors.
    Everything else is managed internally."""

    _TIME_STEP = 500  # Milliseconds.

    def __init__(self, play,
                 pause,
                 stop,
                 volume,
                 audio_progress,
                 active_color,
                 inactive_color):
        """Initialize the player."""
        super().__init__()
        self._paused = False
        self._first_call = True
        self._play = play
        self._pause = pause
        self._stop = stop
        self._volume = volume
        self._audio_progress = audio_progress
        self._audio_file = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_bar)
        self._play.clicked.connect(self._play_audio)
        self._pause.clicked.connect(self._pause_audio)
        self._stop.clicked.connect(self._stop_audio)
        self._volume.valueChanged.connect(self._set_volume)
        self._play.setIconSize(self._play.size())
        self._pause.setIconSize(self._pause.size())
        self._stop.setIconSize(self._stop.size())
        self.refresh_btns_colors(active_color, inactive_color)

    def refresh_btns_colors(self, active_color, inactive_color):
        """Repaint the buttons of the widgetd after the theme has changed."""
        self._play.setIcon(qta.icon('fa5.play-circle',
                                    color=active_color,
                                    color_disabled=inactive_color))
        self._pause.setIcon(qta.icon('fa5.pause-circle',
                                     color=active_color,
                                     color_disabled=inactive_color))
        self._stop.setIcon(qta.icon('fa5.stop-circle',
                                    color=active_color,
                                    color_disabled=inactive_color))

    @pyqtSlot()
    def _set_volume(self):
        """Set the volume of the audio samples."""
        if mixer.get_init():
            mixer.music.set_volume(
                self._volume.value() / self._volume.maximum()
            )

    def _reset_audio_widget(self):
        """Reset the widget. Stop all playing samples."""
        if mixer.get_init():
            if mixer.music.get_busy():
                mixer.music.stop()
                self._timer.stop()
            mixer.quit()
        self._audio_progress.reset()
        self._enable_buttons(False, False, False)
        self._paused = False

    @pyqtSlot()
    def _update_bar(self):
        """Update the progress bar."""
        pos = mixer.music.get_pos()
        if pos == -1:
            self._timer.stop()
            self._audio_progress.reset()
            self._enable_buttons(True, False, False)
        else:
            self._audio_progress.setValue(pos)

    def _set_max_progress_bar(self):
        """Set the maximum value of the progress bar."""
        self._audio_progress.setMaximum(
            mixer.Sound(self._audio_file).get_length() * 1000
        )

    def set_audio_player(self, fname=""):
        """Set the current audio sample."""
        self._first_call = True
        self._reset_audio_widget()
        full_name = os.path.join(
            Constants.DATA_FOLDER,
            Constants.AUDIO_FOLDER,
            fname + '.ogg'
        )
        if os.path.exists(full_name):
            self._play.setEnabled(True)
            self._audio_file = full_name

    @pyqtSlot()
    def _play_audio(self):
        """Play the audio sample."""
        if not self._paused:
            if self._first_call:
                self._first_call = False
                mixer.init(48000, -16, 1, 1024)
                mixer.music.load(self._audio_file)
                self._set_volume()
                self._set_max_progress_bar()
            mixer.music.play()
        else:
            mixer.music.unpause()
            self._paused = False
        self._timer.start(self._TIME_STEP)
        self._enable_buttons(False, True, True)

    @pyqtSlot()
    def _stop_audio(self):
        """Stop the audio sample."""
        mixer.music.stop()
        self._audio_progress.reset()
        self._timer.stop()
        self._enable_buttons(True, False, False)

    @pyqtSlot()
    def _pause_audio(self):
        """Pause the audio sample."""
        mixer.music.pause()
        self._timer.stop()
        self._paused = True
        self._enable_buttons(True, False, False)

    def _enable_buttons(self, play_en, pause_en, stop_en):
        """Set the three buttons status."""
        self._play.setEnabled(play_en)
        self._pause.setEnabled(pause_en)
        self._stop.setEnabled(stop_en)
