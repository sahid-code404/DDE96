import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami

Kirigami.FormLayout {
    id: configPage

    property alias cfg_iconSize: iconSizeSlider.value
    property alias cfg_magnification: zoomSlider.value
    property alias cfg_autohide: autohideCheck.checked

    Slider {
        id: iconSizeSlider
        Kirigami.FormData.label: "Icon Size:"
        from: 32
        to: 96
        stepSize: 4
        value: 52
    }

    Slider {
        id: zoomSlider
        Kirigami.FormData.label: "Hover Magnification:"
        from: 1.0
        to: 1.8
        stepSize: 0.05
        value: 1.35
    }

    CheckBox {
        id: autohideCheck
        Kirigami.FormData.label: "Auto-hide:"
        text: "Hide dock when windows overlap"
        checked: false
    }
}
