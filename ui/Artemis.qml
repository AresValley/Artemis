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
    title: "Artemis"
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
    property var filterDict: ({})
    property bool updateAvailable: false
    property var currentSelectedSignal: null

    // MARK: Functions
    function lockMenu(is_db_loaded, is_sigid) {
        openFileMenu.enabled = !is_db_loaded
        exportFileMenu.enabled = !is_db_loaded
        signalMenu.enabled = !is_db_loaded
        filterMenu.enabled = !is_db_loaded
        editCategoryMenu.enabled = !is_db_loaded
        filterSinceVersionMenu.enabled = is_sigid
        if (is_db_loaded) {bottomInfoBar('','info')}
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
            if (data[0].since_version) filterSinceVersion.populate(data[0].since_version);
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
        filterSinceVersion.resetToDefault();
        applyFilter({});
    }

    function anyFilterActive() {
        return filterLocation.isFilterActive || 
            filterCategory.isFilterActive || 
            filterModulation.isFilterActive ||
            filterFrequency.isFilterActive ||
            filterBandwidth.isFilterActive ||
            filterACF.isFilterActive ||
            filterSinceVersion.isFilterActive
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

    UIComponents.FilterListDialog {
        id: filterSinceVersion
        objectName: "sinceVersionDialogObj"
        title: qsTr("Filter by DB version")
        
        onFilterApplied: function(selectedValues) {
            if (isFilterActive && selectedValues && selectedValues.length > 0) {
                filterDict["since_version"] = selectedValues;
            } else {
                delete filterDict["since_version"];
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

    // MARK: Export DB
    FileDialog {
        id: exportDialog
        title: qsTr("Please choose a save folder...")
        fileMode: FileDialog.SaveFile
        nameFilters: ["All files (*)"]
        onAccepted: {
            operationPopup.message = qsTr("Exporting...")
            operationPopup.open()
            exportTimer.start()
        }
    }

    Timer {
        id: exportTimer
        interval: 50
        repeat: false
        onTriggered: {
            exportDb(exportDialog.selectedFile)
            operationPopup.close()
        }
    }

    // MARK: Import DB
    FileDialog {
        id: importDialog
        title: qsTr("Please choose a valid tar.gz archive...")
        fileMode: FileDialog.OpenFile
        nameFilters: ["All files (*)"]
        onAccepted: {
            operationPopup.message = "Importing..."
            operationPopup.open()
            importTimer.start()
        }
    }

    Timer {
        id: importTimer
        interval: 50
        repeat: false
        onTriggered: {
            importDb(importDialog.selectedFile)
            operationPopup.close()
        }
    }

    Popup {
        id: operationPopup

        property alias message: popupText.text

        anchors.centerIn: parent
        width: 200
        height: 80
        modal: true
        focus: true
        closePolicy: Popup.NoAutoClose

        background: Rectangle {
            color: "#333333"
            radius: 8
            border.color: "#555555"
            border.width: 1
        }

        Text {
            id: popupText
            text: ""
            color: "white"
            font.pointSize: 14
            font.bold: true
            anchors.centerIn: parent
        }
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

        Keys.onDownPressed: customSignalList.incrementCurrentIndex()
        Keys.onUpPressed: customSignalList.decrementCurrentIndex()

        header: MenuBar {
            id: topBar
            background: Rectangle {
                    color: Material.backgroundColor
                }

            delegate: MenuBarItem {
                id: menuBarItem
                enabled: menuBarItem.menu ? menuBarItem.menu.enabled : true
                opacity: menuBarItem.enabled ? 1.0 : 0.5
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
                MenuItem { text: qsTr("New Database"); onClicked: dialogNewDb.open() }
                MenuItem { text: qsTr("Load Database"); onClicked: showDBmanager() }
                MenuSeparator {}
                MenuItem { id: importFileMenu; text: qsTr("Import Database"); onClicked: importDialog.open() }
                MenuItem { id: exportFileMenu; text: qsTr("Export Database"); onClicked: exportDialog.open(); enabled: false }
                MenuSeparator {}
                MenuItem { id: editCategoryMenu; text: qsTr("Edit Tags"); onClicked: showCatManager(); enabled: false }
                MenuSeparator {}
                MenuItem { id: openFileMenu; text: qsTr("Open Database Folder"); onClicked: openDbDirectory(); enabled: false }
                MenuItem { text: qsTr("Preferences"); onClicked: showPref() }
                MenuItem { text: qsTr("Exit"); onClicked: close() }
            }

            Menu {
                id: signalMenu
                title: qsTr("Edit")
                enabled: false

                MenuItem {
                    id: newSignalMenu
                    text: qsTr("New Signal")
                    onClicked: openSigEditor('Signal', [], true)
                }

                MenuItem {
                    id: editSignalMenu
                    text: qsTr("Edit Name/Description")
                    onClicked: {
                        if (currentSelectedSignal) {
                            openSigEditor('Signal', currentSelectedSignal, false)
                        }
                    }
                }

                MenuSeparator {}

                MenuItem {
                    id: newFrequencyMenu
                    text: qsTr("Add Frequency")
                    onClicked: openSigEditor('Frequency', [], true)
                }

                MenuItem {
                    id: newBandMenu
                    text: qsTr("Add Bandwidth")
                    onClicked: openSigEditor('Bandwidth', [], true)
                }

                MenuItem {
                    id: newModulationMenu
                    text: qsTr("Add Modulation")
                    onClicked: openSigEditor('Modulation', [], true)
                }

                MenuItem {
                    id: newModeMenu
                    text: qsTr("Add Mode")
                    onClicked: openSigEditor('Mode', [], true)
                }

                MenuItem {
                    id: newACFMenu
                    text: qsTr("Add ACF")
                    onClicked: openSigEditor('ACF', [], true)
                }

                MenuItem {
                    id: newLocationMenu
                    text: qsTr("Add Location")
                    onClicked: openSigEditor('Location', [], true)
                }
            }

            Menu {
                id: filterMenu
                title: anyFilterActive() ? qsTr("Filter •") : qsTr("Filter")
                enabled: false
                MenuItem {
                    text: qsTr("Frequency")
                    onClicked: filterFrequency.open()

                    contentItem: Label {
                        text: filterFrequency.isFilterActive
                            ? qsTr("Frequency •")
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
                            ? qsTr("Bandwidth •")
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
                            ? qsTr("ACF •")
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
                            ? qsTr("Modulation •")
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
                            ? qsTr("Category •")
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
                            ? qsTr("Location •")
                            : qsTr("Location")

                        color: filterLocation.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuItem {
                    id: filterSinceVersionMenu
                    text: qsTr("DB version")
                    onClicked: filterSinceVersion.open()

                    contentItem: Label {
                        text: filterSinceVersion.isFilterActive
                            ? qsTr("DB version •")
                            : qsTr("DB version")

                        color: filterSinceVersion.isFilterActive
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuSeparator {}

                MenuItem {
                    id: resetFilterMenu
                    enabled: true
                    text: qsTr("Reset all filters")
                    onClicked: {resetFilters()}
                } 
            }

            Menu {
                title: qsTr("Space Weather")
                MenuItem { text: qsTr("Check Report"); onClicked: showSpaceWeather() }
            }

            Menu {
                id: aboutMenu
                title: updateAvailable ? qsTr("Help •") : qsTr("Help")

                MenuItem {
                    id: checkForUpdatesItem
                    onClicked: checkForUpdate()
                    text: qsTr("Check for Updates")

                    contentItem: Label {
                        text: updateAvailable
                            ? qsTr("Check for Updates •")
                            : qsTr("Check for Updates")

                        color: updateAvailable
                            ? Material.color(Material.Red)
                            : Material.foreground
                    }
                }

                MenuSeparator {}

                MenuItem {
                    text: qsTr("Project Homepage")
                    onClicked: {Qt.openUrlExternally('https://aresvalley.com/')}
                }

                MenuItem {
                    text: qsTr("Documentation")
                    onClicked: {Qt.openUrlExternally('https://AresValley.github.io/Artemis')}
                }

                MenuItem {
                    text: qsTr("Show Release Notes")
                    onClicked: {Qt.openUrlExternally('https://github.com/AresValley/Artemis/blob/master/CHANGELOG.md')}
                }

                MenuSeparator {}

                MenuItem {
                    text: qsTr("Report Issue")
                    onClicked: {Qt.openUrlExternally('https://github.com/AresValley/Artemis/issues')}
                }

                MenuSeparator {}
                MenuItem { text: qsTr("About"); onClicked: aboutDialog.open() }
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

            handle: Rectangle {
                implicitWidth: 4
                color: SplitHandle.pressed ? Qt.lighter(Material.accent, 1.0)
                    : (SplitHandle.hovered ? Qt.lighter(Material.accent, 1.5) : "transparent")
            }

            Item {
                SplitView.preferredWidth: 250
                SplitView.minimumWidth: 200
                SplitView.maximumWidth: 450

                UIComponents.ArtemisListView {
                    id: customSignalList
                    objectName: "signalListObj"

                    anchors.fill: parent
                    anchors.rightMargin: 10

                    onItemSelected: (selectedItem) => {
                        currentSelectedSignal = selectedItem
                        loadSignal(selectedItem.sig_id) 
                        editSignalMenu.enabled = true
                        newFrequencyMenu.enabled = true
                        newBandMenu.enabled = true
                        newModeMenu.enabled = true
                        newModulationMenu.enabled = true
                        newACFMenu.enabled = true
                        newLocationMenu.enabled = true
                    }

                    onSelectionCleared: {
                        currentSelectedSignal = null
                        editSignalMenu.enabled = false
                        newFrequencyMenu.enabled = false
                        newBandMenu.enabled = false
                        newModeMenu.enabled = false
                        newModulationMenu.enabled = false
                        newACFMenu.enabled = false
                        newLocationMenu.enabled = false
                    }
                }
            }

            // MARK: Right panel
            Item {
                SplitView.fillWidth: true
                SignalPage {
                    anchors.fill: parent
                    anchors.leftMargin: 10
                }
            }
        }
    }
}
