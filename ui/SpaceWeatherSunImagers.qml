import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Page {
    id: spaceWeatherSunImagers
    anchors.fill: parent

    objectName: "spaceWeatherSunImagers"

    property var poseidon_json

    function loadDrapReport(poseidon_data) {
        poseidon_json = poseidon_data
        loadImage(poseidon_json['URL'][comboBoxImageProduct.currentValue.value])
    }

    function loadImage(url) {
        checkUrlExists(url, function(exists) {
            if (exists) {
                imageBox.source = url
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

        ComboBox {
            id: comboBoxImageProduct
            textRole: 'text'
            Layout.fillWidth: true
            model:  ListModel {
                ListElement { text: "SUVI 94 Å"; value: "SUVI_094" }
                ListElement { text: "SUVI 131 Å"; value: "SUVI_131" }
                ListElement { text: "SUVI 171 Å"; value: "SUVI_171" }
                ListElement { text: "SUVI 195 Å"; value: "SUVI_195" }
                ListElement { text: "SUVI 284 Å"; value: "SUVI_284" }
                ListElement { text: "SUVI 304 Å"; value: "SUVI_304" }
                ListElement { text: "LASCO C2"; value: "LASCO_C2" }
                ListElement { text: "LASCO C3"; value: "LASCO_C3" }
                ListElement { text: "Thematic Map"; value: "SUVI_THEMATIC" }
            }
            onActivated: {
                loadImage(poseidon_json['URL'][comboBoxImageProduct.currentValue.value])
            }
        }

        Image {
            id: imageBox
            Layout.fillHeight: true
            Layout.fillWidth: true
            fillMode: Image.PreserveAspectFit

        }
    }
}
