import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents


Page {
    id: signalPage
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

        if (sig.since_version !== undefined) {
            signalSinceVersionText.text = "v" + sig.since_version
            signalSinceVersionBadge.visible = true
        } else {
            signalSinceVersionBadge.visible = false
        }

        if (freq_lo !== undefined) {
            bandBar.set(freq_lo[1], freq_up[1])
        } else {
            bandBar.reset()
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

        docManagerButton.visible = true
        addTagButton.enabled = true
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
        audioPlayer.resetPlayer()
        image.source = "qrc:///data/images/spectrum_not_available.svg"
        bandBar.reset()
        signalSinceVersionBadge.visible = false
        docManagerButton.visible = false
        addTagButton.enabled = false
    }

    function contrastTextColor(color) {
        let luminance = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return luminance > 0.55 ? "black" : "white"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.rightMargin: 10
        anchors.topMargin: 10

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
                delegate: UIComponents.ArtemisButton {
                    text: modelData[2]
                    Layout.preferredHeight: 30
                    visibleBackground: true

                    ToolTip {
                        visible: hovered
                        text: 'Click to remove'
                    }
                    onClicked: {
                        deleteCatTag(modelData[0])
                    }
                }
            }

            UIComponents.ArtemisButton {
                id: addTagButton
                enabled: false
                Layout.preferredHeight: 30
                Layout.preferredWidth: 30
                visibleBackground: true
                text: '+'
                onClicked: {
                    categoryMenu.open()
                }
                Menu {
                    id: categoryMenu
                    y: addTagButton.height
                    height:300

                    Instantiator {
                        model: allCategoryList

                        delegate: MenuItem {
                            text: modelData.value
                            onTriggered: {addCatTag(modelData.clb_id)}
                        }

                        onObjectAdded: (index, object) => categoryMenu.insertItem(index, object)
                        onObjectRemoved: (index, object) => categoryMenu.removeItem(object)
                    }
                }
            }
        }

        Rectangle {
            id: signalSinceVersionBadge
            color: Qt.alpha(Material.accent, 0.7)
            radius: 4
            implicitWidth: signalSinceVersionText.implicitWidth + 12
            implicitHeight: signalSinceVersionText.implicitHeight + 4
            visible: false
            Layout.alignment: Qt.AlignHCenter
            
            Text {
                id: signalSinceVersionText
                text: ""
                color: contrastTextColor(Material.accent)
                font.pointSize: 9
                anchors.centerIn: parent
                ToolTip.visible: hoverHandler.hovered
                ToolTip.text: qsTr("Signal introduced in database version %1").arg(text)
                HoverHandler {id: hoverHandler}
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
                    text: "-"
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
                    text: "-"
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
                    id: frequencyRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "FREQUENCY"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: frequencyFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: frequencyFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: frequencyList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[3]
                                visibleBackground: true

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
                }

                RowLayout {
                    id: bandwidthRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "BANDWIDTH"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: bandwidthFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: bandwidthFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: bandwidthList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[3]
                                visibleBackground: true

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
                }

                RowLayout {
                    id: modulationRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "MODULATION"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: modulationFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: modulationFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: modulationList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[1]
                                visibleBackground: true

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
                }

                RowLayout {
                    id: modeRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "MODE"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: modeFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: modeFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: modeList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[1]
                                visibleBackground: true

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
                }

                RowLayout {
                    id: acfRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "ACF"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: acfFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: acfFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: acfList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[1]
                                visibleBackground: true

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
                }

                RowLayout {
                    id: locationRow
                    spacing: 15
                    Layout.fillWidth: true

                    Label {
                        text: "LOCATION"
                        font.pixelSize: 14
                        font.bold: true
                        Layout.preferredWidth: 90
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Rectangle {
                        width: 2
                        color: Material.accent
                        Layout.preferredHeight: locationFlow.childrenRect.height 
                        Layout.alignment: Qt.AlignVCenter
                    }

                    Flow {
                        id: locationFlow
                        Layout.fillWidth: true
                        spacing: 5

                        Repeater {
                            model: locationList
                            delegate: UIComponents.ArtemisButton {
                                width: implicitWidth 
                                height: 30
                                text: modelData[1]
                                visibleBackground: true

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
                }

                Flickable {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.topMargin: 5
                    TextArea.flickable: TextArea {
                        id: descriptionTextArea
                        placeholderText: qsTr("Description")
                        font.pointSize: 10
                        wrapMode: TextEdit.WordWrap
                        textFormat: Text.MarkdownText
                        readOnly: true
                        onLinkActivated: (link) => {
                            Qt.openUrlExternally(link)
                        }
                    }
                    ScrollBar.vertical: ScrollBar {
                        width: 10
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

                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    UIComponents.ArtemisButton {
                        id: urlButton
                        text: "Sigid Wiki"
                        icon.source: "qrc:/data/images/icons/browser.svg"
                        display: AbstractButton.TextBesideIcon
                        visible: false
                        Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                        Layout.fillWidth: true
                        onClicked: {
                            Qt.openUrlExternally(urlSigidwiki)
                        }
                    }

                    UIComponents.ArtemisButton {
                        id: docManagerButton
                        text: qsTr("Open Documents")
                        icon.source: "qrc:/data/images/icons/documents.svg"
                        display: AbstractButton.TextBesideIcon
                        visible: false
                        Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                        Layout.fillWidth: true
                        onClicked: {
                            openDocManager()
                        }
                    }
                }
            }
        }
    }
}
