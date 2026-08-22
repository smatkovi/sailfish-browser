TEMPLATE = lib
TARGET = browsersettingsplugin
TARGET = $$qtLibraryTarget($$TARGET)

MODULENAME = org/sailfishos/browsernext153/settings
TARGETPATH = $$[QT_INSTALL_QML]/$$MODULENAME

QT += qml
CONFIG += plugin

import.files = qmldir
import.path = $$TARGETPATH
target.path = $$TARGETPATH

SOURCES +=  plugin.cpp

qmlpages.path = /usr/share/jolla-settings/pages/browser-next153
qmlpages.files = browser.qml

plugin_entry.path = /usr/share/jolla-settings/entries
plugin_entry.files = browser-next153.json

INSTALLS += target import plugin_entry qmlpages

OTHER_FILES += *.qml *.json

# Translations
TS_PATH = $$PWD
TS_FILE = $$OUT_PWD/settings-sailfish-browser-next153.ts
EE_QM = $$OUT_PWD/settings-sailfish-browser-next153_eng_en.qm
include(../translations/translations.pri)
