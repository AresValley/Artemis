import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents

Window {
    id: windowDBmanager

    width: 600
    height: 420

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    title: qsTr("Artemis - Load Database")

    property var currentSelectedItem: null
    property string loadedDbDirName: ""

    signal loadDB (string dbName)
    signal deleteDB (string dbName)
    signal renameDB (string dbName, string newDbName)

    function loadList(dict, loadedName) {
        clearAll()
        loadedDbDirName = loadedName
        customDBList.populateList(dict)
    }

    function clearAll() {
        currentSelectedItem = null
        titleLabel.text = 'N/A'
        versionLabel.text = ''
        dateLabel.text = ''
        totDocsLabel.text = ''
        totSignalsLabel.text = ''
        totImagesLabel.text = ''
        totAudioLabel.text = ''
        customDBList.clearList()
    }

    function loadDBButton() {
        if (currentSelectedItem) {
            loadDB(currentSelectedItem.db_dir_name)
        }
    }

    function lockMenu(toggle) {
        deleteButton.enabled = !toggle
        renameButton.enabled = !toggle
        loadButton.enabled = !toggle
    }

    function contrastTextColor(color) {
        let luminance = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return luminance > 0.55 ? "black" : "white"
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: "Are you sure?"
        message: "You are about to delete the database and all its contents permanently. The process cannot be undone."
        messageType: "warn"
        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            if (currentSelectedItem) {
                deleteDB(currentSelectedItem.db_dir_name)
            }
        }
    }

    Dialog {
        id: renameDbDialog
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        modal: true
        closePolicy: Popup.NoAutoClose
        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            Label {
                text: qsTr("Enter the new name for the database:")
                Layout.bottomMargin: 15
                font.pointSize: 12
            }
            TextField {
                id: newDbName
                Layout.fillWidth: true
                placeholderText: qsTr("New DB Name")
            }
        }

        onAccepted: {
            if (currentSelectedItem) {
                renameDB(currentSelectedItem.db_dir_name, newDbName.text)
            }
        }
    }

    Page {
        anchors.fill: parent

        SplitView {
            anchors.fill: parent

            anchors.margins: 12 
            
            orientation: Qt.Horizontal

            UIComponents.ArtemisListView {
                id: customDBList
                SplitView.minimumWidth: 160
                SplitView.preferredWidth: 190
                SplitView.maximumWidth: 260
                Layout.fillHeight: true

                onItemSelected: (selectedItem) => {
                    currentSelectedItem = selectedItem
                    lockMenu(false)
                    
                    titleLabel.text = selectedItem.name
                    versionLabel.text = 'VERSION ' + selectedItem.version
                    dateLabel.text = selectedItem.date
                    totDocsLabel.text = selectedItem.documents_n
                    totSignalsLabel.text = selectedItem.signals_n
                    totImagesLabel.text = selectedItem.images_n
                    totAudioLabel.text = selectedItem.audio_n
                }

                onSelectionCleared: {
                    currentSelectedItem = null
                    lockMenu(true)
                    
                    titleLabel.text = 'N/A'
                    versionLabel.text = ''
                    dateLabel.text = ''
                    totDocsLabel.text = ''
                    totSignalsLabel.text = ''
                    totImagesLabel.text = ''
                    totAudioLabel.text = ''
                }
            }

            Pane {
                SplitView.fillWidth: true
                Layout.fillHeight: true
                padding: 16

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 12

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 2

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 8

                            Label {
                                id: titleLabel
                                text: 'N/A'
                                font.pointSize: 16
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }

                            // "LOADED" badge
                            Rectangle {
                                id: loadedBadge
                                color: Material.accent
                                radius: 4
                                implicitWidth: badgeText.implicitWidth + 12
                                implicitHeight: badgeText.implicitHeight + 4
                                visible: currentSelectedItem
                                    ? (currentSelectedItem.db_dir_name === loadedDbDirName)
                                    : false
                                Text {
                                    id: badgeText
                                    text: "LOADED"
                                    color: contrastTextColor(Material.accent)
                                    font.pointSize: 9
                                    font.bold: true
                                    anchors.centerIn: parent
                                }
                            }
                        }
                        
                        Label {
                            id: versionLabel
                            text: ''
                            font.pointSize: 9
                            font.bold: true
                            color: Material.accent
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: Material.dropShadowColor
                        opacity: 0.2
                    }

                    GridLayout {
                        columns: 2
                        rowSpacing: 10
                        columnSpacing: 20
                        Layout.fillWidth: true

                        Label { 
                            text: qsTr("Total Signals:")
                            font.pointSize: 11
                            color: Material.hintTextColor 
                        }
                        Label { 
                            id: totSignalsLabel
                            text: ""
                            font.pointSize: 14
                            font.bold: true
                            color: Material.accent
                        }

                        Label { 
                            text: qsTr("Total Documents:")
                            font.pointSize: 11
                            color: Material.hintTextColor 
                        }
                        Label { 
                            id: totDocsLabel
                            text: ""
                            font.pointSize: 11
                            font.bold: true
                        }

                        Label { 
                            text: qsTr("  ├ Images:")
                            font.pointSize: 10
                            color: Material.hintTextColor
                        }
                        Label { 
                            id: totImagesLabel
                            text: ""
                            font.pointSize: 10
                        }

                        Label { 
                            text: qsTr("  └ Audio:")
                            font.pointSize: 10
                            color: Material.hintTextColor
                        }
                        Label { 
                            id: totAudioLabel
                            text: ""
                            font.pointSize: 10
                        }

                        Label { 
                            text: qsTr("DB Created:")
                            font.pointSize: 10
                            color: Material.hintTextColor
                            Layout.topMargin: 8
                        }
                        Label { 
                            id: dateLabel
                            text: ""
                            font.pointSize: 10
                            Layout.topMargin: 8
                        }     
                    }

                    Item {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10

                        UIComponents.ArtemisButton {
                            id: deleteButton
                            text: qsTr("Delete")
                            type: "danger"
                            enabled: false
                            icon.source: "qrc:/data/images/icons/delete.svg"
                            display: AbstractButton.TextBesideIcon
                            onClicked: dialogDeleteConfirmation.open()
                        }
                        
                        UIComponents.ArtemisButton {
                            id: renameButton
                            text: qsTr("Rename")
                            type: "warning"
                            enabled: false
                            icon.source: "qrc:/data/images/icons/rename.svg"
                            display: AbstractButton.TextBesideIcon
                            onClicked: {
                                if (currentSelectedItem) {
                                    newDbName.text = currentSelectedItem.name
                                }
                                renameDbDialog.open()
                            }
                        }

                        Item { Layout.fillWidth: true }

                        UIComponents.ArtemisButton {
                            id: loadButton
                            text: qsTr("Load")
                            type: "success"
                            enabled: false
                            icon.source: "qrc:/data/images/icons/open.svg"
                            display: AbstractButton.TextBesideIcon
                            font.bold: true
                            onClicked: loadDBButton()
                        }
                    }
                }
            }
        }
    }
}