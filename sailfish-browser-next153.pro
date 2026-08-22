TEMPLATE = subdirs
SUBDIRS += apps tests settings backup-unit

tests.depends = apps

# The .desktop file
desktop.files = sailfish-browser-next153.desktop sailfish-captiveportal-next153.desktop
desktop.path = /usr/share/applications

dbus_service.files = org.sailfishos.browsernext153.service \
                     org.sailfishos.browsernext153.ui.service \
                     org.sailfishos.captiveportalnext153.service
dbus_service.path = /usr/share/dbus-1/services

chrome_scripts.files = chrome/*.js
chrome_scripts.path = $$[QT_INSTALL_LIBS]/mozembedlite/chrome/embedlite/content

oneshots.files = oneshot.d/browser-next153-cleanup-startup-cache \
                 oneshot.d/browser-next153-update-default-data
oneshots.path  = /usr/lib/oneshot.d

data.files = data/prefs.js \
             data/ua-update.json.in
data.path = /usr/share/sailfish-browser-next153/data

INSTALLS += desktop dbus_service chrome_scripts oneshots data

usersession.path = /usr/lib/systemd/user/user-session.target.d
usersession.files += 50-sailfish-browser-next153.conf
INSTALLS += usersession

OTHER_FILES += \
    rpm/*.spec
