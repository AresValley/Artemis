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

    contentHeight: dialogLayout.height + 24

    signal filterApplied(var lowerBand, var upperBand)

    property bool originalSwitchState: false
    property string originalText: ""
    property int originalUnitIndex: 1
    property real originalSliderValue: 0.0

    property string field_label: ""
    property bool isTimeField: false

    property alias isFilterActive: switchActive.checked

    function setup(active, valueText, unitIndex, tolerance) {
        switchActive.checked = active
        textFieldInput.text = valueText
        comboBoxUnit.currentIndex = unitIndex
        toleranceSlider.value = tolerance
    }

    function resetToDefault() {
        switchActive.checked = false
        textFieldInput.text = ""
        comboBoxUnit.currentIndex = 1
        toleranceSlider.value = 0.0
    }

    function updateSummary() {
        if (textFieldInput.text === "" || isNaN(parseFloat(textFieldInput.text))) {
            summaryLabel.text = ""
            return
        }

        var unitText = comboBoxUnit.currentText
        var rawValue = parseFloat(textFieldInput.text)
        var lowVal = (rawValue * (1 - toleranceSlider.value)).toFixed(1)
        var uppVal = (rawValue * (1 + toleranceSlider.value)).toFixed(1)

        if (toleranceSlider.value === 0) {
            summaryLabel.text = lowVal + " " + unitText
        } else {
            summaryLabel.text = lowVal + " " + unitText + " - " + uppVal + " " + unitText
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

    Column {
        id: dialogLayout
        width: parent.width
        spacing: 16
        opacity: switchActive.checked ? 1.0 : 0.5

        RowLayout {
            width: parent.width
            spacing: 8

            TextField {
                id: textFieldInput
                Layout.fillWidth: true
                placeholderText: root.field_label
                enabled: switchActive.checked
                inputMethodHints: Qt.ImhFormattedNumbersOnly
                validator: DoubleValidator { bottom: 0 }
                
                onTextChanged: root.updateSummary()
            }

            ComboBox {
                id: comboBoxUnit
                enabled: switchActive.checked && !root.isTimeField
                textRole: "text"
                valueRole: "value"

                ListModel {
                    id: frequencyModel
                    ListElement { text: "Hz"; value: 1 }
                    ListElement { text: "kHz"; value: 1e3 }
                    ListElement { text: "MHz"; value: 1e6 }
                    ListElement { text: "GHz"; value: 1e9 }
                }

                ListModel {
                    id: timeModel
                    ListElement { text: "ms"; value: 1 }
                }

                model: root.isTimeField ? timeModel : frequencyModel

                onCurrentTextChanged: root.updateSummary()
            }
        }

        Column {
            width: parent.width
            spacing: 4

            Label {
                text: qsTr("Tolerance: ") + (toleranceSlider.value * 100).toFixed(0) + "%"
                font.pointSize: 10
                font.bold: true
                opacity: 0.8
            }

            Slider {
                id: toleranceSlider
                width: parent.width
                enabled: switchActive.checked
                from: 0.0
                to: 0.5 
                stepSize: 0.01
                value: 0.0
                
                onValueChanged: root.updateSummary()
            }
        }

        Label {
            id: summaryLabel
            width: parent.width
            height: 32
            color: Material.accent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pointSize: 15
            font.bold: true

            bottomPadding: 8 
        }
    }

    onOpened: {
        originalSwitchState = switchActive.checked
        originalText = textFieldInput.text
        originalUnitIndex = comboBoxUnit.currentIndex
        originalSliderValue = toleranceSlider.value
        updateSummary()
    }

    onAccepted: {
        if (switchActive.checked && textFieldInput.text !== "") {
            var unitValue = comboBoxUnit.currentValue
            var rawValue = parseFloat(textFieldInput.text) * unitValue
 
            var lower_band = rawValue * (1 - toleranceSlider.value)
            var upper_band = rawValue * (1 + toleranceSlider.value)

            filterApplied(lower_band, upper_band)
        } else {
            filterApplied(null, null)
        }
    }

    onRejected: {
        switchActive.checked = originalSwitchState
        textFieldInput.text = originalText
        comboBoxUnit.currentIndex = originalUnitIndex
        toleranceSlider.value = originalSliderValue
    }
}