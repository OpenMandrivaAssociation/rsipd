Summary:	RSIP is a new protocol which may be an alternative to the NAT/PAT
Name:		rsipd
Version:	0.9.3
Release:	%mkrel 9
License:	GPL
Group:		System/Servers
URL:		http://rsip.info.ucl.ac.be/
Source0:	http://rsip.info.ucl.ac.be/downloads/server/latest/Sources/%{name}-%{version}.src.tar.bz2
Patch0:		rsipd.patch
Patch1:		rsipd-0.9.3-assert.patch
Patch2:		rsipd-0.9.3-gcc4.patch
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
BuildRequires:	libstdc++-devel >= 3.0
BuildRequires:	openslp-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
RSIP is a new protocol which may be an alternative to the NAT/PAT.
RSIP may be used to share an Internet connection between several
computers. Imagine you own 3 computers at home but only 1 Internet
connection. NAT/PAT is often used to share this connection to
allow the three computers to surf at the same time. However, IP
packets exchanged are modified on the way by the NAT/PAT router.
This makes several applications unusable, unless you "patch" your
NAT with "ALG" (or NAT modules). And there must exist one ALG for
each existing or future application which does not support NAT.

RSIP does not modify the packets. Every non-server application
works transparently. We may surf, send email, transfer files etc.
using RSIP from one of our three private computers, even at the
same time. For example, you may use videoconferencing applications
such as GnomeMeeting. This is not possible with the NAT without a
specific NAT module !

Imagine now you want to publish your last holiday pictures on your
own Apache web server. If you use NAT/PAT, you would have to do
"port forwarding'. RSIP provides a similar (simpler ?) technique
to use your server. See the howto section. However, like for the
NAT, it is not possible to install two servers using the same port
on two or more of your private computers.


%prep

%setup -q
%patch0 -p0
%patch1 -p1 -b .assert
%patch2 -p0

%build

%make CFLAGS="%{optflags} -D_REENTRANT"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/rsip
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/lib/rsip

install -m755 src/rsipd %{buildroot}%{_sbindir}/rsipd
install -m644 rsipd.conf %{buildroot}%{_sysconfdir}/rsip/rsipd.conf
install -m755 rsipd %{buildroot}%{_initrddir}/rsipd
ln -fs %{_initrddir}/rsipd %{buildroot}%{_sbindir}/rsipdctl

%post
%_post_service rsipd

%preun
%_preun_service rsipd

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README INSTALLING TODO ChangeLog
%attr(0644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/rsip/rsipd.conf
%dir %{_sysconfdir}/rsip/
%attr(0755,root,root) %config(noreplace) %{_initrddir}/rsipd
%{_sbindir}/rsipd
%{_sbindir}/rsipdctl
%dir /var/lib/rsip


