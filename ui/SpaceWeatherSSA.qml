import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Page {
    id: spaceWeatherSSA
    anchors.fill: parent

    objectName: "spaceWeatherSSA"

    function loadDrapReport(poseidon_data) {
        checkUrlExists(poseidon_data['URL']['SYNOPTIC_MAP'], function(exists) {
            if (exists) {
                imageBox.source = poseidon_data['URL']['SYNOPTIC_MAP']
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
    }
}
