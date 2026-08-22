QT += quick

CONFIG += link_pkgconfig
PKGCONFIG += qt5embedwidget-next153

INCLUDEPATH += $$PWD/core $$PWD/storage $$PWD/history $$PWD/qtmozembed $$PWD/factories $$PWD/../common
LIBS += -L$$PWD/lib -lsailfishbrowser-next153
