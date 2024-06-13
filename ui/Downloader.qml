import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Window {
    id: windowDownloader

    width: 400
    height: 130

    maximumHeight: height
    maximumWidth: width

    minimumHeight: height
    minimumWidth: width

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    title: qsTr("Artemis - Downloader")

    signal onAbort()

    onClosing: {
        onAbort()
    }

    function updateProgressBar(bytesReceived, bytesTotal) {
        progressBar.value = bytesReceived
        progressBar.to = bytesTotal
    }

    function setIndeterminateBar() {
        progressBar.indeterminate = true
    }

    function updateStatus(arg) {
        progressLabel.text = arg
    }

    Page {
        id: page
        anchors.fill: parent

        ColumnLayout {
            id: columnLayout
            anchors.fill: parent

            Label {
                text: qsTr("Downloading in progress...")
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            ProgressBar {
                id: progressBar
                Layout.rightMargin: 20
                Layout.leftMargin: 20
                Layout.fillWidth: true
                indeterminate: false
                value: 0
                to: 0
            }

            Label {
                id: progressLabel
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            Button {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                text: qsTr("Abort")
                icon.source: "qrc:/images/icons/abort.svg"
                display: AbstractButton.TextBesideIcon
                flat: true
                onClicked: { onAbort() }
            }
        }
    }
}
