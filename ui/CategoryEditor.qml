import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Window {
    id: windowCategoryEditor
    title: 'Artemis - Category Manager'

    width: 450
    height: 400

    Component.onCompleted: {
        x = Screen.width/2 - width/2
        y = Screen.height/2 - height/2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    signal saveParam(var data, bool isNew)
    signal deleteParam(int clbId)

    function loadList(dict) {
        clearAll()
        for (var i = 0; i < dict.length; i++) {
            myModel.append(dict[i])
        }
    }

    function itemChanged() {
        var selected_cat = myModel.get(listView.currentIndex)
        if (selected_cat !== undefined) {
            renameButton.enabled = true
            deleteButton.enabled = true
        } else {
            renameButton.enabled = false
            deleteButton.enabled = false
        }
    }

    function getModel() {
        var modelList = []
        for (var i = 0; i < myModel.count; i++) {
            modelList.push(myModel.get(i).value)
        }
        return modelList
    }

    function clearAll() {
        myModel.clear()
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: "Are you sure?"
        message: "You are about to delete the selected category tag. The process cannot be undone."
        messageType: "warn"
        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            deleteParam(myModel.get(listView.currentIndex).clb_id)
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

            TextField {
                id: newCatName
                Layout.fillWidth: true
                placeholderText: qsTr("Tag")
            }
        }

        onAccepted: {
            saveParam([newCatName.text], true)
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

            TextField {
                id: renameCatName
                Layout.fillWidth: true
                placeholderText: qsTr("Tag")
            }
        }

        onAccepted: {
            saveParam(
                [
                    renameCatName.text,
                    myModel.get(listView.currentIndex).clb_id
                ],
                false
            )
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

                ListView {
                    id: listView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    highlightMoveDuration: 0
                    highlight: Rectangle { color: Material.accent; radius: 5 }
                    onCurrentIndexChanged: { itemChanged() }
                    delegate: Item {
                        id: listDelegate
                        width: ListView.view.width
                        height: 20
                        Label { text: value }
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
            }

            RowLayout {
                Layout.fillWidth: true

                Button {
                    id: addButton
                    text: qsTr("Add")
                    onClicked: {
                        dialogNewCat.open()
                    }
                    icon.source: "qrc:/images/icons/add.svg"
                    display: AbstractButton.TextBesideIcon
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Item {
                    Layout.fillWidth: true
                }

                Button {
                    id: renameButton
                    text: qsTr("Rename")
                    onClicked: {
                        dialogRenameCat.open()
                    }
                    icon.source: "qrc:/images/icons/rename.svg"
                    enabled: false
                    display: AbstractButton.TextBesideIcon
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }

                Item {
                    Layout.fillWidth: true
                }

                Button {
                    id: deleteButton
                    text: qsTr("Delete")
                    onClicked: {
                        dialogDeleteConfirmation.open()
                    }
                    icon.source: "qrc:/images/icons/delete.svg"
                    enabled: false
                    display: AbstractButton.TextBesideIcon
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }
        }
    }
}
