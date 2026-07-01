import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Dialog {
    id: root
    modal: true
    standardButtons: Dialog.Ok | Dialog.Cancel

    anchors.centerIn: Overlay.overlay
    width: Math.min(parent.width * 0.8, 400)

    contentHeight: dialogLayout.implicitHeight + 24

    signal filterApplied(var selectedValues)

    property var originalCheckedStates: []
    property bool originalSwitchState: false
    property alias isFilterActive: switchActive.checked
    property alias filterModel: modelItems

    function populate(itemList) {
        modelItems.clear();
        if (!itemList) return;

        var arr = Array.from(itemList);
        for (var i = 0; i < arr.length; i++) {
            if (arr[i] !== undefined && arr[i] !== null) {
                var val = (arr[i].value !== undefined) ? arr[i].value : arr[i];
                modelItems.append({
                    "value": val,
                    "checked": false
                });
            }
        }
    }

    function resetToDefault() {
        switchActive.checked = false;
        for (var i = 0; i < modelItems.count; i++) {
            modelItems.setProperty(i, "checked", false);
        }
    }

    header: Item {
        width: parent.width
        height: 48 

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            anchors.topMargin: 12
            anchors.bottomMargin: 4

            Label {
                text: root.title
                font.pointSize: 14
                Layout.fillWidth: true
                verticalAlignment: Text.AlignVCenter 
            }

            Switch {
                id: switchActive
                Layout.alignment: Qt.AlignVCenter
            }
        }
    }

    ColumnLayout {
        id: dialogLayout

        anchors.fill: parent
        spacing: 12

        ListView {
            id: listViewItems
            Layout.fillWidth: true
            Layout.preferredHeight: 200
            
            opacity: switchActive.checked ? 1.0 : 0.5
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            ScrollBar.vertical: ScrollBar { 
                policy: ScrollBar.AlwaysOn
                implicitWidth: 8
                active: true
            }

            delegate: CheckBox {
                enabled: switchActive.checked
                text: model.value 
                checked: model.checked ?? false

                height: 36 

                onClicked: {
                    if (modelItems.get(index)) {
                        modelItems.setProperty(index, "checked", checked)
                    }
                }
            }
            model: ListModel { id: modelItems }
        }
    }

    onOpened: {
        originalSwitchState = switchActive.checked
        originalCheckedStates = []
        for (var i = 0; i < modelItems.count; i++) {
            originalCheckedStates.push(modelItems.get(i).checked)
        }
    }

    onAccepted: {
        var selectedList = []
        if (switchActive.checked) {
            for (var i = 0; i < modelItems.count; i++) {
                if (modelItems.get(i).checked) { 
                    selectedList.push(modelItems.get(i).value) 
                }
            }
        }
        filterApplied(selectedList)
    }

    onRejected: {
        switchActive.checked = originalSwitchState
        for (var i = 0; i < modelItems.count; i++) {
            if (i < originalCheckedStates.length) {
                modelItems.setProperty(i, "checked", originalCheckedStates[i])
            }
        }
    }
}
