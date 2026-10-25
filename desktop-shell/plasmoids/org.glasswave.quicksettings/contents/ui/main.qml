import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import org.kde.plasma.plasmoid 2.0
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: qsRoot

    preferredRepresentation: compactRepresentation

    compactRepresentation: Item {
        width: 24
        height: 24
        Kirigami.Icon {
            anchors.centerIn: parent
            width: 18
            height: 18
            source: "preferences-system"
        }
        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: qsRoot.expanded = !qsRoot.expanded
        }
    }

    fullRepresentation: Rectangle {
        id: popoverSurface
        implicitWidth: 320
        implicitHeight: 380
        radius: 18
        color: Qt.rgba(0.12, 0.12, 0.14, 0.92)
        border.color: Qt.rgba(1.0, 1.0, 1.0, 0.14)
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 14
            spacing: 12

            // Top Quick Toggles Grid (2x2)
            GridLayout {
                columns: 2
                Layout.fillWidth: true
                columnSpacing: 10
                rowSpacing: 10

                // Wi-Fi Card
                Rectangle {
                    Layout.fillWidth: true
                    height: 54
                    radius: 14
                    color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 8
                        Rectangle {
                            width: 32; height: 32; radius: 16
                            color: "#0a84ff"
                            Kirigami.Icon { anchors.centerIn: parent; width: 18; height: 18; source: "network-wireless" }
                        }
                        ColumnLayout {
                            spacing: 1
                            Text { text: "Wi-Fi"; color: "#fff"; font.bold: true; font.pixelSize: 12 }
                            Text { text: "Connected"; color: "#a0a0a5"; font.pixelSize: 10 }
                        }
                    }
                }

                // Bluetooth Card
                Rectangle {
                    Layout.fillWidth: true
                    height: 54
                    radius: 14
                    color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 8
                        Rectangle {
                            width: 32; height: 32; radius: 16
                            color: "#0a84ff"
                            Kirigami.Icon { anchors.centerIn: parent; width: 18; height: 18; source: "preferences-system-bluetooth" }
                        }
                        ColumnLayout {
                            spacing: 1
                            Text { text: "Bluetooth"; color: "#fff"; font.bold: true; font.pixelSize: 12 }
                            Text { text: "On"; color: "#a0a0a5"; font.pixelSize: 10 }
                        }
                    }
                }

                // Dark Mode Card
                Rectangle {
                    Layout.fillWidth: true
                    height: 54
                    radius: 14
                    color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 8
                        Rectangle {
                            width: 32; height: 32; radius: 16
                            color: "#5e5ce6"
                            Kirigami.Icon { anchors.centerIn: parent; width: 18; height: 18; source: "weather-clear-night" }
                        }
                        ColumnLayout {
                            spacing: 1
                            Text { text: "Dark Mode"; color: "#fff"; font.bold: true; font.pixelSize: 12 }
                            Text { text: "Active"; color: "#a0a0a5"; font.pixelSize: 10 }
                        }
                    }
                }

                // Do Not Disturb Card
                Rectangle {
                    Layout.fillWidth: true
                    height: 54
                    radius: 14
                    color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 8
                        Rectangle {
                            width: 32; height: 32; radius: 16
                            color: "#48484a"
                            Kirigami.Icon { anchors.centerIn: parent; width: 18; height: 18; source: "notifications-disabled" }
                        }
                        ColumnLayout {
                            spacing: 1
                            Text { text: "Focus / DND"; color: "#fff"; font.bold: true; font.pixelSize: 12 }
                            Text { text: "Off"; color: "#a0a0a5"; font.pixelSize: 10 }
                        }
                    }
                }
            }

            // Display Brightness Slider Card
            Rectangle {
                Layout.fillWidth: true
                height: 58
                radius: 14
                color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 2
                    Text { text: "Display"; color: "#a0a0a5"; font.pixelSize: 11 }
                    Slider {
                        Layout.fillWidth: true
                        from: 0.1; to: 1.0; value: 0.85
                    }
                }
            }

            // Sound Volume Slider Card
            Rectangle {
                Layout.fillWidth: true
                height: 58
                radius: 14
                color: Qt.rgba(0.18, 0.18, 0.20, 0.8)
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 2
                    Text { text: "Sound"; color: "#a0a0a5"; font.pixelSize: 11 }
                    Slider {
                        Layout.fillWidth: true
                        from: 0.0; to: 1.0; value: 0.65
                    }
                }
            }
        }
    }
}
