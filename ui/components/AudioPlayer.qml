import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtMultimedia


Item {
    width: 200
    height: 80

    property bool loop: false

    function loadSound(audio_path) {
        player.stop()
        player.source = audio_path
        buttonPlay.icon.color = Material.accent
        buttonPlay.enabled = true
        buttonLoop.enabled = true
    }

    function playSound() {
        buttonPlay.icon.color = Material.foreground
        buttonPause.icon.color = Material.accent
        buttonStop.icon.color = Material.accent
        buttonPlay.enabled = false
        buttonPause.enabled = true
        buttonStop.enabled = true
        buttonLoop.enabled = true
        playerPosition.enabled = player.seekable
        player.play()
    }

    function pauseSound() {
        buttonPlay.icon.color = Material.accent
        buttonPause.icon.color = Material.foreground
        buttonPlay.enabled = true
        buttonPause.enabled = false
        player.pause()
    }

    function stopSound() {
        buttonPlay.icon.color = Material.accent
        buttonPause.icon.color = Material.foreground
        buttonStop.icon.color = Material.foreground
        buttonLoop.icon.color = Material.foreground
        buttonPlay.enabled = true
        buttonPause.enabled = false
        buttonStop.enabled = false
        buttonLoop.enabled = false
        loop = false
        player.stop()
    }

    function resetPlayer() {
        player.stop()
        player.source = ''
        loop = false
        buttonPlay.icon.color = Material.foreground
        buttonPause.icon.color = Material.foreground
        buttonStop.icon.color = Material.foreground
        buttonLoop.icon.color = Material.foreground
        buttonPlay.enabled = false
        buttonPause.enabled = false
        buttonStop.enabled = false
        buttonLoop.enabled = false
        playerPosition.enabled = false
    }

    ColumnLayout {
        RowLayout {
            spacing: 0
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            RoundButton {
                id: buttonPlay
                icon.color: Material.foreground
                icon.source: "qrc:/images/icons/player_play.svg"
                display: AbstractButton.IconOnly
                enabled: false
                flat: true
                onClicked: playSound()
            }

            RoundButton {
                id: buttonPause
                icon.color: Material.foreground
                icon.source: "qrc:/images/icons/player_pause.svg"
                display: AbstractButton.IconOnly
                enabled: false
                flat: true
                onClicked: pauseSound()
            }

            RoundButton {
                id: buttonStop
                icon.color: Material.foreground
                icon.source: "qrc:/images/icons/player_stop.svg"
                display: AbstractButton.IconOnly
                enabled: false
                flat: true
                onClicked: stopSound()
            }

            RoundButton {
                id: buttonLoop
                icon.color: Material.foreground
                icon.source: "qrc:/images/icons/player_loop.svg"
                display: AbstractButton.IconOnly
                enabled: false
                flat: true
                onClicked: {
                    if (loop) {
                        loop = false
                        icon.color = Material.foreground
                    } else {
                        loop = true
                        icon.color = Material.accent
                    }
                }
            }
        }

        Slider {
            id: playerPosition
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.preferredHeight: 20
            enabled: player.seekable
            value: player.duration > 0 ? player.position / player.duration : 0
            onMoved: {
                player.position = player.duration * playerPosition.position
            }
        }

        MediaPlayer {
            id: player
            audioOutput: audioOutput

            onPlaybackStateChanged: {
                if (player.playbackState === MediaPlayer.StoppedState) {
                    if (loop) {
                        playSound()
                    } else {
                        stopSound()
                    }
                }
            }
        }

        AudioOutput {
            id: audioOutput
            //volume: volumeSlider.value
        }
    }
}
