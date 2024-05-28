import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents


Page {
    id: signalPage
    anchors.fill: parent
    objectName: "signalPageObj"

    signal openDocManager()
    signal openSigEditor(string type, var sig_param, bool is_new)
    signal addCatTag(int clbId)
    signal deleteCatTag(int catId)

    property string urlSigidwiki
    property var frequencyList
    property var bandwidthList
    property var categoryList
    property var allCategoryList
    property var modulationList
    property var modeList
    property var acfList
    property var locationList


    function populateSignalParam(sig) {
        var sig = sig[0]
        signalName.text = sig.name
        frequencyList = sig.frequency
        bandwidthList = sig.bandwidth

        var freq_lo = sig.frequency[0]
        var freq_up = sig.frequency.slice(-1)[0]
        var band_lo = sig.bandwidth[0]
        var band_up = sig.bandwidth.slice(-1)[0]

        freqValue.text = format_range(freq_lo, freq_up)
        bandValue.text = format_range(band_lo, band_up)

        categoryList = sig.category
        allCategoryList = sig.all_category
        modeList = sig.mode
        modulationList = sig.modulation
        locationList = sig.location
        acfList = sig.acf

        descriptionTextArea.text = sig.description

        if (freq_lo !== undefined) {
            bandBar.setBandBar(freq_lo[1], freq_up[1])
        }

        if (sig.url !== undefined) {
            urlButton.visible = true
            urlSigidwiki = sig.url
        }
        else {
            urlButton.visible = false
        }

        image.source = sig.spectrum_path

        if (sig.audio_path !== '') {
            loadPlayer(sig.audio_path)
        } else {
            lockPlayer()
        }

        lockMenu(false)
    }

    function format_range(lower_freq, upper_freq) {
        try {
            if (lower_freq[1] !== upper_freq[1]) {
                return lower_freq[3] + ' - ' + upper_freq[3]
            } else {
                return lower_freq[3]
            }
        } catch (error) {
            return 'UNKNOWN'
        }
    }

    function loadPlayer(audio_path) {
        audioPlayer.resetPlayer()
        audioPlayer.loadSound(audio_path)
    }

    function lockPlayer() {
        audioPlayer.resetPlayer()
    }

    function resetAll() {
        signalName.text = ""
        freqValue.text = "-"
        bandValue.text = "-"
        frequencyList = []
        bandwidthList = []
        categoryList = []
        modeList = []
        modulationList = []
        locationList = []
        acfList = []
        descriptionTextArea.text = ""
        bandBar.resetBandBar()
        audioPlayer.resetPlayer()
        image.source = "qrc:///images/spectrum_not_available.svg"
        lockMenu(true)
    }

    function lockMenu(toggle) {
        if (toggle) {
            urlButton.visible = false
            docManagerButton.visible = false
            freqButton.enabled = false
            bandButton.enabled = false
            modulationButton.enabled = false
            modeButton.enabled = false
            acfButton.enabled = false
            locationButton.enabled = false
            addTagButton.enabled = false
        } else {
            docManagerButton.visible = true
            freqButton.enabled = true
            bandButton.enabled = true
            modulationButton.enabled = true
            modeButton.enabled = true
            acfButton.enabled = true
            locationButton.enabled = true
            addTagButton.enabled = true
        }
    }

    Dialog {
        id: dialogAddCategory

        x: (parent.width - width) / 2
        y: (parent.height - height) / 2

        modal: true
        closePolicy: Popup.CloseOnPressOutside

        ColumnLayout {
            anchors.fill: parent

            Repeater {
                model: allCategoryList
                delegate: Button {
                    text: modelData.value
                    Layout.fillWidth: true
                    Layout.preferredHeight: 25
                    highlighted: true
                    bottomInset: 3
                    topInset: 3
                    flat: false
                    onClicked: {
                        addCatTag(modelData.clb_id)
                        dialogAddCategory.close()
                    }
                }
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent

        Label {
            id: signalName
            color: Material.accent
            font.pixelSize: 25
            horizontalAlignment: Text.AlignHCenter
            Layout.topMargin: 10
            Layout.fillHeight: false
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
            clip: true
            Layout.fillWidth: true
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Repeater {
                model: categoryList
                delegate: Button {
                    text: modelData[1]
                    Layout.preferredHeight: 25
                    highlighted: true
                    bottomInset: 3
                    topInset: 3
                    flat: false
                    ToolTip {
                        visible: hovered
                        text: 'Click to remove'
                    }
                    onClicked: {
                        deleteCatTag(modelData[0])
                    }
                }
            }

            Button {
                id: addTagButton
                enabled: false
                Layout.preferredHeight: 25
                Layout.preferredWidth: 25
                bottomInset: 3
                topInset: 3
                text: '+'
                onClicked: {
                    dialogAddCategory.open()
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true


            ColumnLayout {
                Label {
                    color: Material.accent
                    text: qsTr("FREQUENCY RANGE")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }

                Label {
                    id: freqValue
                    color: Material.accent
                    text: qsTr("-")
                    font.pixelSize: 18
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }

            Item {
                Layout.fillWidth: true
            }

            ColumnLayout {
                Label {
                    color: Material.accent
                    text: qsTr("BANDWIDTH RANGE")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }

                Label {
                    id: bandValue
                    color: Material.accent
                    text: qsTr("-")
                    font.pixelSize: 18
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }
        }

        UIComponents.BandBar {
            id: bandBar
            Layout.fillWidth: true
        }


        RowLayout {
            width: 100
            height: 100
            Layout.topMargin: 5
            spacing: 15

            ColumnLayout {
                width: 100
                height: 100

                RowLayout {
                    Button {
                        id: freqButton
                        enabled: false
                        contentItem: Label {
                            text: "FREQUENCY"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        Layout.minimumWidth: 120
                        height: 25
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('Frequency', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: frequencyList
                        delegate: Button {
                            text: modelData[3]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('Frequency', modelData, false)
                            }
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: bandButton
                        enabled: false
                        contentItem: Label {
                            text: "BANDWIDTH"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        Layout.minimumWidth: 120
                        height: 25
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('Bandwidth', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: bandwidthList
                        delegate: Button {
                            text: modelData[3]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('Bandwidth', modelData, false)
                            }
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: modulationButton
                        enabled: false
                        contentItem: Label {
                            text: "MODULATION"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        Layout.minimumWidth: 120
                        height: 25
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('Modulation', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: modulationList
                        delegate: Button {
                            text: modelData[1]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('Modulation', modelData, false)
                            }
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: modeButton
                        enabled: false
                        contentItem: Label {
                            text: "MODE"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        Layout.minimumWidth: 120
                        height: 25
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('Mode', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: modeList
                        delegate: Button {
                            text: modelData[1]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('Mode', modelData, false)
                            }
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: acfButton
                        enabled: false
                        contentItem: Label {
                            text: "ACF"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        height: 25
                        Layout.minimumWidth: 120
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('ACF', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: acfList
                        delegate: Button {
                            text: modelData[1]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('ACF', modelData, false)
                            }
                        }
                    }
                }

                RowLayout {
                    Button {
                        id: locationButton
                        enabled: false
                        contentItem: Label {
                            text: "LOCATION"
                            horizontalAlignment : Text.AlignLeft
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: 14
                            font.bold: true
                        }
                        Layout.minimumWidth: 120
                        height: 25
                        flat: true
                        bottomInset: 0
                        topInset: 0
                        rightPadding: 10
                        leftPadding: 10
                        bottomPadding: 0
                        topPadding: 0
                        onClicked: {
                            openSigEditor('Location', [], true)
                        }
                    }
                    ListView {
                        height: 25
                        Layout.fillWidth: true
                        spacing: 5
                        orientation: ListView.Horizontal
                        clip: true
                        model: locationList
                        delegate: Button {
                            text: modelData[1]
                            height: 25
                            bottomInset: 3
                            topInset: 3
                            flat: false
                            ToolTip {
                                visible: modelData[2] !== '' ? hovered : false
                                text: modelData[2]
                            }
                            onClicked: {
                                openSigEditor('Location', modelData, false)
                            }
                        }
                    }
                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.topMargin: 5
                    Layout.fillHeight: true
                    ScrollBar.vertical.interactive: true

                    TextArea {
                        id: descriptionTextArea
                        wrapMode: TextEdit.WordWrap
                        textFormat: Text.MarkdownText
                        font.pointSize: 10
                        readOnly: true
                    }
                }
            }

            ColumnLayout {
                Layout.fillHeight: true
                Layout.fillWidth: false
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop

                UIComponents.AudioPlayer {
                    id: audioPlayer
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                }

                Image {
                    id: image
                    source: ""
                    Layout.preferredHeight: 300
                    Layout.preferredWidth: 180
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    fillMode: Image.Stretch
                }

                Item {
                    Layout.fillHeight: true
                }

                RowLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    RoundButton {
                        id: urlButton
                        icon.source: "qrc:/images/icons/browser.svg"
                        display: AbstractButton.IconOnly
                        visible: false
                        text: "U"
                        onClicked: {
                            Qt.openUrlExternally(urlSigidwiki)
                        }
                    }

                    RoundButton {
                        id: docManagerButton
                        icon.source: "qrc:/images/icons/documents.svg"
                        display: AbstractButton.IconOnly
                        visible: false
                        text: "D"
                        onClicked: {
                            openDocManager()
                        }
                    }
                }
            }
        }



    }
}
