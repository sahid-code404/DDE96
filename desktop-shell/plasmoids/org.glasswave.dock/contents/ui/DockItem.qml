import QtQuick 2.15
import org.kde.kirigami as Kirigami

Item {
    id: itemRoot
    property var appData
    property int itemIndex: 0
    property int baseSize: 52
    property real maxZoom: 1.35
    property int activeHoverIndex: -1
    property bool isRunning: false
    property bool isBouncing: false

    // Compute magnification scale using smooth distance falloff
    property real targetScale: {
        if (activeHoverIndex < 0) return 1.0;
        var dist = Math.abs(itemIndex - activeHoverIndex);
        if (dist === 0) return maxZoom;
        if (dist === 1) return 1.0 + (maxZoom - 1.0) * 0.45;
        return 1.0;
    }

    width: baseSize
    height: baseSize + 6

    Rectangle {
        id: iconContainer
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 6
        width: baseSize
        height: baseSize
        color: "transparent"
        scale: targetScale

        Behavior on scale {
            NumberAnimation { duration: 120; easing.type: Easing.OutQuad }
        }

        Kirigami.Icon {
            id: appIcon
            anchors.fill: parent
            source: itemRoot.appData.icon || "application-x-executable"
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: {
                itemRoot.triggerBounce();
                // Execute application via KRun / QProcess
                if (itemRoot.appData.exec) {
                    // Signal launch
                    itemRoot.isRunning = true;
                }
            }
        }
    }

    // Running Indicator Dot
    Rectangle {
        id: runningDot
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        width: 4
        height: 4
        radius: 2
        color: Qt.rgba(1.0, 1.0, 1.0, 0.85)
        visible: itemRoot.isRunning
    }

    // Launch Bounce Animation
    SequentialAnimation {
        id: bounceAnim
        running: false
        NumberAnimation { target: iconContainer; property: "y"; to: -18; duration: 150; easing.type: Easing.OutQuad }
        NumberAnimation { target: iconContainer; property: "y"; to: 0; duration: 150; easing.type: Easing.InQuad }
        NumberAnimation { target: iconContainer; property: "y"; to: -8; duration: 100; easing.type: Easing.OutQuad }
        NumberAnimation { target: iconContainer; property: "y"; to: 0; duration: 100; easing.type: Easing.InQuad }
    }

    function triggerBounce() {
        bounceAnim.restart();
    }
}
