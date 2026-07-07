import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents


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
    signal saveLocalizationLanguage(string arg)
    signal saveScaling(string arg)
    signal saveAutoload(int arg)

    function saveAll() {
        saveMaterialAccent(comboBoxAccent.currentText)
        saveMaterialTheme(comboBoxTheme.currentText)
        saveLocalizationLanguage(comboBoxLanguage.currentValue)
        saveAutoload(checkBoxAutoload.checked)
        saveScaling(comboBoxScaling.currentText)
    }

    function loadMaterialAccent(accent) {
        for (var idx = 0; idx < comboBoxAccent.count; idx++) {
            if (accent === comboBoxAccent.valueAt(idx)) {
                comboBoxAccent.currentIndex = idx
                break
            }
        }
    }

    function loadMaterialTheme(theme) {
        for (var idx = 0; idx < comboBoxTheme.count; idx++) {
            if (theme === comboBoxTheme.valueAt(idx)) {
                comboBoxTheme.currentIndex = idx
                break
            }
        }
    }

    function loadLocalizationLanguage(language) {
        const idx = comboBoxLanguage.indexOfValue(language)
        if (idx >= 0)
            comboBoxLanguage.currentIndex = idx
    }

    function loadScaling(scaling) {
        for (var idx = 0; idx < comboBoxScaling.count; idx++) {
            if (scaling === comboBoxScaling.valueAt(idx)) {
                comboBoxScaling.currentIndex = idx
                break
            }
        }
    }

    function loadAutoload(toggle) {
        checkBoxAutoload.checked = !!toggle
    }

    DialogMessage {
        id: dialogPreferencesSaved
        modal: true
        anchors.centerIn: parent

        title: qsTr("Preferences saved!")
        message: qsTr("User preferences have been saved successfully! An Artemis restart is required for changes to take effect.")

        standardButtons: Dialog.Ok

        onAccepted: {
            windowPreferences.close()
        }
    }

    Pane {
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: qsTr("Language")
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxLanguage
                    Layout.preferredWidth: 137
                    Layout.preferredHeight: 48
                    textRole: "text"
                    valueRole: "value"
                    model: ListModel {
                        ListElement { text: "English"; value: "en_US" }
                        ListElement { text: "Italiano";  value: "it_IT" }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: qsTr("Material Theme")
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxTheme
                    Layout.preferredWidth: 137
                    Layout.preferredHeight: 48
                    model: ["System", "Light", "Dark"]
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: qsTr("Material Accent")
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxAccent
                    Layout.preferredWidth: 137
                    Layout.preferredHeight: 48
                    model: [
                        "Red", "Pink", "Purple", "DeepPurple", "Indigo",
                        "Blue", "LightBlue", "Cyan", "Teal", "Green",
                        "LightGreen", "Lime", "Yellow", "Amber", "Orange",
                        "DeepOrange", "Brown", "Grey", "BlueGrey"
                    ]
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: qsTr("DPI Scaling")
                    font.pixelSize: 12
                    clip: true
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: comboBoxScaling
                    Layout.preferredWidth: 137
                    Layout.preferredHeight: 48
                    model: [
                        "0.50", "0.55", "0.60", "0.65", "0.70",
                        "0.75", "0.80", "0.85", "0.90", "0.95",
                        "1.00", "1.05", "1.10", "1.15", "1.20",
                        "1.25", "1.30", "1.35", "1.40", "1.45",
                        "1.50"
                    ]
                }
            }

            RowLayout {
                Layout.fillWidth: true

                Label {
                    text: qsTr("Auto-load SigID database on startup (latest version)")
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

            UIComponents.ArtemisButton {
                text: qsTr("Save")
                type: "success"
                icon.source: "qrc:/data/images/icons/save.svg"
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
