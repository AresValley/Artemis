import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Item {

    function setLights(aIndex) {
        resetLights()
        if (aIndex >= 0 && aIndex < 8) {
            rect0.color = "#539bff"
        } else if (aIndex >= 8 && aIndex < 16) {
            rect1.color = "#0ccf43"
        } else if (aIndex >= 16 && aIndex < 30) {
            rect2.color = "#f0e000"
        } else if (aIndex >= 30 && aIndex < 50) {
            rect3.color = "#ffb700"
        } else if (aIndex >= 50 && aIndex < 100) {
            rect4.color = "#ff7b00"
        } else if (aIndex >= 100) {
            rect5.color = "#e80000"
        }
    }

    function resetLights() {
        rect0.color = "#2b4d7f"
        rect1.color = "#076823"
        rect2.color = "#797200"
        rect3.color = "#815f00"
        rect4.color = "#814100"
        rect5.color = "#750300"
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            id: rect5
            color: "#750300"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            topLeftRadius: 10
            topRightRadius: 10
            Label {
                text: qsTr("SEVERE STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }

        Rectangle {
            id: rect4
            color: "#814100"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("STRONG STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }

        Rectangle {
            id: rect3
            color: "#815f00"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("MODERATE STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }

        Rectangle {
            id: rect2
            color: "#797200"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("ACTIVE-STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }

        Rectangle {
            id: rect1
            color: "#076823"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("UNSETTLED")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }

        Rectangle {
            id: rect0
            color: "#2b4d7f"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            bottomLeftRadius: 10
            bottomRightRadius: 10
            Label {
                text: qsTr("QUIET")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.2
            }
        }
    }
}
