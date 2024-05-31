import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

Page {
    id: spaceWeatherCurrent
    anchors.fill: parent

    objectName: "spaceWeatherForecastObj"

    function loadForecastReport(poseidon_data) {
        if (poseidon_data['FORCST']['SUMMARY']['G_REPORT'][0] === 1) {
            imageAttentionGReport.source = "qrc:/images/icons/dialog_warn.svg"
        } else {
            imageAttentionGReport.source = "qrc:/images/icons/dialog_info.svg"
        }
        labelGReport.text = poseidon_data['FORCST']['SUMMARY']['G_REPORT'][1]

        if (poseidon_data['FORCST']['SUMMARY']['S_REPORT'][0] === 1) {
            imageAttentionSReport.source = "qrc:/images/icons/dialog_warn.svg"
        } else {
            imageAttentionSReport.source = "qrc:/images/icons/dialog_info.svg"
        }
        labelSReport.text = poseidon_data['FORCST']['SUMMARY']['S_REPORT'][1]

        if (poseidon_data['FORCST']['SUMMARY']['R_REPORT'][0] === 1) {
            imageAttentionRReport.source = "qrc:/images/icons/dialog_warn.svg"
        } else {
            imageAttentionRReport.source = "qrc:/images/icons/dialog_info.svg"
        }
        labelRReport.text = poseidon_data['FORCST']['SUMMARY']['R_REPORT'][1]

        labelDay1kp.text = poseidon_data['FORCST']['SUMMARY']['PRE_DATES'][0]
        labelDay2kp.text = poseidon_data['FORCST']['SUMMARY']['PRE_DATES'][1]
        labelDay3kp.text = poseidon_data['FORCST']['SUMMARY']['PRE_DATES'][2]

        var timeRanges = ['00-03UT', '03-06UT', '06-09UT', '09-12UT', '12-15UT', '15-18UT', '18-21UT', '21-00UT']

        for (var i = 0; i < timeRanges.length; i++) {
            var timeRange = timeRanges[i]
            for (var j = 0; j < 3; j++) {
                var index = j.toString()
                var labelName = 'labelKp' + (i).toString() + (j+1).toString()
                var labelText = poseidon_data['FORCST']['SUMMARY']['kp'][timeRange][j]['textual']
                var colorText = poseidon_data['FORCST']['SUMMARY']['kp'][timeRange][j]['color']

                eval(labelName + '.text = labelText')
                if (colorText !== '') {
                    eval(labelName + '.color = colorText')
                }
            }
        }    

        labelDay1Event.text = poseidon_data['FORCST']['PRE_DATES'][0]
        labelDay2Event.text = poseidon_data['FORCST']['PRE_DATES'][1]
        labelDay3Event.text = poseidon_data['FORCST']['PRE_DATES'][2]

        labelEventS10.text = poseidon_data['FORCST']['SUMMARY']['S_PROB']['probS1'][0] + ' %'
        labelEventS11.text = poseidon_data['FORCST']['SUMMARY']['S_PROB']['probS1'][1] + ' %'
        labelEventS12.text = poseidon_data['FORCST']['SUMMARY']['S_PROB']['probS1'][2] + ' %'

        labelEventMFlare0.text = poseidon_data['FORCST']['CLASS_M'][0] + ' %'
        labelEventMFlare1.text = poseidon_data['FORCST']['CLASS_M'][1] + ' %'
        labelEventMFlare2.text = poseidon_data['FORCST']['CLASS_M'][2] + ' %'

        labelEventXFlare0.text = poseidon_data['FORCST']['CLASS_X'][0] + ' %'
        labelEventXFlare1.text = poseidon_data['FORCST']['CLASS_X'][1] + ' %'
        labelEventXFlare2.text = poseidon_data['FORCST']['CLASS_X'][2] + ' %'

        labelEventPFlare0.text = poseidon_data['FORCST']['CLASS_PROTON'][0] + ' %'
        labelEventPFlare1.text = poseidon_data['FORCST']['CLASS_PROTON'][1] + ' %'
        labelEventPFlare2.text = poseidon_data['FORCST']['CLASS_PROTON'][2] + ' %'

        labelEventR1R20.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR1'][0] + ' %'
        labelEventR1R21.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR1'][1] + ' %'
        labelEventR1R22.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR1'][2] + ' %'

        labelEventR30.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR3'][0] + ' %'
        labelEventR31.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR3'][1] + ' %'
        labelEventR32.text = poseidon_data['FORCST']['SUMMARY']['R_PROB']['probR3'][2] + ' %'

        var geoActiveM0 = poseidon_data['FORCST']['GEO_MID_ACTIVE'][0] + ' %'
        var geoActiveM1 = poseidon_data['FORCST']['GEO_MID_ACTIVE'][1] + ' %'
        var geoActiveM2 = poseidon_data['FORCST']['GEO_MID_ACTIVE'][2] + ' %'

        var geoActiveH0 = poseidon_data['FORCST']['GEO_HIG_ACTIVE'][0] + ' %'
        var geoActiveH1 = poseidon_data['FORCST']['GEO_HIG_ACTIVE'][1] + ' %'
        var geoActiveH2 = poseidon_data['FORCST']['GEO_HIG_ACTIVE'][2] + ' %'

        var geoMinorM0 = poseidon_data['FORCST']['GEO_MID_MINOR'][0] + ' %'
        var geoMinorM1 = poseidon_data['FORCST']['GEO_MID_MINOR'][1] + ' %'
        var geoMinorM2 = poseidon_data['FORCST']['GEO_MID_MINOR'][2] + ' %'

        var geoMinorH0 = poseidon_data['FORCST']['GEO_HIG_MINOR'][0] + ' %'
        var geoMinorH1 = poseidon_data['FORCST']['GEO_HIG_MINOR'][1] + ' %'
        var geoMinorH2 = poseidon_data['FORCST']['GEO_HIG_MINOR'][2] + ' %'

        var geoMajorM0 = poseidon_data['FORCST']['GEO_MID_MAJOR'][0] + ' %'
        var geoMajorM1 = poseidon_data['FORCST']['GEO_MID_MAJOR'][1] + ' %'
        var geoMajorM2 = poseidon_data['FORCST']['GEO_MID_MAJOR'][2] + ' %'

        var geoMajorH0 = poseidon_data['FORCST']['GEO_HIG_MAJOR'][0] + ' %'
        var geoMajorH1 = poseidon_data['FORCST']['GEO_HIG_MAJOR'][1] + ' %'
        var geoMajorH2 = poseidon_data['FORCST']['GEO_HIG_MAJOR'][2] + ' %'

        labelEventActive0.text = geoActiveM0 + ' / ' + geoActiveH0
        labelEventActive1.text = geoActiveM1 + ' / ' + geoActiveH1
        labelEventActive2.text = geoActiveM2 + ' / ' + geoActiveH2

        labelEventMinor0.text = geoMinorM0 + ' / ' + geoMinorH0
        labelEventMinor1.text = geoMinorM1 + ' / ' + geoMinorH1
        labelEventMinor2.text = geoMinorM2 + ' / ' + geoMinorH2

        labelEventMajor0.text = geoMajorM0 + ' / ' + geoMajorH0
        labelEventMajor1.text = geoMajorM1 + ' / ' + geoMajorH1
        labelEventMajor2.text = geoMajorM2 + ' / ' + geoMajorH2
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.rightMargin: 20
        anchors.leftMargin: 20
        anchors.bottomMargin: 20
        anchors.topMargin: 20

        ColumnLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            Label {
                text: qsTr("FORECAST SUMMARY")
                font.capitalization: Font.SmallCaps
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            Frame {
                Layout.fillWidth: true

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 15

                    RowLayout {
                        spacing: 20

                        Image {
                            id: imageAttentionGReport
                            sourceSize.height: 40
                            sourceSize.width: 40
                            fillMode: Image.PreserveAspectFit
                        }

                        ColumnLayout {
                            Layout.fillHeight: true
                            Layout.fillWidth: true

                            Label {
                                font.capitalization: Font.SmallCaps
                                text: qsTr("Geomagnetic Activity")
                                font.pointSize: 11
                                Layout.fillWidth: true
                            }

                            Label {
                                id: labelGReport
                                wrapMode: Label.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }

                    RowLayout {
                        spacing: 20

                        Image {
                            id: imageAttentionSReport
                            fillMode: Image.PreserveAspectFit
                            sourceSize.height: 40
                            sourceSize.width: 40
                        }

                        ColumnLayout {
                            Layout.fillHeight: true
                            Label {
                                text: qsTr("Solar Radiation Storms")
                                font.pointSize: 11
                                font.capitalization: Font.SmallCaps
                                Layout.fillWidth: true
                            }

                            Label {
                                id: labelSReport
                                wrapMode: Label.WordWrap
                                Layout.fillWidth: true
                            }
                            Layout.fillWidth: true
                        }
                    }

                    RowLayout {
                        spacing: 20

                        Image {
                            id: imageAttentionRReport
                            fillMode: Image.PreserveAspectFit
                            sourceSize.height: 40
                            sourceSize.width: 40
                        }

                        ColumnLayout {
                            Layout.fillHeight: true

                            Label {
                                text: qsTr("Radio Blackouts")
                                font.pointSize: 11
                                font.capitalization: Font.SmallCaps
                                Layout.fillWidth: true
                            }

                            Label {
                                id: labelRReport
                                wrapMode: Label.WordWrap
                                Layout.fillWidth: true
                            }

                            Layout.fillWidth: true
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                Layout.fillHeight: true
                Layout.fillWidth: true

                Label {
                    text: qsTr("3-DAY Kp INDEX")
                    font.capitalization: Font.SmallCaps
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Frame {
                    clip: true
                    Layout.fillHeight: true

                    GridLayout {
                        anchors.fill: parent
                        columnSpacing: 15
                        rows: 9
                        columns: 4

                        Label {
                            text: qsTr("Time (UTC)")
                        }

                        Label {
                            id: labelDay1kp
                            text: qsTr("Day 1")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelDay2kp
                            text: qsTr("Day 2")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelDay3kp
                            text: qsTr("Day 3")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("00-03")
                        }

                        Label {
                            id: labelKp01
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp02
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp03
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("03-06")
                        }

                        Label {
                            id: labelKp11
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp12
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp13
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("06-09")
                        }

                        Label {
                            id: labelKp21
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp22
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp23
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("09-12")
                        }

                        Label {
                            id: labelKp31
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp32
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp33
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("12-15")
                        }

                        Label {
                            id: labelKp41
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp42
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp43
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("15-18")
                        }

                        Label {
                            id: labelKp51
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp52
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp53
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("18-21")
                        }

                        Label {
                            id: labelKp61
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp62
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp63
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            text: qsTr("21-00")
                        }

                        Label {
                            id: labelKp71
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp72
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }

                        Label {
                            id: labelKp73
                            Layout.leftMargin: labelDay1kp.width * 0.3
                            font.pointSize: 12
                            font.bold: true
                        }
                    }
                }
            }

            ColumnLayout {
                Label {
                    text: qsTr("EVENTS PROBABILITY")
                    font.capitalization: Font.SmallCaps
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                }

                Frame {
                    Layout.fillWidth: true
                    GridLayout {
                        anchors.fill: parent
                        rows: 9
                        columnSpacing: 15
                        columns: 4

                        Label {
                        }

                        Label {
                            id: labelDay1Event
                            text: qsTr("Day 1")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelDay2Event
                            text: qsTr("Day 2")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelDay3Event
                            text: qsTr("Day 3")
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Solar Radiation Storm")
                            font.capitalization: Font.SmallCaps
                            font.bold: true
                            Layout.columnSpan: 4
                        }

                        Label {
                            text: qsTr("S1 or greater")
                        }

                        Label {
                            id: labelEventS10
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventS11
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventS12
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Solar Flares")
                            font.capitalization: Font.SmallCaps
                            font.bold: true
                            Layout.columnSpan: 4
                        }

                        Label {
                            text: qsTr("Class M flare")
                        }

                        Label {
                            id: labelEventMFlare0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMFlare1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMFlare2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Class X flare")
                        }

                        Label {
                            id: labelEventXFlare0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventXFlare1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventXFlare2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Proton flare")
                        }

                        Label {
                            id: labelEventPFlare0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventPFlare1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventPFlare2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }


                        Label {
                            text: qsTr("Radio Blackout")
                            font.capitalization: Font.SmallCaps
                            font.bold: true
                            Layout.columnSpan: 4
                        }

                        Label {
                            text: qsTr("R1 - R2")
                        }

                        Label {
                            id: labelEventR1R20
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventR1R21
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventR1R22
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("R3 or greater")
                        }

                        Label {
                            id: labelEventR30
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventR31
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventR32
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Geomagnetic Activity")
                            font.capitalization: Font.SmallCaps
                            font.bold: true
                            Layout.columnSpan: 4
                        }

                        Label {
                            text: qsTr("Active")
                        }

                        Label {
                            id: labelEventActive0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventActive1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventActive2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Minor")
                        }

                        Label {
                            id: labelEventMinor0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMinor1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMinor2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            text: qsTr("Major")
                        }

                        Label {
                            id: labelEventMajor0
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMajor1
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }

                        Label {
                            id: labelEventMajor2
                            font.bold: true
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        }
                    }

                    Layout.fillHeight: true
                    clip: true
                }
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }
}
