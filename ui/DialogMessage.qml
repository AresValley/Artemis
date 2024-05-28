import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Window


Dialog {
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    modal: true
    closePolicy: Popup.NoAutoClose

    property string message
    property string messageType

    RowLayout {
        Layout.fillWidth: true
        spacing: 10

        Image {
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            sourceSize.height: 60
            sourceSize.width: 60

            source: {
                switch (messageType.toLowerCase()) {
                case "question":
                    return "qrc:///images/icons/dialog_quest.svg"
                case "warn":
                    return "qrc:///images/icons/dialog_warn.svg"
                case "error":
                    return "qrc:///images/icons/dialog_error.svg"
                case "info":
                    return "qrc:///images/icons/dialog_info.svg"
                default:
                    return "qrc:///images/icons/dialog_info.svg"
                }
            }
        }

        Label {
            text: message

            Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
            Layout.fillWidth: true
            Layout.minimumWidth: 200
            Layout.maximumWidth: 300

            textFormat: Text.RichText
            wrapMode: Text.WordWrap
        }
    }
}
