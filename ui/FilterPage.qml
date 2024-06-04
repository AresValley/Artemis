import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Page {
    id: filterPage
    anchors.fill: parent
    objectName: "filterPageObj"

    signal applyFilter(var filterDict)
    signal sendBottomAlert(string message, string messagType)

    property var filterDict: {}

    function updateFilterDict() {
        filterDict = {}
        if (switchFreq.checked) {
            var unitFreqValue = comboBoxFreq.currentValue.value
            var lower_band = parseFloat(textFieldFreq.text) * unitFreqValue * (1 - tolFreq.value)
            var upper_band = parseFloat(textFieldFreq.text) * unitFreqValue * (1 + tolFreq.value)
            filterDict['frequency'] = {
                'lower_band': lower_band,
                'upper_band': upper_band
            }
        }

        if (switchBand.checked) {
            var unitBandValue = comboBoxBand.currentValue.value
            var lower_band = parseFloat(textFieldBand.text) * unitBandValue * (1 - tolBand.value)
            var upper_band = parseFloat(textFieldBand.text) * unitBandValue * (1 + tolBand.value)
            filterDict['bandwidth'] = {
                'lower_band': lower_band,
                'upper_band': upper_band
            }
        }

        if (switchACF.checked) {
            var lower_band = parseFloat(textFieldACF.text) * (1 - tolACF.value)
            var upper_band = parseFloat(textFieldACF.text) * (1 + tolACF.value)
            filterDict['acf'] = {
                'lower_band': lower_band,
                'upper_band': upper_band
            }
        }

        if (switchModulation.checked) {
            var modulationList = []
            for (var i = 0; i < modelModulation.count; i++) {
                if (modelModulation.get(i).checked) {
                    modulationList.push(
                        modelModulation.get(i).value
                    )
                }
            }
            filterDict['modulation'] = modulationList
        }

        if (switchLocation.checked) {
            var locationList = []
            for (var i = 0; i < modelLocation.count; i++) {
                if (modelLocation.get(i).checked) {
                    locationList.push(
                        modelLocation.get(i).value
                    )
                }
            }
            filterDict['location'] = locationList
        }

        if (switchCategory.checked) {
            var categoryList = []
            for (var i = 0; i < modelCategory.count; i++) {
                if (modelCategory.get(i).checked) {
                    categoryList.push(
                        modelCategory.get(i).clb_id
                    )
                }
            }
            filterDict['category'] = categoryList
        }
        applyFilter(filterDict)
    }

    function resetAll() {
        switchFreq.checked = false
        switchBand.checked = false
        switchACF.checked = false
        switchModulation.checked = false
        switchLocation.checked = false
        switchCategory.checked = false
        lockFreq(true)
        lockBand(true)
        lockACF(true)
    }

    function lockFreq(toggle) {
        if(toggle) {
            textFieldFreq.enabled = false
            comboBoxFreq.enabled = false
            tolFreq.enabled = false
            summaryFreq.text = ''
        }
        else {
            textFieldFreq.enabled = true
            comboBoxFreq.enabled = true
            tolFreq.enabled = true
            if (textFieldFreq.text !== '') {
                updateSummaryFreq()
                updateFilterDict()
            }
        }
    }

    function lockBand(toggle) {
        if(toggle) {
            textFieldBand.enabled = false
            comboBoxBand.enabled = false
            tolBand.enabled = false
            summaryBand.text = ''
        }
        else {
            textFieldBand.enabled = true
            comboBoxBand.enabled = true
            tolBand.enabled = true
            if (textFieldBand.text !== '') {
                updateSummaryBand()
                updateFilterDict()
            }
        }
    }

    function lockACF(toggle) {
        if(toggle) {
            textFieldACF.enabled = false
            tolACF.enabled = false
            summaryACF.text = ''
        }
        else {
            textFieldACF.enabled = true
            tolACF.enabled = true
            if (textFieldACF.text !== '') {
                updateSummaryACF()
                updateFilterDict()
            }
        }
    }

    function updateSummaryFreq() {
        if (textFieldFreq.text !== "") {
            var unitFreqText = comboBoxFreq.currentValue.text
            var lowFreq = (parseFloat(textFieldFreq.text) * (1 - tolFreq.value)).toFixed(1)
            var uppFreq = (parseFloat(textFieldFreq.text) * (1 + tolFreq.value)).toFixed(1)

            if (tolFreq.value === 0) {
                summaryFreq.text = lowFreq + " " + unitFreqText
            }
            else {
                summaryFreq.text = lowFreq + " " + unitFreqText + " - " + uppFreq + " " + unitFreqText
            }
        }
    }

    function updateSummaryBand() {
        if (textFieldBand.text !== "") {
            var unitBandText = comboBoxBand.currentValue.text
            var lowBand = (parseFloat(textFieldBand.text) * (1 - tolBand.value)).toFixed(1)
            var uppBand = (parseFloat(textFieldBand.text) * (1 + tolBand.value)).toFixed(1)

            if (tolBand.value === 0) {
                summaryBand.text = lowBand + " " + unitBandText
            }
            else {
                summaryBand.text = lowBand + " " + unitBandText + " - " + uppBand + " " + unitBandText
            }
        }
    }

    function updateSummaryACF() {
        if (textFieldACF.text !== "") {
            var lowBand = (parseFloat(textFieldACF.text) * (1 - tolACF.value)).toFixed(1)
            var uppBand = (parseFloat(textFieldACF.text) * (1 + tolACF.value)).toFixed(1)

            if (tolACF.value === 0) {
                summaryACF.text = lowBand + " ms"
            }
            else {
                summaryACF.text = lowBand + " ms" + " - " + uppBand + " ms" 
            }
        }
    }

    function loadLists(filterList) {
        modelModulation.clear()
        var modulationDict = filterList[0].modulation
        for (var i = 0; i < modulationDict.length; i++) {
            modelModulation.append(modulationDict[i])
        }

        modelLocation.clear()
        var locationDict = filterList[0].location
        for (var i = 0; i < locationDict.length; i++) {
            modelLocation.append(locationDict[i])
        }

        modelCategory.clear()
        var categoryDict = filterList[0].category
        for (var i = 0; i < categoryDict.length; i++) {
            modelCategory.append(categoryDict[i])
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.topMargin: 10

        GridLayout {
            rows: 2
            columns: 3
            rowSpacing: 10
            columnSpacing: 10

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("Frequency")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }

                        Switch {
                            id: switchFreq
                            onToggled: {
                                if(switchFreq.checked) {
                                    lockFreq(false)
                                }
                                else {
                                    lockFreq(true)
                                    updateFilterDict()
                                }
                            }
                        }
                    }

                    RowLayout {
                        TextField {
                            id: textFieldFreq
                            Layout.fillWidth: true
                            placeholderText: qsTr("Frequency")
                            validator: DoubleValidator{bottom: 0}
                            enabled: false
                            onTextChanged: {
                                if(switchFreq.checked && textFieldFreq.text !== '') {
                                    updateSummaryFreq()
                                    updateFilterDict()
                                }
                            }
                        }

                        ComboBox {
                            id: comboBoxFreq
                            enabled: false
                            textRole: 'text'
                            model:  ListModel {
                                ListElement { text: "Hz"; value: 1 }
                                ListElement { text: "kHz"; value: 1e3 }
                                ListElement { text: "MHz"; value: 1e6 }
                                ListElement { text: "GHz"; value: 1e9 }
                            }
                            onActivated: {
                                if(switchFreq.checked && textFieldFreq.text !== '') {
                                    updateSummaryFreq()
                                    updateFilterDict()
                                }
                            }
                        }
                    }

                    Slider {
                        id: tolFreq
                        Layout.fillWidth: true
                        enabled: false
                        value: 0
                        onValueChanged: {
                            if(switchFreq.checked && textFieldFreq.text !== '') {
                                updateSummaryFreq()
                                updateFilterDict()
                            }
                        }
                    }

                    Label {
                        id: summaryFreq
                        color: Material.color(Material.Green)
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("Bandwidth")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }

                        Switch {
                            id: switchBand
                            onToggled: {
                                if(switchBand.checked) {
                                    lockBand(false)
                                }
                                else {
                                    lockBand(true)
                                    updateFilterDict()
                                }
                            }
                        }
                    }

                    RowLayout {
                        TextField {
                            id: textFieldBand
                            validator: DoubleValidator {
                                bottom: 0
                            }
                            onTextChanged: {
                                if(switchBand.checked && textFieldBand.text !== '') {
                                    updateSummaryBand()
                                    updateFilterDict()
                                }
                            }
                            Layout.fillWidth: true
                            placeholderText: qsTr("Bandwidth")
                            enabled: false
                        }

                        ComboBox {
                            id: comboBoxBand
                            enabled: false
                            textRole: 'text'
                            model:  ListModel {
                                ListElement { text: "Hz"; value: 1 }
                                ListElement { text: "kHz"; value: 1e3 }
                                ListElement { text: "MHz"; value: 1e6 }
                                ListElement { text: "GHz"; value: 1e9 }
                            }
                            onActivated: {
                                if(switchBand.checked && textFieldBand.text !== '') {
                                    updateSummaryBand()
                                    updateFilterDict()
                                }
                            }
                        }
                    }

                    Slider {
                        id: tolBand
                        Layout.fillWidth: true
                        enabled: false
                        value: 0
                        onValueChanged: {
                            if(switchBand.checked && textFieldBand.text !== '') {
                                updateSummaryBand()
                                updateFilterDict()
                            }
                        }
                    }
                    Label {
                        id: summaryBand
                        color: Material.color(Material.Green)
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("ACF")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }

                        Switch {
                            id: switchACF
                            onToggled: {
                                if(switchACF.checked) {
                                    lockACF(false)
                                } else {
                                    lockACF(true)
                                    updateFilterDict()
                                }
                            }
                        }
                    }

                    RowLayout {
                        TextField {
                            id: textFieldACF
                            validator: DoubleValidator {
                                bottom: 0
                            }
                            onTextChanged: {
                                if(switchACF.checked && textFieldACF.text !== '') {
                                    updateSummaryACF()
                                    updateFilterDict()
                                }
                            }
                            Layout.fillWidth: true
                            placeholderText: qsTr("ACF")
                            enabled: false
                        }

                        ComboBox {
                            enabled: false
                            model: ['ms']
                        }
                    }

                    Slider {
                        id: tolACF
                        Layout.fillWidth: true
                        enabled: false
                        value: 0
                        onValueChanged: {
                            if(switchACF.checked && textFieldACF.text !== '') {
                                updateSummaryACF()
                                updateFilterDict()
                            }
                        }
                    }
                    Label {
                        id: summaryACF
                        color: Material.color(Material.Green)
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("Modulation")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }
                        Switch {
                            id: switchModulation
                            onToggled: {
                                updateFilterDict()
                            }
                        }
                    }

                    ListView {
                        Layout.minimumHeight: 200
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        highlightMoveDuration: 0
                        clip: true
                        focus: true
                        ScrollBar.vertical: ScrollBar {
                            active: true
                        }
                        delegate: Item {
                            width: ListView.view.width
                            height: 30
                            CheckBox {
                                enabled: switchModulation.checked
                                text: value
                                onCheckedChanged: {
                                    modelModulation.setProperty(index, "checked", checked)
                                    updateFilterDict()
                                }
                            }
                        }
                        model: ListModel {
                            id: modelModulation
                        }
                    }
                }
            }

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("Location")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }
                        Switch {
                            id: switchLocation
                            onToggled: {
                                updateFilterDict()
                            }
                        }
                    }

                    ListView {
                        Layout.minimumHeight: 200
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        highlightMoveDuration: 0
                        clip: true
                        focus: true
                        ScrollBar.vertical: ScrollBar {
                            active: true
                        }
                        delegate: Item {
                            width: ListView.view.width
                            height: 30
                            CheckBox {
                                enabled: switchLocation.checked
                                text: value
                                onCheckedChanged: {
                                    modelLocation.setProperty(index, "checked", checked)
                                    updateFilterDict()
                                }
                            }
                        }
                        model: ListModel {
                            id: modelLocation
                        }
                    }
                }
            }

            GroupBox {
                Layout.fillHeight: true
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent

                    RowLayout {
                        Label {
                            text: qsTr("Category")
                            Layout.fillWidth: true
                            font.bold: true
                            font.pointSize: 12
                            font.capitalization: Font.SmallCaps
                        }
                        Switch {
                            id: switchCategory
                            onToggled: {
                                updateFilterDict()
                            }
                        }
                    }

                    ListView {
                        Layout.minimumHeight: 200
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        highlightMoveDuration: 0
                        clip: true
                        focus: true
                        ScrollBar.vertical: ScrollBar {
                            active: true
                        }
                        delegate: Item {
                            width: ListView.view.width
                            height: 30
                            CheckBox {
                                enabled: switchCategory.checked
                                text: value
                                onCheckedChanged: {
                                    modelCategory.setProperty(index, "checked", checked)
                                    updateFilterDict()
                                }
                            }
                        }
                        model: ListModel {
                            id: modelCategory
                        }
                    }
                }
            }
        }
    }
}
