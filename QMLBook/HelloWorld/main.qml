import QtQuick 2.4
import QtQuick.Window 2.2

Window {
    visible: true

    width: 600
    height: 600
    color: "#D8D8D8"

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onClicked: Qt.quit()
    }

    Image {
        id: app
        x: (parent.width - width)/2
        y: 10
        source: "assets/test.jpg"
    }

    Text {
        width: parent.width
        horizontalAlignment: Text.AlignHCenter
        y: app.y + app.height + 40
        text: "Hello World"
        color: "blue"
    }
}
