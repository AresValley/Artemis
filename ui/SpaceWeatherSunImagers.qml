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
                ListElement { text: "94 Å - Atmospheric Imagery Assembly"; value: "AIA_094" }
                ListElement { text: "131 Å - Atmospheric Imagery Assembly"; value: "AIA_131" }
                ListElement { text: "171 Å - Atmospheric Imagery Assembly"; value: "AIA_171" }
                ListElement { text: "193 Å - Atmospheric Imagery Assembly"; value: "AIA_193" }
                ListElement { text: "303 Å - Atmospheric Imagery Assembly"; value: "AIA_304" }
                ListElement { text: "335 Å - Atmospheric Imagery Assembly"; value: "AIA_335" }
                ListElement { text: "1600 Å - Atmospheric Imagery Assembly"; value: "AIA_1600" }
                ListElement { text: "1700 Å - Atmospheric Imagery Assembly"; value: "AIA_1700" }
                ListElement { text: "Magnetogram - Helioseismic and Magnetic Imager"; value: "AIA_MAGN" }
                ListElement { text: "Intensitygram - Helioseismic and Magnetic Imager"; value: "AIA_INTE" }
                ListElement { text: "Dopplergram - Helioseismic and Magnetic Imager"; value: "AIA_DOPP" }
                ListElement { text: "LASCO C2 - Large Angle and Spectrometric Coronagraph"; value: "LASCO_C2" }
                ListElement { text: "LASCO C3 - Large Angle and Spectrometric Coronagraph"; value: "LASCO_C3" }
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
