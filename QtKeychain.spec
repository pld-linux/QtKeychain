#
# Conditional build:
%bcond_without	qt4	# Qt4 library
%bcond_without	qt5	# Qt5 library

Summary:	Qt API to store passwords and other secret data securely
Summary(pl.UTF-8):	API Qt do bezpiecznego przechowywania haseł i innych tajnych danych
Name:		QtKeychain
Version:	0.9.1
Release:	1
License:	Modified BSD License
Group:		Libraries
#Source0Download: https://github.com/frankosterfeld/qtkeychain/releases
Source0:	https://github.com/frankosterfeld/qtkeychain/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e6921de6f256259784f2a9edd1eeb8f5
Patch0:		%{name}-qt4.patch
URL:		https://github.com/frankosterfeld/qtkeychain
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libsecret-devel
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(find_lang) >= 1.37
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtDBus-devel >= 4
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5DBus-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-linguist >= 5
BuildRequires:	qt5-qmake >= 5
%endif
Requires:	QtKeychain-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QtKeychain a Qt API to store passwords and other secret data securely.

How the data is stored depends on the platform:
- Mac OS X: Passwords are stored in the OS X Keychain.
- Linux/Unix: If running, GNOME Keyring is used, otherwise qtkeychain
  tries to use KWallet (via D-Bus), if available.
- Windows: Windows does not provide a service for secure storage.
  QtKeychain uses the Windows API function

%description -l pl.UTF-8
API Qt do bezpiecznego przechowywania haseł i innych tajnych danych.

Sposób przechowywania danych zależy od platformy:
- Mac OS X: hasła są przechowywanie poprzez usługę OS X Keychain
- Linux/Unix: używany jest GNOME Keyring jeśli jest uruchomiony,
  w przeciwnym wypadku używany jest KWallet (przez DBus), o ile jest
  dostępny
- Windows: system nie udostępnia usługi do bezpiecznego przechowywania
  danych; QtKeychain używa funkcji Windows API

%package devel
Summary:	Development files for QtKeychain
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QtKeychain
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use QtKeychain.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę QtKeychain.

%package common
Summary:	Common data for QtKeychain libraries
Summary(pl.UTF-8):	Wspólne dane dla bibliotek QtKeychain
Group:		Libraries
Conflicts:	QtKeychain < 0.9.1-1

%description common
Common data for QtKeychain libraries (both Qt 4 and Qt 5).

%description common -l pl.UTF-8
Wspólne dane dla bibliotek QtKeychain (zarówno dla Qt 4, jak i Qt 5).

%package -n Qt5Keychain
Summary:	Qt 5 API to store passwords and other secret data securely
Summary(pl.UTF-8):	API Qt 5 do bezpiecznego przechowywania haseł i innych tajnych danych
Group:		Libraries
Requires:	QtKeychain-common = %{version}-%{release}

%description -n Qt5Keychain
QtKeychain a Qt API to store passwords and other secret data securely.

How the data is stored depends on the platform:
- Mac OS X: Passwords are stored in the OS X Keychain.
- Linux/Unix: If running, GNOME Keyring is used, otherwise qtkeychain
  tries to use KWallet (via D-Bus), if available.
- Windows: Windows does not provide a service for secure storage.
  QtKeychain uses the Windows API function

%description -n Qt5Keychain -l pl.UTF-8
API Qt do bezpiecznego przechowywania haseł i innych tajnych danych.

Sposób przechowywania danych zależy od platformy:
- Mac OS X: hasła są przechowywanie poprzez usługę OS X Keychain
- Linux/Unix: używany jest GNOME Keyring jeśli jest uruchomiony,
  w przeciwnym wypadku używany jest KWallet (przez DBus), o ile jest
  dostępny
- Windows: system nie udostępnia usługi do bezpiecznego przechowywania
  danych; QtKeychain używa funkcji Windows API

%package -n Qt5Keychain-devel
Summary:	Development files for Qt5Keychain
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Qt5Keychain
Group:		Development/Libraries
Requires:	Qt5Keychain = %{version}-%{release}

%description -n Qt5Keychain-devel
This package contains the header files for developing applications
that use Qt5Keychain.

%description -n Qt5Keychain-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę Qt5Keychain.

%prep
%setup -q -n qtkeychain-%{version}
%patch0 -p1

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake .. \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DECM_MKSPECS_INSTALL_DIR=%{_datadir}/qt4/mkspecs/modules

%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake .. \
	-DBUILD_WITH_QT4:BOOL=OFF \
	-DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt5/mkspecs/modules
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C build-qt4 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with qt5}
%{__make} -C build-qt5 install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%find_lang qtkeychain --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqtkeychain.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtkeychain.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqtkeychain.so
%{_includedir}/qtkeychain
%{_libdir}/cmake/QtKeychain
%{_datadir}/qt4/mkspecs/modules/qt_QtKeychain.pri
%endif

%files common -f qtkeychain.lang
%defattr(644,root,root,755)
%doc COPYING ChangeLog ReadMe.txt

%if %{with qt5}
%files -n Qt5Keychain
%defattr(644,root,root,755)
%doc COPYING ChangeLog ReadMe.txt
%attr(755,root,root) %{_libdir}/libqt5keychain.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqt5keychain.so.1

%files -n Qt5Keychain-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqt5keychain.so
%{_includedir}/qt5keychain
%{_libdir}/cmake/Qt5Keychain
%{_libdir}/qt5/mkspecs/modules/qt_Qt5Keychain.pri
%endif
