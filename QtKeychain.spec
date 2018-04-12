#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

Summary:	Qt API to store passwords and other secret data securely
Name:		QtKeychain
Version:	0.8.0
Release:	1
License:	Modified BSD License
Group:		Libraries
Source0:	https://github.com/frankosterfeld/qtkeychain/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d741e7e55ae48a130cb95264fbe732b7
Patch0:		cmake.patch
URL:		https://github.com/frankosterfeld/qtkeychain
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(find_lang) >= 1.37
%if %{with qt4}
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5DBus-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#define	skip_post_check_so	libqt5keychain.so.*

%description
QtKeychain a Qt API to store passwords and other secret data securely.

How the data is stored depends on the platform:
- Mac OS X: Passwords are stored in the OS X Keychain.
- Linux/Unix: If running, GNOME Keyring is used, otherwise qtkeychain
  tries to use KWallet (via D-Bus), if available.
- Windows: Windows does not provide a service for secure storage.
  QtKeychain uses the Windows API function

%package devel
Summary:	Development files for QtKeychain
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files for developing
applications that use QKeychain.

%package -n Qt5Keychain
Summary:	Qt API to store passwords and other secret data securely
Group:		Libraries

%description -n Qt5Keychain
QtKeychain a Qt API to store passwords and other secret data securely.

How the data is stored depends on the platform:
- Mac OS X: Passwords are stored in the OS X Keychain.
- Linux/Unix: If running, GNOME Keyring is used, otherwise qtkeychain
  tries to use KWallet (via D-Bus), if available.
- Windows: Windows does not provide a service for secure storage.
  QtKeychain uses the Windows API function

%package -n Qt5Keychain-devel
Summary:	Development files for QtKeychain
Group:		Development/Libraries
Requires:	Qt5Keychain = %{version}-%{release}

%description -n Qt5Keychain-devel
This package contains libraries and header files for developing
applications that use QKeychain.

%prep
%setup -q -n qtkeychain-%{version}
%patch0 -p1

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake \
	-DBUILD_WITH_QT4:BOOL=TRUE \
	..
%{__make}
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake \
	-DBUILD_WITH_QT4:BOOL=OFF \
	..
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
%{__make} -C build-qt4 install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang qtkeychain --with-qm
%endif

%if %{with qt5}
%{__make} -C build-qt5 install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang qtkeychain --with-qm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with qt4}
%files -f qtkeychain.lang
%defattr(644,root,root,755)
%doc COPYING ReadMe.txt ChangeLog
%attr(755,root,root) %{_libdir}/libqtkeychain.so.*.*.*
%ghost %{_libdir}/libqtkeychain.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/qtkeychain
%{_libdir}/libqtkeychain.so
%{_libdir}/cmake/QtKeychain
%endif

%if %{with qt5}
%files -n Qt5Keychain
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqt5keychain.so.*.*.*
%ghost %{_libdir}/libqt5keychain.so.1

%files -n Qt5Keychain-devel
%defattr(644,root,root,755)
%{_includedir}/qt5keychain
%{_libdir}/libqt5keychain.so
%{_libdir}/cmake/Qt5Keychain
%endif
