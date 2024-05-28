import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Item {

    function setLights(kIndex) {
        resetLights()
        if (kIndex === 0) {
            rect0.color = "#539bff"
        } else if (kIndex === 1) {
            rect1.color = "#0ccf43"
        } else if (kIndex === 2) {
            rect2.color = "#0ccf43"
        } else if (kIndex === 3) {
            rect3.color = "#f0e000"
        } else if (kIndex === 4) {
            rect4.color = "#f0e000"
        } else if (kIndex === 5) {
            rect5.color = "#ffb700"
        } else if (kIndex === 6) {
            rect6.color = "#ff7b00"
        } else if (kIndex === 7) {
            rect7.color = "#e80000"
        } else if (kIndex === 8) {
            rect8.color = "#e80000"
        } else if (kIndex === 9) {
            rect9.color = "#e80000"
        }
    }

    function resetLights() {
        rect0.color = "#2b4d7f"
        rect1.color = "#076823"
        rect2.color = "#076823"
        rect3.color = "#797200"
        rect4.color = "#797200"
        rect5.color = "#815f00"
        rect6.color = "#814100"
        rect7.color = "#750300"
        rect8.color = "#750300"
        rect9.color = "#750300"
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            id: rect9
            color: "#750300"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            topLeftRadius: 10
            topRightRadius: 10
            Label {
                text: qsTr("SUPER STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect8
            color: "#750300"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("EXTREME STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect7
            color: "#750300"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("SEVERE STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect6
            color: "#814100"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("MAJOR STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect5
            color: "#815f00"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("MINOR STORM")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect4
            color: "#797200"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("ACTIVE")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect3
            color: "#797200"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("UNSETTLED")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect2
            color: "#076823"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("QUIET")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }

        Rectangle {
            id: rect1
            color: "#076823"
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            Label {
                text: qsTr("VERY QUIET")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
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
                text: qsTr("INACTIVE")
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                font.pixelSize: parent.height*0.3
            }
        }
    }
}
