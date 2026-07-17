import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs


import './components' as UIComponents

Window {
    id: documentsManageranager

    width: 820  
    height: 520 

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    title: qsTr("Artemis - Documents Manager")


    signal saveNewDoc (variant docParamLst)
    signal updateDoc (variant docParamLst)
    signal deleteDoc (string docId, string extension, string type, bool preview)
    signal openDoc (string docId, string extension)


    property var currentDoc: null

    function loadList(dict) {
        clearAll()
        listView.populateList(dict)
    }

    function getModel() {
        var dictionaryList = []
        var list = listView.loadedList
        if (!list) return dictionaryList

        for (var i = 0; i < list.length; i++) {
            var dictionary = [
                list[i].doc_id,
                list[i].name,
                list[i].description,
                list[i].type,
                list[i].preview,
                list[i].extension
            ]
            dictionaryList.push(dictionary)
        }
        return dictionaryList
    }

    function itemChanged() {
        if (currentDoc !== undefined && currentDoc !== null) {
            nameField.text = currentDoc.name ? currentDoc.name : ""
            fileNameField.text = currentDoc.doc_id + '.' + currentDoc.extension
            descriptionField.text = currentDoc.description ? currentDoc.description : ""
            lockMenu(false)

            if (currentDoc.type === 'Image' || currentDoc.type === 'Audio') {
                switchPreview.visible = true
                switchPreview.checked = currentDoc.preview
            } else {
                switchPreview.visible = false
            }
        } else {
            lockMenu(true)
        }
    }

    function lockMenu(toggle) {
        if (toggle) {
            openButton.enabled = false
            switchPreview.visible = false
            deleteButton.enabled = false
            editButton.enabled = false
        } else {
            openButton.enabled = true
            deleteButton.enabled = true
            editButton.enabled = true
        }
    }

    function clearAll() {
        nameField.clear()
        fileNameField.clear()
        descriptionField.clear()
        listView.clearList()
        currentDoc = null
    }

    function previewChanged(is_preview) {
        if (!currentDoc || currentDoc.preview === is_preview) return

        var list = listView.loadedList || []

        list.forEach(function(item) {
            if (is_preview === 1 && item.type === currentDoc.type) item.preview = 0
            if (item.doc_id === currentDoc.doc_id) item.preview = is_preview
        })

        currentDoc.preview = is_preview

        updateDoc(getModel())
        listView.populateList(list)
        changeSavedDialog.open()
    }

    function validateFields() {
        return (newPathField.text !== '' && newNameField.text !== '')
    }

    function setEditFileTypeComboBox(type) {
        for (var idx = 0; idx < editFileTypeComboBox.count; idx ++) {
            if (type === editFileTypeComboBox.valueAt(idx)) {
                editFileTypeComboBox.currentIndex = idx
                break
            }
        }
    }

    function editCurrentDoc(name, description, type) {
        if (!currentDoc) return
        var doc_param = [
            currentDoc.doc_id,
            name,
            description,
            type,
            currentDoc.preview,
        ]
        updateDoc([doc_param])
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        nameFilters: [
            "Image (*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.tif *.webp *.svg *.heic *.raw *.cr2 *.nef *.orf *.sr2 *.arw *.dng)",
            "Audio (*.mp3 *.wav *.aac *.flac *.alac *.wma *.ogg *.m4a *.aiff *.aif *.amr *.opus *.mid *.midi *.pcm)",
            "Document (*.doc *.docx *.pdf *.txt *.rtf *.odt *.html *.htm *.xml *.ppt *.pptx *.xls *.xlsx *.csv *.epub *.mobi *.md *.tex *.wps)",
            "All files (*)"
        ]

        onAccepted: {
            newPathField.text = selectedFile
            if (selectedNameFilter.name === 'Image') {
                newFileTypeComboBox.currentIndex = 0
            } else if (selectedNameFilter.name === 'Audio') {
                newFileTypeComboBox.currentIndex = 1
            } else if (selectedNameFilter.name === 'Document') {
                newFileTypeComboBox.currentIndex = 2
            } else {
                newFileTypeComboBox.currentIndex = 3
            }
        }
    }

    Dialog {
        id: dialogAddNew
        height: 400
        width: 400
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        modal: true
        closePolicy: Popup.NoAutoClose
        standardButtons: Dialog.Save | Dialog.Close

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                TextField {
                    id: newPathField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Path")
                    readOnly: true
                }
                UIComponents.ArtemisButton {
                    text: qsTr("Browse")
                    onClicked: fileDialog.open()
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                ComboBox {
                    id: newFileTypeComboBox
                    model: ["Image", "Audio", "Document", "Other"]
                }
                TextField {
                    id: newNameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Name")
                }
            }

            Flickable {
                Layout.fillWidth: true
                Layout.fillHeight: true
                TextArea.flickable: TextArea {
                    id: newDescriptionField
                    placeholderText: qsTr("Description")
                    font.pointSize: 10
                    wrapMode: TextEdit.WordWrap
                }
                ScrollBar.vertical: ScrollBar { width: 10 }
            }
        }

        onAccepted: {
            if (validateFields()) {
                saveNewDoc([
                    newPathField.text,
                    newNameField.text,
                    newDescriptionField.text,
                    newFileTypeComboBox.currentText
                ])
            }
        }
    }

    Dialog {
        id: dialogEdit
        height: 400
        width: 400
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        modal: true
        closePolicy: Popup.NoAutoClose
        standardButtons: Dialog.Save | Dialog.Close

        ColumnLayout {
            anchors.fill: parent
            spacing: 10

            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                ComboBox {
                    id: editFileTypeComboBox
                    model: ["Image", "Audio", "Document", "Other"]
                }
                TextField {
                    id: editNameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Name")
                }
            }

            Flickable {
                Layout.fillWidth: true
                Layout.fillHeight: true
                TextArea.flickable: TextArea {
                    id: editDescriptionField
                    placeholderText: qsTr("Description")
                    font.pointSize: 10
                    wrapMode: TextEdit.WordWrap
                }
                ScrollBar.vertical: ScrollBar { width: 10 }
            }
        }

        onAccepted: {
            editCurrentDoc(
                editNameField.text,
                editDescriptionField.text,
                editFileTypeComboBox.currentText
            )
        }
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: "Are you sure?"
        message: "You are about to delete the selected document. The process cannot be undone."
        messageType: "warn"
        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            if (currentDoc) {
                deleteDoc(
                    currentDoc.doc_id,
                    currentDoc.extension,
                    currentDoc.type,
                    currentDoc.preview
                )
            }
        }
    }

    DialogMessage {
        id: changeSavedDialog
        title: 'Change Saved!'
        message: 'Your changes have been successfully saved!'
        standardButtons: Dialog.Ok
    }

    Page {
        anchors.fill: parent

        SplitView {
            anchors.fill: parent
            anchors.margins: 14
            orientation: Qt.Horizontal

            handle: Rectangle {
                implicitWidth: 4
                color: SplitHandle.pressed ? Qt.lighter(Material.accent, 1.0)
                    : (SplitHandle.hovered ? Qt.lighter(Material.accent, 1.5) : "transparent")
            }

            ColumnLayout {
                SplitView.fillWidth: false
                SplitView.minimumWidth: 180
                SplitView.preferredWidth: 240
                spacing: 10

                UIComponents.ArtemisListView {
                    id: listView
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    onItemSelected: (itemObj) => {
                        currentDoc = itemObj
                        itemChanged()
                    }
                    onSelectionCleared: {
                        currentDoc = null
                        itemChanged()
                    }
                }

                UIComponents.ArtemisButton {
                    id: addButton
                    text: qsTr("Add New")
                    type: "success"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    icon.source: "qrc:/data/images/icons/add.svg"
                    display: AbstractButton.TextBesideIcon
                    onClicked: dialogAddNew.open()
                }
            }

            ColumnLayout {
                SplitView.fillWidth: true
                SplitView.minimumWidth: 340
                spacing: 12 

                Label {
                    text: qsTr("FILE DETAILS")
                    font.letterSpacing: 0.8
                    font.bold: true
                    color: Material.accent
                    font.pixelSize: 14
                    Layout.alignment: Qt.AlignHCenter
                    Layout.bottomMargin: 4
                }

                TextField {
                    id: nameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Name")
                    readOnly: true
                }

                TextField {
                    id: fileNameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("File Name")
                    readOnly: true
                }

                Flickable {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    TextArea.flickable: TextArea {
                        id: descriptionField
                        placeholderText: qsTr("Description")
                        readOnly: true
                        font.pointSize: 10
                        wrapMode: TextEdit.WordWrap
                    }
                    ScrollBar.vertical: ScrollBar { width: 10 }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 8

                    UIComponents.ArtemisButton {
                        id: deleteButton
                        text: qsTr("Delete")
                        type: "danger"
                        icon.source: "qrc:/data/images/icons/delete.svg"
                        display: AbstractButton.TextBesideIcon
                        onClicked: dialogDeleteConfirmation.open()
                    }

                    Item { Layout.fillWidth: true } 

                    Switch {
                        id: switchPreview
                        text: qsTr("Main")
                        Layout.alignment: Qt.AlignVCenter
                        checked: currentDoc ? (currentDoc.preview === 1) : false
                        onToggled: previewChanged(checked ? 1 : 0)
                    }

                    UIComponents.ArtemisButton {
                        id: editButton
                        text: qsTr("Edit")
                        type: "warning"
                        enabled: false
                        icon.source: "qrc:/data/images/icons/rename.svg"
                        display: AbstractButton.TextBesideIcon
                        onClicked: {
                            if (currentDoc) {
                                editNameField.text = currentDoc.name ? currentDoc.name : ""
                                setEditFileTypeComboBox(currentDoc.type)
                                editDescriptionField.text = currentDoc.description ? currentDoc.description : ""
                                dialogEdit.open()
                            }
                        }
                    }

                    UIComponents.ArtemisButton {
                        id: openButton
                        text: qsTr("Open")
                        type: "success"
                        enabled: false
                        icon.source: "qrc:/data/images/icons/open.svg"
                        display: AbstractButton.TextBesideIcon
                        onClicked: {
                            if (currentDoc) {
                                openDoc(
                                    currentDoc.doc_id,
                                    currentDoc.extension
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}