%global min_xulrunner_version 115.35.1
%global min_qtmozembed_version 1.56.0
%global min_embedlite_components_version 2.0.0
%global min_sailfishwebengine_version 1.7.0

%global captiveportal sailfish-captiveportal-next153

Name:       sailfish-browser-next153

Summary:    Sailfish Browser
Version:    3.0.0
Release:    5
License:    MPLv2.0
Url:        https://github.com/sailfishos/sailfish-browser-next153
Source0:    %{name}-%{version}.tar.bz2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(qt5embedwidget-next153) >= %{min_qtmozembed_version}
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(nemotransferengine-qt5)
BuildRequires:  pkgconfig(mlite5)
BuildRequires:  pkgconfig(qdeclarative5-boostable)
BuildRequires:  pkgconfig(sailfishwebengine-next153) >= %{min_sailfishwebengine_version}
BuildRequires:  pkgconfig(sailfishpolicy)
BuildRequires:  qt5-qttools
BuildRequires:  qt5-qttools-linguist
BuildRequires:  oneshot
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(vault) >= 1.0.1
BuildRequires:  pkgconfig(dsme_dbus_if)

Requires: sailfishsilica-qt5 >= 1.2.33
Requires: sailfish-content-graphics
Requires: xulrunner-qt5-next153 >= %{min_xulrunner_version}
Requires: embedlite-components-qt5-next153 >= %{min_embedlite_components_version}
Requires: qtmozembed-qt5-next153 >= %{min_qtmozembed_version}
Requires: sailfish-components-webview-qt5-next153 >= %{min_sailfishwebengine_version}
Requires: sailfish-components-webview-qt5-next153-popups >= %{min_sailfishwebengine_version}
Requires: sailfish-components-webview-qt5-next153-pickers >= %{min_sailfishwebengine_version}
Requires: qt5-plugin-imageformat-ico
Requires: qt5-plugin-imageformat-gif
Requires: qt5-plugin-position-geoclue
Requires: sailjail-launch-approval
Requires: desktop-file-utils
Requires: qt5-qtgraphicaleffects
Requires: nemo-qml-plugin-policy-qt5 >= 0.0.4
Requires: sailfish-policy >= 0.3.31
Requires: libkeepalive >= 1.7.0
Requires: sailfish-components-pickers-qt5 >= 0.1.7
Requires: nemo-qml-plugin-notifications-qt5 >= 1.0.12
# The stock browser booster preloads the stock engine; a -next153 process would
# then map two libxul copies. The icon starts through D-Bus activation, so the
# booster is not needed here.
Requires: nemo-qml-plugin-connectivity
Requires: jolla-settings >= 0.11.29
Requires: jolla-settings-system >= 1.0.70
Requires: sailfish-policy
Obsoletes: sailfish-browser-next153-settings <= 2.3.29
Provides: sailfish-browser-next153-settings > 2.3.29

%{_oneshot_requires_post}

%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}

%description
Sailfish Web Browser

%package ts-devel
Summary: Translation source for Sailfish browser

%description ts-devel
Translation source for Sailfish Browser

%package tests
Summary: Tests for Sailfish browser
BuildRequires:  pkgconfig(Qt5Test)
Requires:   %{name} = %{version}-%{release}
Requires:   qt5-qtdeclarative-devel-tools
Requires:   qt5-qtdeclarative-import-qttest
Requires:   mce-tools

%description tests
Unit tests and additional data needed for functional tests

%prep
%setup -q -n %{name}-%{version}

%build
%qtc_qmake5 -r VERSION=%{version}
%qtc_make %{?_smp_mflags}

%install
%qmake5_install
chmod +x %{buildroot}/%{_oneshotdir}/*

mkdir -p %{buildroot}/%{_sharedstatedir}/environment/nemo/
cp -f data/70-browser-next153.conf %{buildroot}/%{_sharedstatedir}/environment/nemo/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/172x172/apps
cp -f data/icons/sailfish-browser-next153.png %{buildroot}%{_datadir}/icons/hicolor/172x172/apps/sailfish-browser-next153.png

%post
/sbin/ldconfig || :

# Upgrade, count is 2 or higher (depending on the number of versions installed)
if [ "$1" -ge 2 ]; then
    %{_bindir}/add-oneshot --all-users --now browser-next153-cleanup-startup-cache || :
    %{_bindir}/add-oneshot --new-users --all-users --late browser-next153-update-default-data || :
fi

%postun
/sbin/ldconfig || :

%files
%license LICENSE.txt
%{_bindir}/%{name}
%{_bindir}/%{captiveportal}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/172x172/apps/%{name}.png
%{_datadir}/applications/%{captiveportal}.desktop
%{_datadir}/%{name}
%{_datadir}/%{captiveportal}
%{_datadir}/translations/%{name}*.qm
%{_datadir}/translations/%{captiveportal}*.qm
%{_datadir}/translations/settings-%{name}_eng_en.qm
%{_datadir}/dbus-1/services/*.service
%{_oneshotdir}/*
# Let main package own import root level
%dir %{_libdir}/qt5/qml/org/sailfishos/browsernext153
%{_libdir}/libsailfishbrowser-next153.so.*
%exclude %{_libdir}/libsailfishbrowser-next153.so
%{_sharedstatedir}/environment/nemo/*
%{_libexecdir}/jolla-vault/units/vault-browser-next153
%{_datadir}/jolla-vault/units/BrowserNext153.json
%{_libdir}/qt5/qml/org/sailfishos/browsernext153/settings
%{_datadir}/jolla-settings/entries/browser-next153.json
%{_datadir}/jolla-settings/pages/browser-next153

%files ts-devel
%{_datadir}/translations/source/*.ts

%files tests
%{_datadir}/applications/test-%{name}.desktop
/opt/tests/%{name}

%changelog
* Sun Aug 23 2026 Sebastian Matkovich <sebastianmatkovich@gmail.com> - 3.0.0-3
- Notification permission listed in the site and global permission pages

* Sun Aug 23 2026 Sebastian Matkovich <sebastianmatkovich@gmail.com> - 3.0.0-2
- Show web notifications as system notifications through Nemo.Notifications
- Start without the stock browser booster, which preloads the stock engine
- Request the Notifications sailjail permission
