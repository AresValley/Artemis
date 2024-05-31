import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs

Window {
    id: documentsManageranager

    width: 800
    height: 500

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


    function loadList(dict) {
        clearAll()
        for (var i = 0; i < dict.length; i++) {
            myModel.append(dict[i])
        }
        itemChanged()
    }

    function getModel() {
        var dictionaryList = []
        for (var i = 0; i < myModel.count; i++) {
            var dictionary = [
                myModel.get(i).doc_id,
                myModel.get(i).name,
                myModel.get(i).description,
                myModel.get(i).type,
                myModel.get(i).preview,
                myModel.get(i).extension
            ]
            dictionaryList.push(dictionary)
        }
        return dictionaryList
    }

    function itemChanged() {
        var selected_doc = myModel.get(listView.currentIndex)
        if (selected_doc !== undefined) {

            var docId = selected_doc.doc_id
            var extension = selected_doc.extension
            var name = selected_doc.name
            var description = selected_doc.description
            var type = selected_doc.type
            var preview = selected_doc.preview

            nameField.text = name
            fileNameField.text = docId + '.' + extension
            descriptionField.text = description
            lockMenu(false)

            if (type === 'Image' || type === 'Audio') {
                switchPreview.visible = true
                if (preview === 1) {
                    switchPreview.checked = true
                } else {
                    switchPreview.checked = false
                }
            } else {
                switchPreview.visible = false
            }
        } else {
            lockMenu(true)
        }
    }

    function contentChanged() {
        if (listView.currentIndex !== -1) {
            myModel.set(
                listView.currentIndex,
                {
                    'name': nameField.text,
                    'description': descriptionField.text,
                }
            )
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
        myModel.clear()
    }

    function previewChanged(is_preview) {
        var previewItem = myModel.get(listView.currentIndex)
        if (previewItem.preview !== is_preview) {
            if (is_preview) {
                for (var i = 0; i < myModel.count; i++) {
                    if (myModel.get(i).type === previewItem.type) {
                        myModel.get(i).preview = 0
                    }
                }
                previewItem.preview = 1            
            } else {
                previewItem.preview = 0
            }
            updateDoc(getModel())
            itemChanged()
            changeSavedDialog.open()
        }
    }

    function validateFields() {
        if (newPathField.text === '' || newNameField.text === '') {
            // message file or name not selected
            return false
        } else {
            return true
        }
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
        var selected_doc = myModel.get(listView.currentIndex)
        var doc_param = [
            selected_doc.doc_id,
            name,
            description,
            type,
            selected_doc.preview,
        ]
        updateDoc([doc_param])
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        nameFilters: [
            "Image (*.jpg *.png)",
            "Audio (*.mp3 *.m4a *.ogg)",
            "Document (*.txt *.pdf)",
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

            RowLayout {
                Layout.fillWidth: true
                
                TextField {
                    id: newPathField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Path")
                    readOnly: true
                }
                
                Button {
                    text: qsTr("Browse")
                    onClicked: {
                        fileDialog.open()
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                
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

            ScrollView {
                Layout.fillHeight: true
                Layout.fillWidth: true
                ScrollBar.vertical.interactive: true
                
                TextArea {
                    id: newDescriptionField
                    placeholderText: qsTr("Description")
                    wrapMode: TextEdit.WordWrap
                }
            }
        }

        onAccepted: {
            if (validateFields()) {
                saveNewDoc(
                    [
                        newPathField.text,
                        newNameField.text,
                        newDescriptionField.text,
                        newFileTypeComboBox.currentText
                    ]
                )
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

            RowLayout {
                Layout.fillWidth: true
                
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

            ScrollView {
                Layout.fillHeight: true
                Layout.fillWidth: true
                ScrollBar.vertical.interactive: true
                
                TextArea {
                    id: editDescriptionField
                    placeholderText: qsTr("Description")
                    wrapMode: TextEdit.WordWrap
                }
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
            deleteDoc(
                myModel.get(listView.currentIndex).doc_id,
                myModel.get(listView.currentIndex).extension,
                myModel.get(listView.currentIndex).type,
                myModel.get(listView.currentIndex).preview
            )
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

        RowLayout {
            anchors.fill: parent
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            spacing: 0
            anchors.topMargin: 10

            ColumnLayout {
                Layout.minimumWidth: 150
                RowLayout {
                    Component {
                        id: sectionHeading
                        Rectangle {
                            width: ListView.view.width
                            height: 30
                            color: "#00000000"
                            Label {
                                text: section
                                font.capitalization: Font.AllUppercase
                                font.bold: true
                                font.pixelSize: 16
                                color: Material.accent
                                font.letterSpacing: 0.5
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter
                            }
                        }
                    }

                    ListView {
                        id: listView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        highlightMoveDuration: 0
                        clip: true
                        focus: true
                        ScrollBar.vertical: bar
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
                        
                        section.property: "type"
                        section.criteria: ViewSection.FullString
                        section.delegate: sectionHeading
                    }
                    ScrollBar {
                        id: bar
                        Layout.fillHeight: true
                        active: true
                    }
                }

                Button {
                    id: addButton
                    text: qsTr("Add")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    icon.source: "qrc:/images/icons/add.svg"
                    display: AbstractButton.TextBesideIcon
                    onClicked: {
                        dialogAddNew.open()
                    }
                }
            }

            ToolSeparator {
                id: toolSeparator
                rightPadding: 10
                leftPadding: 10
                Layout.fillHeight: true
            }

            ColumnLayout {
                Layout.preferredWidth: 300

                Label {
                    text: qsTr("FILE DETAILS")
                    font.letterSpacing: 0.5
                    color: Material.accent
                    font.pixelSize: 18
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                TextField {
                    id: nameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("Name")
                    onTextChanged: {
                        contentChanged()
                    }
                }

                TextField {
                    id: fileNameField
                    Layout.fillWidth: true
                    placeholderText: qsTr("File")
                    readOnly: true
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    ScrollBar.vertical.interactive: true

                    TextArea {
                        id: descriptionField
                        wrapMode: TextEdit.WordWrap
                        font.pointSize: 10
                        onTextChanged: {
                            contentChanged()
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: deleteButton
                        text: qsTr("Delete")
                        icon.source: "qrc:/images/icons/delete.svg"
                        display: AbstractButton.TextBesideIcon
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            dialogDeleteConfirmation.open()
                        }
                    }

                    Item {
                        Layout.fillWidth: true
                    }

                    Switch {
                        id: switchPreview
                        text: qsTr("Main")

                        onCheckedChanged: {
                            if (checked) {
                                previewChanged(1)
                            } else {
                                previewChanged(0)
                            }
                        }
                    }

                    Button {
                        id: editButton
                        text: qsTr("Edit")
                        enabled: false
                        icon.source: "qrc:/images/icons/rename.svg"
                        display: AbstractButton.TextBesideIcon
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            editNameField.text = myModel.get(listView.currentIndex).name
                            setEditFileTypeComboBox(myModel.get(listView.currentIndex).type)
                            editDescriptionField.text = myModel.get(listView.currentIndex).description
                            dialogEdit.open()
                        }
                    }

                    Button {
                        id: openButton
                        text: qsTr("Open")
                        enabled: false
                        icon.source: "qrc:/images/icons/open.svg"
                        display: AbstractButton.TextBesideIcon
                        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                        onClicked: {
                            openDoc(
                                myModel.get(listView.currentIndex).doc_id,
                                myModel.get(listView.currentIndex).extension
                            )
                        }
                    }
                }
            }
        }
    }
}
