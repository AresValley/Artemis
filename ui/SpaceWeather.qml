import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Window {
    id: windowSpaceWeather

    width: 1000
    height: 700

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    title: qsTr("Artemis - Space Weather")

    function updateBottomBar(message) {
        spaceBottomBar.text = message
    }


    Page {
        anchors.fill: parent

        footer: Label {
            id: spaceBottomBar
            font.pixelSize: 12
            leftPadding: 5
            rightPadding: 5
            bottomPadding: 5
        }

        ColumnLayout {
            anchors.fill: parent

            TabBar {
                id: tabBar
                width: parent.width
                Layout.fillWidth: true

                TabButton {
                    text: qsTr("Current")
                }
                TabButton {
                    text: qsTr("Forecasts")
                }
            }

            StackLayout {
                currentIndex: tabBar.currentIndex
                Layout.fillHeight: true
                Layout.fillWidth: true

                Item {
                    SpaceWeatherCurrentPage {
                        id: spaceWeatherCurrentPage
                    }
                }

                Item {
                    SpaceWeatherForecastPage {
                        id: spaceWeatherForecastPage
                    }
                }
            }
        }
    }
}
