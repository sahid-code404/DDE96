import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import org.kde.plasma.plasmoid 2.0
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: launcherRoot
    preferredRepresentation: compactRepresentation

    compactRepresentation: Item {
        width: 24
        height: 24
        Kirigami.Icon {
            anchors.centerIn: parent
            width: 18
            height: 18
            source: "system-search"
        }
        MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: launcherRoot.expanded = !launcherRoot.expanded
        }
    }

    fullRepresentation: Rectangle {
        implicitWidth: 640
        implicitHeight: 460
        radius: 20
        color: Qt.rgba(0.12, 0.12, 0.14, 0.94)
        border.color: Qt.rgba(1.0, 1.0, 1.0, 0.16)
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 18
            spacing: 14

            // Spotlight Search Header
            RowLayout {
                Layout.fillWidth: true
                spacing: 10

                Kirigami.Icon {
                    width: 22
                    height: 22
                    source: "system-search"
                }

                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: "Spotlight Search (apps, documents, calculations)..."
                    font.pixelSize: 16
                    color: "#ffffff"
                    background: Rectangle { color: "transparent" }
                    focus: true
                }
            }

            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: Qt.rgba(1.0, 1.0, 1.0, 0.1)
            }

            // Results List
            ListView {
                id: resultsList
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 6

                model: [
                    { "name": "Glasswave Files", "desc": "Finder-like File Manager", "icon": "glasswave-files", "exec": "glasswave-files" },
                    { "name": "Glasswave Terminal", "desc": "Translucent Shell Terminal", "icon": "glasswave-terminal", "exec": "glasswave-terminal" },
                    { "name": "Glasswave Settings", "desc": "Appearance and System Control Center", "icon": "glasswave-settings", "exec": "glasswave-settings" },
                    { "name": "Glasswave Calculator", "desc": "Safe Scientific Calculator", "icon": "glasswave-calculator", "exec": "glasswave-calculator" },
                    { "name": "Glasswave Activity Monitor", "desc": "System Statistics & Process Viewer", "icon": "glasswave-monitor", "exec": "glasswave-monitor" },
                    { "name": "Glasswave Screenshot", "desc": "Wayland Screen Capture HUD", "icon": "glasswave-screenshot", "exec": "glasswave-screenshot" }
                ]

                delegate: Rectangle {
                    width: resultsList.width
                    height: 48
                    radius: 10
                    color: itemMouse.containsMouse ? Qt.rgba(0.04, 0.52, 1.0, 0.35) : "transparent"

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 12

                        Kirigami.Icon {
                            width: 32
                            height: 32
                            source: modelData.icon
                        }

                        ColumnLayout {
                            spacing: 1
                            Text { text: modelData.name; color: "#ffffff"; font.bold: true; font.pixelSize: 13 }
                            Text { text: modelData.desc; color: "#a0a0a5"; font.pixelSize: 11 }
                        }
                    }

                    MouseArea {
                        id: itemMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            launcherRoot.expanded = false;
                        }
                    }
                }
            }
        }
    }
}
