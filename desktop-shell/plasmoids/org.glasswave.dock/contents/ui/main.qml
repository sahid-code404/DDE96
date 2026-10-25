import QtQuick 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root
    preferredRepresentation: fullRepresentation

    property int baseIconSize: Plasmoid.configuration.iconSize || 52
    property real magnificationFactor: Plasmoid.configuration.magnification || 1.35
    property bool autohide: Plasmoid.configuration.autohide || false
    property int hoveredIndex: -1
    property real hoverPos: -1

    // Default Pinned Apps
    property var defaultApps: [
        { "name": "Files", "icon": "glasswave-files", "exec": "glasswave-files" },
        { "name": "Terminal", "icon": "glasswave-terminal", "exec": "glasswave-terminal" },
        { "name": "Settings", "icon": "glasswave-settings", "exec": "glasswave-settings" },
        { "name": "Calculator", "icon": "glasswave-calculator", "exec": "glasswave-calculator" },
        { "name": "Activity Monitor", "icon": "glasswave-monitor", "exec": "glasswave-monitor" },
        { "name": "Screenshot", "icon": "glasswave-screenshot", "exec": "glasswave-screenshot" }
    ]

    fullRepresentation: Item {
        id: container
        implicitWidth: dockPill.width + 32
        implicitHeight: baseIconSize + 28

        Rectangle {
            id: dockPill
            anchors.centerIn: parent
            width: itemsRow.width + 24
            height: baseIconSize + 16
            radius: 22
            color: Qt.rgba(0.11, 0.11, 0.12, 0.82)
            border.color: Qt.rgba(1.0, 1.0, 1.0, 0.15)
            border.width: 1

            // Mouse Tracker for Smooth Magnification
            MouseArea {
                id: dockMouseArea
                anchors.fill: parent
                hoverEnabled: true
                propagateComposedEvents: true

                onPositionChanged: function(mouse) {
                    root.hoverPos = mouse.x;
                    var localIdx = Math.floor((mouse.x - 12) / (root.baseIconSize + 10));
                    root.hoveredIndex = Math.max(0, Math.min(itemsRepeater.count - 1, localIdx));
                }

                onExited: {
                    root.hoveredIndex = -1;
                    root.hoverPos = -1;
                }
            }

            Row {
                id: itemsRow
                anchors.centerIn: parent
                spacing: 10

                Repeater {
                    id: itemsRepeater
                    model: root.defaultApps

                    DockItem {
                        appData: modelData
                        itemIndex: index
                        baseSize: root.baseIconSize
                        maxZoom: root.magnificationFactor
                        activeHoverIndex: root.hoveredIndex
                    }
                }
            }
        }
    }
}
