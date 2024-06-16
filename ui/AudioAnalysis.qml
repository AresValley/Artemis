import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs


Window {
    id: window
    width: 1100
    height: 800

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    title: qsTr("Artemis - Audio Analysis")

    modality: Qt.ApplicationModal
    flags: Qt.Window

    // Windows without upper bar
    //flags: Qt.FramelessWindowHint

}
