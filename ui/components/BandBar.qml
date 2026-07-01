import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Item {
    id: root
    width: 400
    height: 20

    property real lastLof: -1
    property real lastUpf: -1
    property int selectedStart: -1
    property int selectedEnd: -1

    function bandIndex(freq) {
        if (freq < 30) return 0
        if (freq < 300) return 1
        if (freq < 3000) return 2
        if (freq < 30000) return 3
        if (freq < 300000) return 4
        if (freq < 3000000) return 5
        if (freq < 30000000) return 6
        if (freq < 300000000) return 7
        if (freq < 3000000000) return 8
        if (freq < 30000000000) return 9
        return 10
    }

    // Return "black" o "white" based on the luminance
    function contrastTextColor(color) {
        let luminance = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return luminance > 0.55 ? "black" : "white"
    }

    function setBandBar(lof, upf) {
        lastLof = lof
        lastUpf = upf

        if (container.width <= 0) return

        let start = bandIndex(lof)
        let end = bandIndex(upf)
        selectedStart = start
        selectedEnd = end

        let step = container.width / 11
        selector.x = start * step
        selector.width = Math.max(step, (end - start + 1) * step)
    }

    Rectangle {
        id: container
        anchors.fill: parent
        radius: 13

        onWidthChanged: {
            if (width > 0 && root.lastLof !== -1) {
                root.setBandBar(root.lastLof, root.lastUpf)
            }
        }

        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "#1a000000" }
            GradientStop { position: 0.5; color: "#3d000000" }
            GradientStop { position: 1.0; color: "#1a000000" }
        }

        Rectangle {
            id: selector
            height: parent.height
            x: 0
            width: 0
            radius: 10
            color: Material.accent
            z: 0
            Behavior on x {
                NumberAnimation { duration: 200; easing.type: Easing.InOutQuad }
            }
            Behavior on width {
                NumberAnimation { duration: 200; easing.type: Easing.InOutQuad }
            }
        }

        Row {
            anchors.fill: parent
            spacing: 0
            Repeater {
                model: ["ELF","SLF","ULF","VLF","LF","MF","HF","VHF","UHF","SHF","EHF"]
                delegate: Rectangle {
                    width: container.width / 11
                    height: container.height
                    color: "transparent"
                    Label {
                        anchors.fill: parent
                        text: modelData
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.bold: true
                        color: (index >= root.selectedStart && index <= root.selectedEnd)
                            ? root.contrastTextColor(Material.accent)
                            : Material.foreground

                        Behavior on color {
                            ColorAnimation { duration: 200 }
                        }
                    }
                }
            }
        }
    }
}
