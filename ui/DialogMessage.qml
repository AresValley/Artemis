import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

Dialog {
    id: root
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    modal: true
    closePolicy: Popup.NoAutoClose

    property string message: ""
    property string messageType: ""
    property string dialogTitle: "" 

    width: 440

    padding: 16

    RowLayout {
        anchors.fill: parent
        spacing: 16

        Image {
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            Layout.preferredWidth: 48
            Layout.preferredHeight: 48
            sourceSize.width: 48
            sourceSize.height: 48

            source: {
                switch (messageType.toLowerCase()) {
                case "question":
                    return "qrc:///data/images/icons/dialog_quest.svg"
                case "warn":
                    return "qrc:///data/images/icons/dialog_warn.svg"
                case "error":
                    return "qrc:///data/images/icons/dialog_error.svg"
                case "info":
                default:
                    return "qrc:///data/images/icons/dialog_info.svg"
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop

            Label {
                text: root.dialogTitle
                font.pixelSize: 16
                font.bold: true
                color: Material.foreground
                visible: text !== ""
                Layout.fillWidth: true
                wrapMode: Text.Wrap
            }

            TextArea {
                text: root.message
                textFormat: Text.RichText
                wrapMode: Text.Wrap

                readOnly: true
                selectByMouse: true
                background: null 

                font.pixelSize: 14
                color: Material.foreground

                Layout.fillWidth: true
                topPadding: 0
                bottomPadding: 0
                leftPadding: 0
                rightPadding: 0
            }
        }
    }
}
