import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


Window {
    id: windowSignalEditor

    width: 500
    height: 400

    Component.onCompleted: {
        x = Screen.width / 2 - width / 2
        y = Screen.height / 2 - height / 2
    }

    modality: Qt.ApplicationModal
    flags: Qt.Window

    signal saveParam(string type, var data, bool isNew)
    signal deleteParam(string type, int ID)

    property string paramType
    property int paramID
    property bool isNew

    property var validator_freq: /^\d+(\.\d+)?$/
    property var validator_all: /.*/


    function load(type, sig_param, is_new) {
        clearAll()
        isNew = is_new
        paramType = type

        paramValue.placeholderText = paramType

        if (isNew) {
            paramID = 0
            windowSignalEditor.title = 'Artemis - New ' + paramType
        } else {
            paramID = sig_param[0]
            windowSignalEditor.title = 'Artemis - Edit ' + paramType
            if (paramType === 'Frequency' || paramType === 'Bandwidth') {
                var freq = changeUnit(sig_param[1])
                paramValue.text = sig_param[1] / freq.scale
                loadUnitComboBox(freq.unit)
            } else {
                paramValue.text = sig_param[1]
            }
            paramDescription.text = sig_param[2]
        }
    }

    function save() {
        if (paramType === 'Frequency' || paramType === 'Bandwidth') {
            var scaleFactor = unitComboBox.currentValue.value
            var mainValue = paramValue.text * scaleFactor
        } else {
            var mainValue = paramValue.text
        }
        var param = [paramID, mainValue, paramDescription.text]
        saveParam(paramType, param, isNew)
        changeSavedDialog.open()
    }

    function clearAll() {
        paramValue.clear()
        paramDescription.clear()
        loadUnitComboBox('Hz')
    }

    function changeUnit(frequency) {
        var digits = frequency.toString().length

        if (digits < 4)
            return { scale: 1, unit: "Hz" }
        else if (digits < 7)
            return { scale: Math.pow(10, 3), unit: "kHz" }
        else if (digits < 10)
            return { scale: Math.pow(10, 6), unit: "MHz" }
        else
            return { scale: Math.pow(10, 9), unit: "GHz" }
    }

    function loadUnitComboBox(unit) {
        for (var idx = 0; idx < unitComboBox.count; idx ++) {
            if (unit === unitComboBox.valueAt(idx).text) {
                unitComboBox.currentIndex = idx
                break
            }
        }
    }

    DialogMessage {
        id: changeSavedDialog
        title: 'Change Saved!'
        message: 'Your changes have been successfully saved!'
        standardButtons: Dialog.Ok

        onAccepted: {
            windowSignalEditor.close()
        }
    }

    DialogMessage {
        id: dialogDeleteConfirmation
        modal: true
        title: "Are you sure?"
        message: "You are about to delete the selected " + paramType + ". The process cannot be undone."
        messageType: "warn"
        standardButtons: Dialog.Cancel | Dialog.Yes

        onAccepted: {
            deleteParam(paramType, paramID)
            windowSignalEditor.close()
        }
    }

    Page {
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 10
            anchors.bottomMargin: 10

            RowLayout {

                TextField {
                    id: paramValue
                    visible: paramType !== 'Description' ? true : false
                    Layout.fillWidth: true
                    placeholderText: qsTr("Frequency")
                    validator: RegularExpressionValidator {
                        regularExpression: paramType === 'Frequency' || paramType === 'Bandwidth' ? validator_freq : validator_all
                    }
                }

                ComboBox {
                    id: unitComboBox
                    visible: paramType === 'Frequency' || paramType === 'Bandwidth' ? true : false
                    textRole: 'text'
                    model: ListModel {
                        ListElement { text: 'Hz'; value: 1 }
                        ListElement { text: 'kHz'; value: 1e3 }
                        ListElement { text: 'MHz'; value: 1e6 }
                        ListElement { text: 'GHz'; value: 1e9 }
                    }
                }
            }

            ScrollView {
                Layout.fillWidth: true
                Layout.topMargin: 5
                Layout.fillHeight: true
                ScrollBar.vertical.interactive: true

                TextArea {
                    id: paramDescription
                    placeholderText: qsTr("Description")
                    wrapMode: TextEdit.WordWrap
                    font.pointSize: 10
                }
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.fillWidth: true

                Button {
                    id: deleteButton
                    visible: isNew ? false : true
                    text: qsTr("Delete")
                    icon.source: "qrc:/images/icons/delete.svg"
                    display: AbstractButton.TextBesideIcon
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    onClicked: {
                        dialogDeleteConfirmation.open()
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

                Button {
                    id: saveButton
                    text: qsTr("Save")
                    icon.source: "qrc:/images/icons/save.svg"
                    display: AbstractButton.TextBesideIcon
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    onClicked: {
                        save()
                    }
                }
            }
        }
    }
}
