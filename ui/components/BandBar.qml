import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material

Item {
    width: 400
    height: 20

    function setBandBar(lof, upf) {
        resetBandBar()

        if (lof < 30) {
            selector.anchors.left = rectangleELF.left
        } else if (lof >= 30 && lof < 300) {
            selector.anchors.left = rectangleSLF.left
        } else if (lof >= 300 && lof < 3000) {
            selector.anchors.left = rectangleULF.left
        } else if (lof >= 3000 && lof < 30000) {
            selector.anchors.left = rectangleVLF.left
        } else if (lof >= 30000 && lof < 300000) {
            selector.anchors.left = rectangleLF.left
        } else if (lof >= 300000 && lof < 3000000) {
            selector.anchors.left = rectangleMF.left
        } else if (lof >= 3000000 && lof < 30000000) {
            selector.anchors.left = rectangleHF.left
        } else if (lof >= 30000000 && lof < 300000000) {
            selector.anchors.left = rectangleVHF.left
        } else if (lof >= 300000000 && lof < 3000000000) {
            selector.anchors.left = rectangleUHF.left
        } else if (lof >= 3000000000 && lof < 30000000000) {
            selector.anchors.left = rectangleSHF.left
        } else if (lof >= 30000000000 && lof < 300000000000) {
            selector.anchors.left = rectangleEHF.left
        }

        if (upf < 30) {
            selector.anchors.right = rectangleELF.right
        } else if (upf >= 30 && upf < 300) {
            selector.anchors.right = rectangleSLF.right
        } else if (upf >= 300 && upf < 3000) {
            selector.anchors.right = rectangleULF.right
        } else if (upf >= 3000 && upf < 30000) {
            selector.anchors.right = rectangleVLF.right
        } else if (upf >= 30000 && upf < 300000) {
            selector.anchors.right = rectangleLF.right
        } else if (upf >= 300000 && upf < 3000000) {
            selector.anchors.right = rectangleMF.right
        } else if (upf >= 3000000 && upf < 30000000) {
            selector.anchors.right = rectangleHF.right
        } else if (upf >= 30000000 && upf < 300000000) {
            selector.anchors.right = rectangleVHF.right
        } else if (upf >= 300000000 && upf < 3000000000) {
            selector.anchors.right = rectangleUHF.right
        } else if (upf >= 3000000000 && upf < 30000000000) {
            selector.anchors.right = rectangleSHF.right
        } else if (upf >= 30000000000 && upf < 300000000000) {
            selector.anchors.right = rectangleEHF.right
        }
    }

    function resetBandBar() {
        selector.anchors.left = container.left
        selector.anchors.right = container.left
    }

    Rectangle {
        id: container
        radius: 13
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0
                color: "#1a000000"
            }
            GradientStop {
                position: 0.5
                color: "#26000000"
            }
            GradientStop {
                position: 1
                color: "#1a000000"
            }
        }

        Rectangle {
            id: rectangleELF
            width: parent.width/11
            anchors.left: parent.left
            anchors.right: rectangleSLF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("ELF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleSLF
            width: parent.width/11
            anchors.right: rectangleULF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("SLF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleULF
            width: parent.width/11
            anchors.right: rectangleVLF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("ULF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleVLF
            width: parent.width/11
            anchors.right: rectangleLF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("VLF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleLF
            width: parent.width/11
            anchors.right: rectangleMF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("LF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleMF
            width: parent.width/11
            anchors.right: rectangleHF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("MF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleHF
            width: parent.width/11
            anchors.right: rectangleVHF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("HF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleVHF
            width: parent.width/11
            anchors.right: rectangleUHF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("VHF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleUHF
            width: parent.width/11
            anchors.right: rectangleSHF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("UHF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleSHF
            width: parent.width/11
            anchors.right: rectangleEHF.left
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("SHF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: rectangleEHF
            width: parent.width/11
            anchors.right: parent.right
            height: 20
            color: "#00ffffff"
            Label {
                text: qsTr("EHF")
                font.bold: true
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Rectangle {
            id: selector
            height: 20
            color: Material.accent
            radius: 10
            z: -1
        }
    }
}
