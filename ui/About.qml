import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Controls.Material


Dialog {
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    property int currentYear: new Date().getFullYear()

    modal: true

    RowLayout {
        Layout.fillWidth: true

        spacing: 10

        Image {
            Layout.alignment: Qt.AlignCenter

            sourceSize.height: 80
            sourceSize.width: 80
            source: "qrc:///images/artemis_icon.svg"
        }

        Label {
            text: "<style>a { color: " + Material.accent + "; }</style>" +
                    "<p><b>Artemis</a> " + APPLICATION_VERSION + "</b></p>" +
                    "<p>" + "<a href=\"https://github.com/AresValley/Artemis\">ARTEMIS</a> " +
                    qsTr("- The Radio Signals Recognition Manual") + "<br/>" +
                    "Powered By Python " + PYTHON_VERSION + " & Qt " + QT_VERSION + "</p>" +
                    "<p>Copyright (c) 2014-" + currentYear + " <a href=\"https://aresvalley.com\">" + qsTr("AresValley") +
                    "</a> GPLv3 License</p>"

            Layout.fillWidth: true
            Layout.minimumWidth: 200

            textFormat: Text.RichText
            wrapMode: Text.WordWrap

            onLinkActivated: (link) => {
                Qt.openUrlExternally(link)
            }
        }
    }
}
