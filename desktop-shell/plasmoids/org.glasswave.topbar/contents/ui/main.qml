import QtQuick 2.15
import QtQuick.Layouts 1.15
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core as PlasmaCore
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: topBarApplet
    preferredRepresentation: fullRepresentation

    property string activeTitle: "Finder"

    fullRepresentation: RowLayout {
        spacing: 12
        Layout.fillHeight: true

        // Brand Mark Icon / Launcher trigger
        Item {
            width: 20
            height: 20
            Layout.alignment: Qt.AlignVCenter

            Kirigami.Icon {
                anchors.fill: parent
                source: "distributor-logo"
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    // Trigger Spotlight Launcher
                }
            }
        }

        // Active Application Title (Bold macOS style)
        Text {
            text: topBarApplet.activeTitle
            font.bold: true
            font.pixelSize: 13
            color: "#ffffff"
            Layout.alignment: Qt.AlignVCenter
        }
    }
}
