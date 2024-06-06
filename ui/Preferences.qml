import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Window {
    id: windowPreferences

    width: 450
    height: 400

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    title: qsTr("Artemis - Preferences")

    signal saveMaterialAccent(string arg)
    signal saveMaterialTheme(string arg)
    signal saveAutoload(int arg)

    function saveAll() {
        saveMaterialAccent(comboBoxAccent.currentText)
        saveMaterialTheme(comboBoxTheme.currentText)
        saveAutoload(checkBoxAutoload.checked)
    }

    function loadMaterialAccent(accent) {
        for (var idx = 0; idx < comboBoxAccent.count; idx ++) {
            if (accent === comboBoxAccent.valueAt(idx)) {
                comboBoxAccent.currentIndex = idx
                break
            }
        }
    }

    function loadMaterialTheme(theme) {
        for (var idx = 0; idx < comboBoxTheme.count; idx ++) {
            if (theme === comboBoxTheme.valueAt(idx)) {
                comboBoxTheme.currentIndex = idx
                break
            }
        }
    }

    function loadAutoload(toggle) {
        if (toggle) {
            checkBoxAutoload.checked = true
        } else {
            checkBoxAutoload.checked = false
        }
    }

    DialogMessage {
        id: dialogPreferencesSaved
        modal: true

        title: "Preferences saved!"
        message: "User preferences has been saved succesfully! Artemis restart is require for changes to take effect."

        standardButtons: Dialog.Ok

        onAccepted: {
            windowPreferences.close()
        }
    }


    Pane {
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: "Material Theme"
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxTheme
                    width: 137
                    height: 48
                    model: [
                        "System",
                        "Light",
                        "Dark"
                    ]
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: "Material Accent"
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxAccent
                    width: 137
                    height: 48
                    model: [
                        "Red",
                        "Pink",
                        "Purple",
                        "DeepPurple",
                        "Indigo",
                        "Blue",
                        "LightBlue",
                        "Cyan",
                        "Teal",
                        "Green",
                        "LightGreen",
                        "Lime",
                        "Yellow",
                        "Amber",
                        "Orange",
                        "DeepOrange",
                        "Brown",
                        "Grey",
                        "BlueGrey"
                    ]
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: "Auto-load SigID Database on Startup"
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                CheckBox {
                    id: checkBoxAutoload
                }
            }

            Item {
                Layout.fillHeight: true
            }

            Button {
                text: qsTr("Save")
                icon.source: "qrc:/images/icons/save.svg"
                display: AbstractButton.TextBesideIcon
                Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                onClicked: {
                    saveAll()
                    dialogPreferencesSaved.open()
                }
            }
        }
    }
}
