import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Page {
    id: spaceWeatherDRAP
    anchors.fill: parent

    objectName: "spaceWeatherDRAPObj"

    function loadDrapReport(poseidon_data) {
        labelRecovery.text = poseidon_data['DRAP']['Recovery Time']
        labelXrayMsg.text = poseidon_data['DRAP']['XRay Msg']
        labelProtonMsg.text = poseidon_data['DRAP']['Proton Msg']

        checkUrlExists("https://www.aresvalley.com/poseidon_engine/drap.png", function(exists) {
            if (exists) {
                imageBox.source = "https://www.aresvalley.com/poseidon_engine/drap.png"
            } else {
                imageBox.source = "qrc:///images/artemis_not_available.svg"
            }
        })
    }

    function checkUrlExists(url, callback) {
        var xhr = new XMLHttpRequest()
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                callback(xhr.status === 200)
            }
        }
        xhr.open("HEAD", url, true)
        xhr.send()
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10

        Image {
            id: imageBox
            Layout.fillHeight: true
            Layout.fillWidth: true
            fillMode: Image.PreserveAspectFit

        }

        RowLayout {
            Item {
                Layout.fillWidth: true
            }
            Label {
                text: qsTr("RECOVERY TIME:")
                Layout.fillWidth: false
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            Label {
                id: labelRecovery
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                font.pointSize: 12
                font.bold: true
            }
            Item {
                Layout.fillWidth: true
            }
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.fillWidth: true

            ColumnLayout {
                Label {
                    text: qsTr("X-RAY STATUS")
                }
                Label {
                    id: labelXrayMsg
                    font.pointSize: 12
                    font.bold: true
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Label {
                    text: qsTr("PROTON STATUS")
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
                Label {
                    id: labelProtonMsg
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    font.pointSize: 12
                    font.bold: true
                }
            }
        }
    }
}
