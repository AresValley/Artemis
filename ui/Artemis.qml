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
    title: qsTr("Artemis")
    visible: true
    
    modality: Qt.ApplicationModal
    flags: Qt.Window

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    // MARK: Signals
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

    // MARK: Properties
    property var loadedList: []
    property bool updateAvailable: false

    // MARK: Functions
    function populateList(signalsList) {
        loadedList = signalsList
        textFieldSearch.enabled = true
        var currentIndex = listView.currentIndex
        refreshList()
        if (currentIndex >= 0 && currentIndex < listModel.count) {
            listView.currentIndex = currentIndex
        }
    }

    function refreshList() {
        listModel.clear()
        if (!loadedList) return

        var search = textFieldSearch.text.toLowerCase().trim()

        if (search === "") {
            for (var i = 0; i < loadedList.length; i++) {
                listModel.append(loadedList[i])
            }
        } else {
            for (var j = 0; j < loadedList.length; j++) {
                var name = loadedList[j].name ? loadedList[j].name.toLowerCase() : ""
                var description = loadedList[j].description ? loadedList[j].description.toLowerCase() : ""
                if (name.includes(search) || description.includes(search)) {
                    listModel.append(loadedList[j])
                }
            }
        }
        itemChangedList()
    }

    function itemChangedList() {
        var selected_sig = listModel.get(listView.currentIndex)
        if (selected_sig !== undefined && selected_sig !== null) {
            loadSignal(selected_sig.SIG_ID)
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
        openFileMenu.enabled = !toggle
        exportFileMenu.enabled = !toggle
        newSignalMenu.enabled = !toggle
        editCategoryMenu.enabled = !toggle
    }

    function bottomInfoBar(message, messageType) {
        bottomInfoLabel.text = message
        if (messageType === "warning") {
            bottomInfoLabel.color = Material.color(Material.Red)
        } else {
            bottomInfoLabel.color = Material.foreground
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

    // MARK: Dialogs
    DialogMessage {
        id: dialogDownloadDb
        modal: true
        standardButtons: Dialog.Cancel | Dialog.Yes
        onAccepted: updateDb()
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
            spacing: 10
            Label {
                text: qsTr("Enter the name of the new database:")
                Layout.bottomMargin: 5
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
            newDbName.clear()
        }
    }

    FileDialog {
        id: exportDialog
        title: "Please choose a save folder..."
        fileMode: FileDialog.SaveFile
        nameFilters: ["All files (*)"]
        onAccepted: exportDb(selectedFile)
    }

    FileDialog {
        id: importDialog
        title: "Please choose a valid tar.gz archive..."
        fileMode: FileDialog.OpenFile
        nameFilters: ["All files (*)"]
        onAccepted: importDb(selectedFile)
    }

    About {
        id: aboutDialog
    }

    // MARK: Main UI Layout
    Page {
        anchors.fill: parent
        leftPadding: 10
        bottomPadding: 10
        focus: true

        Keys.onDownPressed: listView.incrementCurrentIndex()
        Keys.onUpPressed: listView.decrementCurrentIndex()

        header: MenuBar {
            id: topBar
            background: Rectangle {
                    color: Material.backgroundColor
                }
            Menu {
                title: qsTr("File")
                MenuItem { text: "New Database..."; onClicked: dialogNewDb.open() }
                MenuItem { text: "Load Database..."; onClicked: showDBmanager() }
                MenuSeparator {}
                MenuItem { id: importFileMenu; text: "Import Database"; onClicked: importDialog.open() }
                MenuItem { id: exportFileMenu; text: "Export Database"; onClicked: exportDialog.open(); enabled: false }
                MenuSeparator {}
                MenuItem { id: editCategoryMenu; text: "Edit Tags"; onClicked: showCatManager(); enabled: false }
                MenuSeparator {}
                MenuItem { id: openFileMenu; text: "Open Database Folder"; onClicked: openDbDirectory(); enabled: false }
                MenuItem { text: "Preferences"; onClicked: showPref() }
                MenuItem { text: "Exit"; onClicked: window.close() }
            }

            Menu {
                id: signalMenu
                title: qsTr("Signal")
                MenuItem {
                    id: newSignalMenu
                    enabled: false
                    text: "New.."
                    onClicked: openSigEditor('Signal', [], true)
                }
                MenuItem {
                    id: editSignalMenu
                    enabled: false
                    text: "Edit..."
                    onClicked: {
                        var currentSig = listModel.get(listView.currentIndex)
                        if (currentSig) openSigEditor('Signal', currentSig, false)
                    }
                }
            }

            Menu {
                title: qsTr("Space Weather")
                MenuItem { text: "Check Report"; onClicked: showSpaceWeather() }
            }

            Menu {
                id: aboutMenu
                title: window.updateAvailable ? qsTr("Help •") : qsTr("Help")

                MenuItem {
                    id: checkForUpdatesItem
                    onClicked: checkForUpdate()
                    contentItem: RowLayout {
                        spacing: 10
                        Label {
                            text: qsTr("Check for Updates")
                            font: checkForUpdatesItem.font
                            color: checkForUpdatesItem.enabled ? Material.foreground : Material.hintTextColor
                            Layout.fillWidth: true
                        }
                        Rectangle {
                            id: updateDot
                            width: 8
                            height: 8
                            radius: 4
                            color: Material.color(Material.Red)
                            visible: window.updateAvailable
                            Layout.alignment: Qt.AlignVCenter

                            SequentialAnimation on opacity {
                                loops: Animation.Infinite
                                running: window.updateAvailable
                                NumberAnimation { from: 1.0; to: 0.4; duration: 250; easing.type: Easing.InOutQuad }
                                NumberAnimation { from: 0.4; to: 1.0; duration: 500; easing.type: Easing.InOutQuad }
                            }
                        }
                    }
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
                MenuItem { text: "About"; onClicked: aboutDialog.open() }
            }
        }

        footer: Label {
            id: bottomInfoLabel
            font.pixelSize: 12
            leftPadding: 5
            rightPadding: 5
            bottomPadding: 5
        }

        SplitView {
            id: mainSplitView
            anchors.fill: parent
            orientation: Qt.Horizontal

            // MARK: Left panel
            ColumnLayout {
                SplitView.preferredWidth: 250
                SplitView.minimumWidth: 200
                SplitView.maximumWidth: 450
                Layout.fillHeight: true

                TextField {
                    id: textFieldSearch
                    Layout.preferredHeight: 40
                    Layout.topMargin: 5
                    Layout.fillWidth: true
                    enabled: false
                    placeholderText: qsTr("Search")
                    onTextChanged: refreshList()
                }

                RowLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: 0

                    ListView {
                        id: listView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        highlightMoveDuration: 100
                        clip: true
                        ScrollBar.vertical: bar

                        highlight: Rectangle { 
                            color: Qt.alpha(Material.accent, 0.85)
                            radius: 4 
                        }
                        onCurrentIndexChanged: itemChangedList()
                        
                        delegate: Item {
                            id: listDelegate
                            width: listView.width
                            height: 25

                            HoverHandler {
                                id: hoverHandler
                            }

                            Rectangle {
                                anchors.fill: parent
                                color: Qt.alpha(Material.accent, 0.15)
                                radius: 4
                                visible: hoverHandler.hovered && listView.currentIndex !== index
                            }

                            Label {
                                text: model.name ? model.name : "" 
                                anchors.left: parent.left
                                anchors.leftMargin: 10
                                anchors.right: parent.right 
                                anchors.rightMargin: 8      
                                anchors.verticalCenter: parent.verticalCenter

                                color: listView.currentIndex === index ? Material.background : Material.foreground
                                font.weight: listView.currentIndex === index ? Font.Medium : Font.Normal
                                elide: Text.ElideRight
                            }

                            MouseArea {
                                anchors.fill: parent
                                onClicked: listView.currentIndex = index
                            }
                        }
                        model: ListModel { id: listModel }
                    }

                    ScrollBar {
                        id: bar
                        Layout.fillHeight: true
                        implicitWidth: 8
                        active: true
                        policy: ScrollBar.AsNeeded
                    }
                }
            }

            // MARK: Right panel
            ColumnLayout {
                SplitView.fillWidth: true 
                Layout.fillHeight: true
                spacing: 5

                TabBar {
                    id: tabBar
                    Layout.fillWidth: true
                    TabButton { text: qsTr("SIGNAL") }
                    TabButton { text: qsTr("FILTERS") }
                }

                StackLayout {
                    currentIndex: tabBar.currentIndex
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    SignalPage {
                        id: signalPage
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }

                    FilterPage {
                        id: filterPage
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }
        }
    }
}
