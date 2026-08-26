/****************************************************************************
**
** Copyright (c) 2026 Sebastian Matkovich
**
****************************************************************************/

/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this file,
 * You can obtain one at http://mozilla.org/MPL/2.0/. */

import QtQuick 2.0
import Sailfish.Silica 1.0
import SailfishNext153.WebEngine 1.0

Page {
    id: page

    property bool observerAdded

    function requestList() {
        if (!observerAdded) {
            WebEngine.addObserver("embed:addons")
            observerAdded = true
        }
        WebEngine.notifyObservers("embedui:addons", { msg: "list" })
    }

    Component.onCompleted: requestList()

    ListModel { id: addonsModel }

    SilicaListView {
        anchors.fill: parent
        model: addonsModel

        header: PageHeader {
            //% "Extensions"
            title: qsTrId("sailfish_browser-he-extensions")
        }

        delegate: ListItem {
            id: item
            contentHeight: column.height + Theme.paddingMedium * 2
            menu: contextMenuComponent

            Column {
                id: column
                x: Theme.horizontalPageMargin
                y: Theme.paddingMedium
                width: parent.width - Theme.horizontalPageMargin * 2 - toggle.width

                Label {
                    width: parent.width
                    text: model.name
                    truncationMode: TruncationMode.Fade
                    color: item.highlighted ? Theme.highlightColor : Theme.primaryColor
                }
                Label {
                    width: parent.width
                    text: model.version + (model.enabled ? "" : " \u2013 " +
                          //% "disabled"
                          qsTrId("sailfish_browser-la-extension_disabled"))
                    font.pixelSize: Theme.fontSizeExtraSmall
                    color: item.highlighted ? Theme.secondaryHighlightColor
                                            : Theme.secondaryColor
                    truncationMode: TruncationMode.Fade
                }
            }

            TextSwitch {
                id: toggle
                anchors {
                    right: parent.right
                    rightMargin: Theme.horizontalPageMargin
                    verticalCenter: parent.verticalCenter
                }
                automaticCheck: false
                checked: model.enabled
                onClicked: WebEngine.notifyObservers("embedui:addons",
                                                     { msg: "setEnabled",
                                                       id: model.id,
                                                       enabled: !model.enabled })
            }

            Component {
                id: contextMenuComponent
                ContextMenu {
                    MenuItem {
                        //% "Remove"
                        text: qsTrId("sailfish_browser-me-remove_extension")
                        onClicked: WebEngine.notifyObservers("embedui:addons",
                                                             { msg: "uninstall",
                                                               id: model.id })
                    }
                }
            }
        }

        ViewPlaceholder {
            enabled: addonsModel.count === 0
            //% "No extensions installed"
            text: qsTrId("sailfish_browser-la-no_extensions")
            //% "Copy an .xpi file into the extensions folder of the browser profile"
            hintText: qsTrId("sailfish_browser-la-no_extensions_hint")
        }

        VerticalScrollDecorator {}
    }

    Connections {
        target: WebEngine
        onRecvObserve: {
            if (message !== "embed:addons" || data.msg !== "list") {
                return
            }
            addonsModel.clear()
            for (var i = 0; i < data.addons.length; ++i) {
                addonsModel.append(data.addons[i])
            }
        }
    }
}
