import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Page {
    id: spaceWeatherAurora
    anchors.fill: parent

    objectName: "spaceWeatherAuroraObj"

    function loadAuroraReport() {
        checkUrlExists("https://www.aresvalley.com/poseidon_engine/aurora.png", function(exists) {
            if (exists) {
                imageBox.source = "https://www.aresvalley.com/poseidon_engine/aurora.png"
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
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.bottomMargin: 20
        anchors.topMargin: 20

        Image {
            id: imageBox
            Layout.fillHeight: true
            Layout.fillWidth: true
            fillMode: Image.PreserveAspectFit
        }
    }
}
