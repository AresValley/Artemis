import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import './components' as UIComponents


Page {
    id: spaceWeatherCurrent
    anchors.fill: parent

    objectName: "spaceWeatherCurrentObj"

    property string g_now_text
    property string s_now_text
    property string r_now_text

    function loadReport(poseidon_data) {
        setLight(lightG_now, 'G', poseidon_data['GSR_SCALES']['G_now'])
        setLight(lightS_now, 'S', poseidon_data['GSR_SCALES']['S_now'])
        setLight(lightR_now, 'R', poseidon_data['GSR_SCALES']['R_now'])

        setLight(lightG_24h, 'G', poseidon_data['GSR_SCALES']['G_max24h'])
        setLight(lightS_24h, 'S', poseidon_data['GSR_SCALES']['S_max24h'])
        setLight(lightR_24h, 'R', poseidon_data['GSR_SCALES']['R_max24h'])

        g_now_text = poseidon_data['GSR_SCALES']['G_now_text']
        s_now_text = poseidon_data['GSR_SCALES']['S_now_text']
        r_now_text = poseidon_data['GSR_SCALES']['R_now_text']

        kIndexLightPanel.setLights(poseidon_data['AK']['k_index_round'])
        labelKIndex.text = 'Kp Index: ' + poseidon_data['AK']['k_index']

        aIndexLightPanel.setLights(poseidon_data['AK']['a_index'])
        labelAIndex.text = 'A Index: ' + poseidon_data['AK']['a_index']

        labelMux.text = poseidon_data['PROPAGATION']['MUX']
        labelEME.text = poseidon_data['PROPAGATION']['EME']
        labelMS.text = poseidon_data['PROPAGATION']['MS']
        labelHfNoise.text = poseidon_data['AK']['exp_noise']

        labelPeakFluxClass.text = poseidon_data['XRAY']['peak_flux_class']
        labelPeakFluxClass3h.text = poseidon_data['XRAY']['peak_flux_class_3h']
        labelPeakFluxClass24h.text = poseidon_data['XRAY']['peak_flux_class_24h']
    }

    function setLight(lightId, type, level) {
        lightId.text = type + level

        if (level === 0) {

        } else if (level === 1) {
            lightId.Material.background = Material.Green
        } else if (level === 2) {
            lightId.Material.background = Material.Amber
        } else if (level === 3) {
            lightId.Material.background = Material.Orange
        } else if (level === 4) {
            lightId.Material.background = Material.DeepOrange
        } else if (level === 5) {
            lightId.Material.background = Material.Red
        }
    }

    DialogMessage {
        id: gsrDialog
        standardButtons: Dialog.Ok
    }


    Page {
        anchors.fill: parent

        RowLayout {
            anchors.fill: parent
            anchors.rightMargin: 20
            anchors.leftMargin: 20
            anchors.bottomMargin: 20
            anchors.topMargin: 20

            ColumnLayout {
                Layout.fillHeight: true
                Label {
                    id: labelKIndex
                    text: qsTr("Kp Index:")
                    font.pointSize: 11
                    font.capitalization: Font.SmallCaps
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }
                UIComponents.KIndexLight {
                    id: kIndexLightPanel
                    width: 250
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true

                ColumnLayout {

                    Label {
                        text: qsTr("NOAA SPACE WEATHER SCALE")
                        font.letterSpacing: 0.5
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    }

                    Frame {
                        clip: true
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            rows: 5
                            columns: 3

                            Label {
                                width: parent.width /3
                                text: qsTr("Geomagnetic Storm")
                                font.capitalization: Font.SmallCaps
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            }

                            Label {
                                text: qsTr("Solar Radiation Storms")
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                text: qsTr("Radio Blackout")
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                            }

                            Item {
                            }

                            Label {
                                text: qsTr("Current")
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.pointSize: 8
                            }

                            Item {
                            }

                            Button {
                                id: lightG_now
                                text: qsTr("G")
                                font.pixelSize: 15
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                                display: AbstractButton.TextOnly
                                ToolTip.visible: hovered
                                ToolTip.text: qsTr("Click for details")
                                onClicked: {
                                    gsrDialog.title = "Geomagnetic Storms"
                                    gsrDialog.message = g_now_text
                                    gsrDialog.open()
                                }
                            }

                            Button {
                                id: lightS_now
                                text: qsTr("S")
                                font.pixelSize: 15
                                display: AbstractButton.TextOnly
                                onClicked: {
                                    gsrDialog.title = "Solar Radiation Storms"
                                    gsrDialog.message = s_now_text
                                    gsrDialog.open()
                                }
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                                ToolTip.visible: hovered
                                ToolTip.text: qsTr("Click for details")
                            }

                            Button {
                                id: lightR_now
                                text: qsTr("R")
                                font.pixelSize: 15
                                display: AbstractButton.TextOnly
                                onClicked: {
                                    gsrDialog.title = "Radio Blackout"
                                    gsrDialog.message = r_now_text
                                    gsrDialog.open()
                                }
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                                ToolTip.visible: hovered
                                ToolTip.text: qsTr("Click for details")
                            }

                            Item {
                            }

                            Label {
                                text: qsTr("24h Maximums")
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.pointSize: 8
                            }

                            Item {
                            }

                            Button {
                                id: lightG_24h
                                text: qsTr("G")
                                font.pixelSize: 15
                                display: AbstractButton.TextOnly
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                            }

                            Button {
                                id: lightS_24h
                                text: qsTr("S")
                                font.pixelSize: 15
                                display: AbstractButton.TextOnly
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                            }

                            Button {
                                id: lightR_24h
                                text: qsTr("R")
                                font.pixelSize: 15
                                display: AbstractButton.TextOnly
                                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                font.bold: true
                            }
                        }
                    }
                }

                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                    Label {
                        text: qsTr("X-RAY SOLAR ACTIVITY")
                        font.letterSpacing: 0.5
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    }

                    Frame {
                        clip: true
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            columnSpacing: 15
                            columns: 2
                            rows: 2

                            Label {
                                text: qsTr("Current Flux Class:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelPeakFluxClass
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                                font.pointSize: 12
                            }

                            Label {
                                text: qsTr("Peak 3h Flux Class:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelPeakFluxClass3h
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                                font.pointSize: 12
                            }

                            Label {
                                text: qsTr("Peak 24h Flux Class:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelPeakFluxClass24h
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                                font.pointSize: 12
                            }
                        }
                    }
                }

                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                    Label {
                        text: qsTr("RF PROPAGATION")
                        font.letterSpacing: 0.5
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    }

                    Frame {
                        clip: true
                        Layout.fillWidth: true

                        GridLayout {
                            anchors.fill: parent
                            columnSpacing: 15
                            rows: 2
                            columns: 2

                            Label {
                                text: qsTr("MUX (MHz):")
                            }

                            Label {
                                id: labelMux
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                                font.pointSize: 12
                            }

                            Label {
                                text: qsTr("Earth-Moon-Earth:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelEME
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.pointSize: 12
                                font.bold: true
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                text: qsTr("Meteor Scatter:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelMS
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.pointSize: 12
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                            }

                            Label {
                                text: qsTr("Expected HF Noise:")
                                font.capitalization: Font.SmallCaps
                            }

                            Label {
                                id: labelHfNoise
                                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                                font.pointSize: 12
                                font.capitalization: Font.SmallCaps
                                font.bold: true
                            }
                        }
                    }
                }

                Item {
                    Layout.fillHeight: true
                    Layout.fillWidth: true
                }
            }

            ColumnLayout {
                Label {
                    id: labelAIndex
                    text: qsTr("A Index:")
                    font.pointSize: 11
                    font.capitalization: Font.SmallCaps
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }
                UIComponents.AIndexLight {
                    id: aIndexLightPanel
                    width: 250
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }
            }
        }
    }
}
