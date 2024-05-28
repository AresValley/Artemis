import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Window {
    id: windowDBmanager

    width: 500
    height: 400

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    title: qsTr("Artemis - Load Database")

    signal loadDB (string dbName)
    signal deleteDB (string dbName)
    signal renameDB (string dbName, string newDbName)

    function loadList(dict) {
        clearAll()
        for (var i = 0; i < dict.length; i++) {
            myModel.append(dict[i])
        }
        itemChanged()
    }

    function itemChanged() {
        var selected_db = myModel.get(listView.currentIndex)
        if (selected_db !== undefined) {
            lockMenu(false)
            titleLabel.text = myModel.get(listView.currentIndex).name
            totDocsLabel.text = myModel.get(listView.currentIndex).documents_n
            totSignalsLabel.text = myModel.get(listView.currentIndex).signals_n
            totImagesLabel.text = myModel.get(listView.currentIndex).images_n
            totAudioLabel.text = myModel.get(listView.currentIndex).audio_n
        } else {
            lockMenu(true)
        }
    }

    function getModel() {
        var modelList = []
        for (var i = 0; i < myModel.count; i++) {
            modelList.push(myModel.get(i).name)
        }
        return modelList
    }

    function clearAll() {
        titleLabel.text = 'N/A'
        totDocsLabel.text = ''
        totSignalsLabel.text = ''
        totImagesLabel.text = ''
        totAudioLabel.text = ''
        myModel.clear()
    }

    function loadDBButton() {
        loadDB(myModel.get(listView.currentIndex).db_dir_name)
    }


    function renameDb() {
        if (textDBName.readOnly) {
            textDBName.focus = true
            textDBName.readOnly = false
            renameButton.highlighted = true
            createDbButton.enabled = false
            deleteDbButton.enabled = false
        }
        else {
            renameDB(myModel.get(listView.currentIndex).db_dir_name, textDBName.text)
            textDBName.focus = false
            textDBName.readOnly = true
            renameButton.highlighted = false
            createDbButton.enabled = true
            deleteDbButton.enabled = true
        }
    }

    function lockMenu(toggle) {
        if (toggle) {
            deleteButton.enabled = false
            renameButton.enabled = false
            loadButton.enabled = false
        } else {
            deleteButton.enabled = true
            renameButton.enabled = true
            loadButton.enabled = true
        }
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: "Are you sure?"
        message: "You are about to delete the database and all its contents permanently. The process cannot be undone."
        messageType: "warn"

        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            deleteDB(myModel.get(listView.currentIndex).db_dir_name)
        }
    }

    Dialog {
        id: renameDb

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        modal: true
        closePolicy: Popup.NoAutoClose

        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent

            TextField {
                id: newDbName
                Layout.fillWidth: true
                placeholderText: qsTr("New DB Name")
            }

        }

        onAccepted: {
            renameDB(myModel.get(listView.currentIndex).db_dir_name, newDbName.text)
        }
    }

    Page {
        anchors.fill: parent

        RowLayout {
            anchors.fill: parent
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10

            ListView {
                id: listView
                width: 150
                Layout.fillHeight: true
                highlight: Rectangle { color: Material.accent; radius: 5 }
                onCurrentIndexChanged: { itemChanged() }
                delegate: Item {
                    id: listDelegate
                    width: ListView.view.width
                    height: 20
                    Label { text: name }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            listView.currentIndex = index
                        }
                    }
                }
                model: ListModel {
                    id: myModel
                }
            }

            ToolSeparator {
                rightPadding: 10
                leftPadding: 10
                Layout.fillHeight: true
            }

            ColumnLayout {
                Layout.fillHeight: true
                Layout.fillWidth: true

                Label {
                    id: titleLabel
                    Layout.bottomMargin: 20
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    font.pointSize: 15
                    font.bold: true
                }
                GridLayout {
                    columnSpacing: 25
                    columns: 2

                    Label {
                        text: qsTr("Total Signals:")
                        font.pointSize: 12
                        font.bold: true
                    }

                    Label {
                        id: totSignalsLabel
                        text: qsTr("0")
                        font.pointSize: 12
                        font.bold: true
                    }

                    Label {
                        text: qsTr("Total Documents:")
                        font.pointSize: 12
                    }

                    Label {
                        id: totDocsLabel
                        text: qsTr("0")
                        font.pointSize: 12
                    }

                    Label {
                        text: qsTr("Images:")
                        Layout.leftMargin: 15
                        font.pointSize: 12
                    }

                    Label {
                        id: totImagesLabel
                        text: qsTr("0")
                        font.pointSize: 12
                    }

                    Label {
                        text: qsTr("Audio:")
                        Layout.leftMargin: 15
                        font.pointSize: 12
                    }

                    Label {
                        id: totAudioLabel
                        text: qsTr("0")
                        font.pointSize: 12
                    }                    
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                }

                RowLayout {
                    Button {
                        id: deleteButton
                        text: qsTr("Delete")
                        icon.source: "qrc:/images/icons/delete.svg"
                        display: AbstractButton.TextBesideIcon
                        enabled: false
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            dialogDeleteConfirmation.open()
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                    }

                    Button {
                        id: renameButton
                        text: qsTr("Rename")
                        icon.source: "qrc:/images/icons/rename.svg"
                        display: AbstractButton.TextBesideIcon
                        enabled: false
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            renameDb.open()
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                    }

                    Button {
                        id: loadButton
                        text: qsTr("Load")
                        icon.source: "qrc:/images/icons/load.svg"
                        display: AbstractButton.TextBesideIcon
                        enabled: false
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            loadDBButton()
                        }
                    }
                }
            }
        }
    }
}
