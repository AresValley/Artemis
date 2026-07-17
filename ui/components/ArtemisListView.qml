import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material

ColumnLayout {
    id: root

    // Internal/external property to store the original items list
    property var loadedList: []

    // Component events to communicate with the main application layer
    signal itemSelected(var itemObj)
    signal selectionCleared()

    // Public function to populate the list from the outside
    function populateList(itemsList) {
        loadedList = itemsList
        textFieldSearch.enabled = true
        var currentIndex = listView.currentIndex
        refreshList()
        if (currentIndex >= 0 && currentIndex < listModel.count) {
            listView.currentIndex = currentIndex
        }
    }

    // Public function to clear the list from the outside
    function clearList() {
        listModel.clear()
        loadedList = []
        textFieldSearch.clear()
        textFieldSearch.enabled = false
    }

    // Internal function to filter AND SORT the list items via search field
    function refreshList() {
        listModel.clear()
        if (!loadedList) return

        var search = textFieldSearch.text.toLowerCase().trim()
        var filteredList = []

        // 1. Filtring
        for (var i = 0; i < loadedList.length; i++) {
            var name = loadedList[i].name ? loadedList[i].name.toLowerCase() : ""
            var description = loadedList[i].description ? loadedList[i].description.toLowerCase() : ""
            
            if (search === "") {
                filteredList.push(loadedList[i])
            } else if (name.includes(search) || description.includes(search)) {
                filteredList.push(loadedList[i])
            }
        }

        // 2. Sorting (taking into account types/section AND alphabetically by name)
        filteredList.sort(function(a, b) {
            var typeA = (a.type || "").toLowerCase()
            var typeB = (b.type || "").toLowerCase()
            
            var typeCompare = typeA.localeCompare(typeB)

            if (typeCompare !== 0) {
                return typeCompare
            }

            var nameA = (a.name || "").toLowerCase()
            var nameB = (b.name || "").toLowerCase()
            return nameA.localeCompare(nameB)
        })

        // 3. Populating
        for (var k = 0; k < filteredList.length; k++) {
            listModel.append(filteredList[k])
        }

        itemChangedList()
    }

    // Internal function to handle list selection changes
    function itemChangedList() {
        var selectedItem = listModel.get(listView.currentIndex)
        if (selectedItem !== undefined && selectedItem !== null) {
            root.itemSelected(selectedItem)
        } else {
            root.selectionCleared()
        }
    }

    // Utility function to calculate contrasting text color based on background luminance
    function contrastTextColor(color) {
        let luminance = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return luminance > 0.55 ? "black" : "white"
    }

    function incrementCurrentIndex() {
        if (listView.currentIndex < listView.count - 1) {
            listView.currentIndex++;
        }
    }

    function decrementCurrentIndex() {
        if (listView.currentIndex > 0) {
            listView.currentIndex--;
        }
    }

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

            // Sections
            section.property: "type" // Group from type property
            section.criteria: ViewSection.FullString
            
            // Graphic delegate of the section
            section.delegate: Rectangle {
                width: listView.width
                height: 32
                color: "transparent"

                Label {
                    text: section.toUpperCase()
                    font.bold: true
                    font.pixelSize: 11
                    font.letterSpacing: 1.0
                    color: Material.accent
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.bottomMargin: 4
                }
            }

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
