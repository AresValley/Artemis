import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents


Window {
    id: windowCategoryEditor
    title: 'Artemis - Category Manager'

    width: 450
    height: 400

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    property var currentSelectedItem: null

    signal saveParam(var data, bool isNew)
    signal deleteParam(int clbId)

    function loadList(dict) {
        clearAll()

        var mappedList = []
        for (var i = 0; i < dict.length; i++) {
            mappedList.push({
                clb_id: dict[i].clb_id,
                name: dict[i].value ? dict[i].value : "",
                description: ""
            })
        }
        
        customCategoryList.populateList(mappedList)
    }

    function clearAll() {
        currentSelectedItem = null
        customCategoryList.clearList()
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: qsTr("Are you sure?")
        message: qsTr("You are about to delete the selected category tag. The process cannot be undone.")
        messageType: "warn"
        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            if (currentSelectedItem) {
                deleteParam(currentSelectedItem.clb_id)
            }
        }
    }

    Dialog {
        id: dialogNewCat

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        modal: true
        closePolicy: Popup.NoAutoClose

        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            Label {
                text: qsTr("Enter the name of the new tag:")
                Layout.bottomMargin: 15
                font.pointSize: 12
            }
            TextField {
                id: newCatName
                Layout.fillWidth: true
                placeholderText: qsTr("Tag Name")
            }
        }

        onAccepted: {
            saveParam([newCatName.text], true)
            newCatName.clear()
        }
    }

    Dialog {
        id: dialogRenameCat

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        modal: true
        closePolicy: Popup.NoAutoClose

        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            Label {
                text: qsTr("Enter the new name for the tag:")
                Layout.bottomMargin: 15
                font.pointSize: 12
            }
            TextField {
                id: renameCatName
                Layout.fillWidth: true
                placeholderText: qsTr("Tag Name")
            }
        }

        onAccepted: {
            if (currentSelectedItem) {
                saveParam(
                    [
                        renameCatName.text,
                        currentSelectedItem.clb_id
                    ],
                    false
                )
            }
        }
    }

    Page {
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10

            RowLayout {
                Layout.fillHeight: true
                Layout.fillWidth: true

                UIComponents.ArtemisListView {
                    id: customCategoryList
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    onItemSelected: (selectedItem) => {
                        currentSelectedItem = selectedItem
                        renameButton.enabled = true
                        deleteButton.enabled = true
                    }

                    onSelectionCleared: {
                        currentSelectedItem = null
                        renameButton.enabled = false
                        deleteButton.enabled = false
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true

                UIComponents.ArtemisButton {
                    id: deleteButton
                    text: qsTr("Delete")
                    type: "danger"
                    enabled: false
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    icon.source: "qrc:/data/images/icons/delete.svg"
                    display: AbstractButton.TextBesideIcon
                    onClicked: {
                        dialogDeleteConfirmation.open()
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

                UIComponents.ArtemisButton {
                    id: renameButton
                    text: qsTr("Rename")
                    type: "warning"
                    enabled: false
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    icon.source: "qrc:/data/images/icons/rename.svg"
                    display: AbstractButton.TextBesideIcon
                    onClicked: {
                        if (currentSelectedItem) {
                            renameCatName.text = currentSelectedItem.name
                        }
                        dialogRenameCat.open()
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

                UIComponents.ArtemisButton {
                    id: addButton
                    text: qsTr("Add")
                    type: "success"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    icon.source: "qrc:/data/images/icons/add.svg"
                    display: AbstractButton.TextBesideIcon
                    onClicked: {
                        dialogNewCat.open()
                    }
                }
            }
        }
    }
}
