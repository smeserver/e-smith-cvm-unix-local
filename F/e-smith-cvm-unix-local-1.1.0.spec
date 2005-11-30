Summary: Module for supervising cvm auth daemon
%define name e-smith-cvm-unix-local
Name: %{name}
%define version 1.1.0
%define release 03
Version: %{version}
Release: %{release}
License: GPL
Vendor: Mitel Networks Corporation
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
Patch0: e-smith-cvm-unix-local-1.1.0-02.mitel_patch
Packager: e-smith developers <bugs@e-smith.com>
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
Requires: cvm daemontools
Requires: e-smith-lib >= 1.13.1-90
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
AutoReqProv: no

%description
Module for supervising cvm auth daemon

%changelog
* Wed Nov 30 2005 Gordon Rowell <gordonr@gormand.com.au> 1.1.0-03
- Bump release number only

* Wed May  4 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-02]
- Update cvm calling sequence, for later version of cvm.

* Wed May  4 2005 Charlie Brady <charlieb@e-smith.com>
- [1.1.0-01]
- Changing version to development stream number - 1.1.0

* Thu Jun 26 2003 Charlie Brady <charlieb@e-smith.com>
- [1.0.0-01]
- Change to stable stream version number - 1.0.0

* Wed Jun  4 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.1-05]
- Use create-system-user to create cvmlog user. [charlieb 6033]

* Fri Apr 18 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.1-04]
- Move socket to a private directory, and change its
  pathname. [charlieb 587]

* Wed Apr 16 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.1-03]
- Change cvmlog userid to 1003, and change error exit to warning.
  [charlieb 6033]

* Fri Mar 21 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.1-02]
- Add cvmlog user and cvm log directory [charlieb 587]

* Wed Mar 19 2003 Charlie Brady <charlieb@e-smith.com>
- [0.0.1-01]
- Initial

%prep
%setup
%patch0 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
mkdir -p $RPM_BUILD_ROOT/service
mkdir -p $RPM_BUILD_ROOT/var/lib/cvm
ln -s /var/service/cvm-unix-local $RPM_BUILD_ROOT/service/cvm-unix-local
mkdir -p $RPM_BUILD_ROOT/var/log/cvm

%pre
/sbin/e-smith/create-system-user cvmlog 1003 'cvm output log user' /var/log/imap /bin/false

%preun
if [ "$1" = 0 ]
then
    # Make sure that imap is not running
    svc-stop imap
    # Now get svscan to forget about it
    svc-remove imap
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr(1755,root,root)/var/service/cvm-unix-local
%attr(0755,root,root)/var/service/cvm-unix-local/run
%attr(0755,root,root)/var/lib/cvm
%dir %attr(0755,root,root)/var/service/cvm-unix-local/log
%attr(0755,root,root)/var/service/cvm-unix-local/log/run
%dir %attr(0750,cvmlog,cvmlog)/var/log/cvm
/service/cvm-unix-local
