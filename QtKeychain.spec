Summary:	Qt API to store passwords and other secret data securely
Summary(pl.UTF-8):	API Qt do bezpiecznego przechowywania haseł i innych tajnych danych
Name:		QtKeychain
Version:	0.11.1
Release:	1
License:	Modified BSD License
Group:		Libraries
#Source0Download: https://github.com/frankosterfeld/qtkeychain/releases
Source0:	https://github.com/frankosterfeld/qtkeychain/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4c398ebd45e7753efa1951b0857e840d
URL:		https://github.com/frankosterfeld/qtkeychain
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtDBus-devel >= 4
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libsecret-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.37
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
Obsoletes:	QtKeychain-common < 0.10
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
Requires:	QtCore-devel >= 4

%description devel
This package contains the header files for developing applications
that use QtKeychain.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę QtKeychain.

%prep
%setup -q -n qtkeychain-%{version}

%build
install -d build-qt4
cd build-qt4
%cmake .. \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt4/mkspecs/modules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-qt4 install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang qtkeychain --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f qtkeychain.lang
%defattr(644,root,root,755)
%doc COPYING ChangeLog ReadMe.txt
%attr(755,root,root) %{_libdir}/libqtkeychain.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtkeychain.so.1
%dir %{_datadir}/qtkeychain
%dir %{_datadir}/qtkeychain/translations

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqtkeychain.so
%{_includedir}/qtkeychain
%{_libdir}/cmake/QtKeychain
%{_libdir}/qt4/mkspecs/modules/qt_QtKeychain.pri
