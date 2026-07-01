import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Dialogs

import './components' as UIComponents


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
    signal applyFilter(var filterDict)

    // MARK: Properties
    property var loadedList: []
    property var filterDict: ({})
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

    function populateFilterLists(data) {
        if (data && data.length > 0) {
            if (data[0].location) filterLocation.populate(data[0].location);
            if (data[0].category) filterCategory.populate(data[0].category);
            if (data[0].modulation) filterModulation.populate(data[0].modulation);
        }
    }

    function submitFilters() {
        applyFilter(filterDict);
    }

    function resetFilters() {
        filterLocation.resetToDefault();
        filterCategory.resetToDefault();
        filterModulation.resetToDefault();
        filterFrequency.resetToDefault();
        filterACF.resetToDefault();
        filterBandwidth.resetToDefault();
        applyFilter({});
    }

    function anyFilterActive() {
        return filterLocation.isFilterActive || 
            filterCategory.isFilterActive || 
            filterModulation.isFilterActive ||
            filterFrequency.isFilterActive ||
            filterBandwidth.isFilterActive ||
            filterACF.isFilterActive
    }

    // Return "black" o "white" based on the luminance
    function contrastTextColor(color) {
        let luminance = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return luminance > 0.55 ? "black" : "white"
    }

    // MARK: FILTERS
    UIComponents.FilterRangeDialog {
        id: filterFrequency
        objectName: "frequencyDialogObj"
        title: qsTr("Filter by Frequency")
        field_label: qsTr("Frequency")

        onFilterApplied: function(lowerBand, upperBand) {
            if (isFilterActive && lowerBand !== null && upperBand !== null) {
                filterDict["frequency"] = {
                    lower_band: lowerBand,
                    upper_band: upperBand
                }
            } else {
                delete filterDict["frequency"]
            }
            submitFilters()
        }
    }

    UIComponents.FilterRangeDialog {
        id: filterBandwidth
        objectName: "bandwidthDialogObj"
        title: qsTr("Filter by Bandwidth")
        field_label: qsTr("Bandwidth")

        onFilterApplied: function(lowerBand, upperBand) {
            if (isFilterActive && lowerBand !== null && upperBand !== null) {
                filterDict["bandwidth"] = {
                    lower_band: lowerBand,
                    upper_band: upperBand
                }
            } else {
                delete filterDict["bandwidth"]
            }
            submitFilters()
        }
    }

    UIComponents.FilterRangeDialog {
        id: filterACF
        objectName: "acfDialogObj"
        title: qsTr("Filter by ACF")
        field_label: qsTr("ACF")
        isTimeField: true

        onFilterApplied: function(lowerBand, upperBand) {
            if (isFilterActive && lowerBand !== null && upperBand !== null) {
                filterDict["acf"] = {
                    lower_band: lowerBand,
                    upper_band: upperBand
                }
            } else {
                delete filterDict["acf"]
            }
            submitFilters()
        }
    }

    UIComponents.FilterListDialog {
        id: filterLocation
        objectName: "locationDialogObj"
        title: qsTr("Filter by Location")
        
        onFilterApplied: function(selectedValues) {
            if (isFilterActive && selectedValues && selectedValues.length > 0) {
                filterDict["location"] = selectedValues;
            } else {
                delete filterDict["location"];
            }
            submitFilters();
        }
    }

    UIComponents.FilterListDialog {
        id: filterCategory
        objectName: "categoryDialogObj"
        title: qsTr("Filter by Category")
        
        onFilterApplied: function(selectedValues) {
            if (isFilterActive && selectedValues && selectedValues.length > 0) {
                filterDict["category"] = selectedValues;
            } else {
                delete filterDict["category"];
            }
            submitFilters();
        }
    }

    UIComponents.FilterListDialog {
        id: filterModulation
        objectName: "modulationDialogObj"
        title: qsTr("Filter by Modulation")
        
        onFilterApplied: function(selectedValues) {
            if (isFilterActive && selectedValues && selectedValues.length > 0) {
                filterDict["modulation"] = selectedValues;
            } else {
                delete filterDict["modulation"];
            }
            submitFilters();
        }
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

            delegate: MenuBarItem {
                id: menuBarItem
                contentItem: Label {
                    text: menuBarItem.text
                    font: menuBarItem.font
                    color: (menuBarItem.menu === filterMenu && anyFilterActive()) ? Material.color(Material.Red) : Material.foreground
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter

                    SequentialAnimation on opacity {
                        id: pulseAnimation
                        running: menuBarItem.menu === filterMenu && anyFilterActive()
                        loops: Animation.Infinite

                        NumberAnimation { to: 0.5; duration: 250; easing.type: Easing.InOutQuad }
                        NumberAnimation { to: 1.0; duration: 500; easing.type: Easing.InOutQuad }

                        onRunningChanged: {
                            if (!running)
                                menuBarItem.contentItem.opacity = 1.0
                        }
                    }
                }
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
                MenuItem { text: "Exit"; onClicked: close() }
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
                id: filterMenu
                title: anyFilterActive() ? qsTr("Filter ●") : qsTr("Filter")

                MenuItem {
                    text: qsTr("Frequency")
                    onClicked: filterFrequency.open()

                    contentItem: Label {
                        text: filterFrequency.isFilterActive
                            ? qsTr("Frequency ●")
                            : qsTr("Frequency")

                        color: filterFrequency.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    text: qsTr("Bandwidth")
                    onClicked: filterBandwidth.open()

                    contentItem: Label {
                        text: filterBandwidth.isFilterActive
                            ? qsTr("Bandwidth ●")
                            : qsTr("Bandwidth")

                        color: filterBandwidth.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    text: qsTr("ACF")
                    onClicked: filterACF.open()

                    contentItem: Label {
                        text: filterACF.isFilterActive
                            ? qsTr("ACF ●")
                            : qsTr("ACF")

                        color: filterACF.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    text: qsTr("Modulation")
                    onClicked: filterModulation.open()

                    contentItem: Label {
                        text: filterModulation.isFilterActive
                            ? qsTr("Modulation ●")
                            : qsTr("Modulation")

                        color: filterModulation.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    text: qsTr("Category")
                    onClicked: filterCategory.open()

                    contentItem: Label {
                        text: filterCategory.isFilterActive
                            ? qsTr("Category ●")
                            : qsTr("Category")

                        color: filterCategory.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    text: qsTr("Location")
                    onClicked: filterLocation.open()

                    contentItem: Label {
                        text: filterLocation.isFilterActive
                            ? qsTr("Location ●")
                            : qsTr("Location")

                        color: filterLocation.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuSeparator {}

                MenuItem {
                    id: resetFilterMenu
                    enabled: true
                    text: "Reset all filters"
                    onClicked: {resetFilters()}
                } 
            }

            Menu {
                title: qsTr("Space Weather")
                MenuItem { text: "Check Report"; onClicked: showSpaceWeather() }
            }

            Menu {
                id: aboutMenu
                title: updateAvailable ? qsTr("Help ●") : qsTr("Help")

                MenuItem {
                    id: checkForUpdatesItem
                    onClicked: checkForUpdate()
                    text: qsTr("Check for Updates")

                    contentItem: Label {
                        text: checkForUpdatesItem.enabled
                            ? qsTr("Check for Updates ●")
                            : qsTr("Check for Updates")

                        color: checkForUpdatesItem.enabled
                            ? Material.color(Material.Red)
                            : Material.foreground
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
                        highlightMoveDuration: 0
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

                                color: listView.currentIndex === index ? contrastTextColor(Material.accent) : Material.foreground
                                font.weight: listView.currentIndex === index ? Font.Bold : Font.Normal
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
            SignalPage {
                id: signalPage
                SplitView.fillWidth: true
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }
}
