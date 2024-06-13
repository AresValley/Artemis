import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs


Window {
    id: window
    width: 1100
    height: 800

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    title: qsTr("Artemis")
    visible: true
    
    modality: Qt.ApplicationModal
    flags: Qt.Window
    
    // Windows without upper bar
    //flags: Qt.FramelessWindowHint

    signal loadSignal(int signalId)
    signal showPref()
    signal showDBmanager()
    signal showCatManager()
    signal openSigEditor(string type, var sig_param, bool is_new)
    signal showSpaceWeather()
    signal checkForUpdate()
    signal updateDb()
    signal updateArtemis()
    signal openDbDirectory()
    signal newDb(string name)
    signal exportDb(string path)
    signal importDb(string path)

    property var loadedList

    function populateList(signalsList) {
        loadedList = signalsList
        textFieldSearch.enabled = true
        var currentIndex = listView.currentIndex
        refreshList()
        // Set the currentIndex back after refreshing the list
        if (currentIndex >= 0 && currentIndex < listModel.count) {
            listView.currentIndex = currentIndex
        }
    }

    function refreshList() {
        listModel.clear()
        for (var i = 0; i < loadedList.length; i++) {
            var name = loadedList[i].name.toLowerCase()
            var description = loadedList[i].description.toLowerCase()
            var search = textFieldSearch.text.toLowerCase()
            if (name.includes(search) || description.includes(search)) {
                listModel.append(loadedList[i])
            }
        }
        itemChangedList()
    }

    function itemChangedList() {
        var selected_sig = listModel.get(listView.currentIndex)
        if (selected_sig !== undefined) {
            loadSignal(listModel.get(listView.currentIndex).SIG_ID)
            editSignalMenu.enabled = true
        } else {
            editSignalMenu.enabled = false
        }
    }

    function clearList() {
        listModel.clear()
        loadedList = []
        textFieldSearch.clear()
        textFieldSearch.enabled = false
    }

    function lockMenu(toggle) {
        if (toggle) {
            openFileMenu.enabled = false
            exportFileMenu.enabled = false
            newSignalMenu.enabled = false
            editCategoryMenu.enabled = false
        } else {
            openFileMenu.enabled = true
            exportFileMenu.enabled = true
            newSignalMenu.enabled = true
            editCategoryMenu.enabled = true
        }
    }

    function bottomInfoBar(message, messageType) {
        bottomInfoLabel.text = message
        switch (messageType) {
        case "warning":
            bottomInfoLabel.color = Material.color(Material.Red)
            break
        case "info":
            bottomInfoLabel.color = Material.foreground
            break
        }
    }

    function openGeneralDialog(messageType, title, message) {
        dialogGeneral.messageType = messageType
        dialogGeneral.title = title
        dialogGeneral.message = message
        dialogGeneral.open()
    }

    function openDialogDownloadDb(messageType, title, message) {
        dialogDownloadDb.messageType = messageType
        dialogDownloadDb.title = title
        dialogDownloadDb.message = message
        dialogDownloadDb.open()
    }

    function openDialogUpdateArtemis(messageType, title, message, auto) {
        dialogUpdateArtemis.messageType = messageType
        dialogUpdateArtemis.title = title
        dialogUpdateArtemis.message = message
        dialogUpdateArtemis.autoUpdate = auto
        dialogUpdateArtemis.open()
    }

    DialogMessage {
        id: dialogDownloadDb
        modal: true

        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            updateDb()
        }
    }

    DialogMessage {
        id: dialogUpdateArtemis
        modal: true

        property bool autoUpdate

        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            if (autoUpdate) {
                updateArtemis();
            } else {
                Qt.openUrlExternally("https://github.com/AresValley/Artemis");
            }
        }
    }

    DialogMessage {
        id: dialogGeneral
        modal: true

        standardButtons: Dialog.Ok
    }

    Dialog {
        id: dialogNewDb

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        modal: true
        closePolicy: Popup.NoAutoClose

        standardButtons: Dialog.Ok | Dialog.Cancel

        ColumnLayout {
            anchors.fill: parent
            Label {
                text: qsTr("Enter the name of the new database:")
                Layout.bottomMargin: 15
                font.pointSize: 12
            }
            TextField {
                id: newDbName
                Layout.fillWidth: true
                placeholderText: qsTr("Name")
            }
        }

        onAccepted: {
            newDb(newDbName.text)
        }
    }

    FileDialog {
        id: exportDialog
        title: "Please choose a save folder..."
        fileMode: FileDialog.SaveFile
        nameFilters: ["Archive (.tar)"]

        onAccepted: {
            exportDb(selectedFile)
        }
    }

    FileDialog {
        id: importDialog
        title: "Please choose a valid tar.gz archive..."
        fileMode: FileDialog.OpenFile
        nameFilters: ["Archive (*.tar)"]

        onAccepted: {
            importDb(selectedFile)
        }
    }

    About {
        id: aboutDialog
    }

    Page {
        anchors.fill: parent
        leftPadding: 10
        bottomPadding: 10

        focus: true

        Keys.onDownPressed: listView.incrementCurrentIndex()
        Keys.onUpPressed: listView.decrementCurrentIndex()

        header: MenuBar {
            id: topBar

            Menu {
                title: qsTr("File")

                MenuItem {
                    text: "New Database..."
                    onClicked: {dialogNewDb.open()}
                }

                MenuItem {
                    text: "Load Database..."
                    onClicked: {showDBmanager()}
                }

                MenuSeparator {}

                MenuItem {
                    id: importFileMenu
                    text: "Import Database"
                    onClicked: {importDialog.open()}
                }

                MenuItem {
                    id: exportFileMenu
                    text: "Export Database"
                    onClicked: {exportDialog.open()}
                    enabled: false
                }

                MenuSeparator {}

                MenuItem {
                    id: editCategoryMenu
                    text: "Edit Tags"
                    onClicked: {showCatManager()}
                    enabled: false
                }

                MenuSeparator {}

                MenuItem {
                    id: openFileMenu
                    text: "Open Database Folder"
                    onClicked: {openDbDirectory()}
                    enabled: false
                }

                MenuItem {
                    text: "Preferences"
                    onClicked: {showPref()}
                }

                MenuItem {
                    text: "Exit"
                    onClicked: {window.close()}
                }

            }

            Menu {
                id: signalMenu
                title: qsTr("Signal")

                MenuItem {
                    id: newSignalMenu
                    enabled: false
                    text: "New.."
                    onClicked: {openSigEditor('Signal', [], true)}
                }

                MenuItem {
                    id: editSignalMenu
                    enabled: false
                    text: "Edit..."
                    onClicked: {openSigEditor('Signal', [], false)}
                }
            }

            Menu {
                title: qsTr("Space Weather")

                MenuItem {
                    text: "Check Report"
                    onClicked: {
                        showSpaceWeather()
                    }
                }
            }

            Menu {
                id: aboutMenu
                title: qsTr("Help")

                MenuItem {
                    text: "Check for Updates"
                    onClicked: {checkForUpdate()}
                }

                MenuSeparator {}

                MenuItem {
                    text: "Project Homepage"
                    onClicked: {Qt.openUrlExternally('https://aresvalley.com/')}
                }

                MenuItem {
                    text: "Documentation"
                    onClicked: {Qt.openUrlExternally('https://AresValley.github.io/Artemis')}
                }

                MenuItem {
                    text: "Show Release Notes"
                    onClicked: {Qt.openUrlExternally('https://github.com/AresValley/Artemis/blob/master/CHANGELOG.md')}
                }

                MenuSeparator {}

                MenuItem {
                    text: "Report Issue"
                    onClicked: {Qt.openUrlExternally('https://github.com/AresValley/Artemis/issues')}
                }

                MenuSeparator {}

                MenuItem {
                    text: "About"
                    onClicked: {
                        aboutDialog.open()
                    }
                }
            }
        }

        footer: Label {
            id: bottomInfoLabel
            font.pixelSize: 12
            leftPadding: 5
            rightPadding: 5
            bottomPadding: 5
        }

        RowLayout {
            anchors.fill: parent
            spacing: 10

            ColumnLayout {
                Layout.maximumWidth: 250

                TextField {
                    id: textFieldSearch
                    Layout.preferredHeight: 39
                    Layout.topMargin: 5
                    enabled: false
                    Layout.fillWidth: true

                    placeholderText: qsTr("Search")
                    onTextChanged: {
                        refreshList()
                    }
                }

                RowLayout {

                    ListView {
                        id: listView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        highlightMoveDuration: 0
                        clip: true
                        ScrollBar.vertical: bar
                        highlight: Rectangle { color: Material.accent; radius: 5 }
                        onCurrentIndexChanged: { itemChangedList() }
                        delegate: Item {
                            id: listDelegate
                            width: ListView.view.width
                            height: 20
                            Label {text: name}
                            MouseArea {
                                anchors.fill: parent
                                onClicked: listView.currentIndex = index
                            }
                        }
                        model: ListModel {
                            id: listModel
                        }
                    }

                    ScrollBar {
                        id: bar
                        Layout.fillHeight: true
                        active: true
                    }
                }
            }

            ColumnLayout {
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.fillHeight: true
                Layout.fillWidth: true

                TabBar {
                    id: tabBar
                    Layout.fillWidth: true

                    TabButton {
                        text: qsTr("SIGNAL")
                    }

                    TabButton {
                        text: qsTr("FILTERS")
                    }
                }

                StackLayout {
                    currentIndex: tabBar.currentIndex
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Item {
                        SignalPage {
                            id: signalPage
                        }
                    }

                    Item {
                        FilterPage {
                            id: filterPage
                        }
                    }
                }
            }
        }
    }
}
