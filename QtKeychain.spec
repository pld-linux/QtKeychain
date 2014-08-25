Summary:	Qt API to store passwords and other secret data securely
Name:		QtKeychain
Version:	0.3.0
Release:	0.1
License:	Modified BSD License
Group:		Libraries
URL:		https://github.com/frankosterfeld/qtkeychain
# Repackaged from https://github.com/frankosterfeld/qtkeychain/archive/master.zip
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	a9de9be0cae568c03b152009d24ff170
BuildRequires:	QtCore-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_qt4_datadir	%{_datadir}/qt4

%description

%in is a Qt API to store passwords and other secret data securely.
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
Requires:	qt4-build
Requires:	qt4-qmake

%description devel
This package contains libraries and header files for developing
applications that use QKeychain.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
		../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ReadMe.txt ChangeLog
%attr(755,root,root) %{_libdir}/libqtkeychain.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqtkeychain.so.0

%files devel
%defattr(644,root,root,755)
#%doc doc examples
%dir %{_includedir}/qtkeychain
%{_includedir}/qtkeychain/keychain.h
%{_includedir}/qtkeychain/qkeychain_export.h
%dir %{_libdir}/cmake/QtKeychain
%attr(755,root,root) %{_libdir}/libqtkeychain.so
%{_libdir}/cmake/QtKeychain/QtKeychainLibraryDepends.cmake
%{_libdir}/cmake/QtKeychain/QtKeychainLibraryDepends-pld.cmake
%{_libdir}/cmake/QtKeychain/QtKeychainConfig.cmake
%{_libdir}/cmake/QtKeychain/QtKeychainConfigVersion.cmake
