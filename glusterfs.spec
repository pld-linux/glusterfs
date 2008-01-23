#
# Conditional build:
%bcond_without	ibverbs		# ib-verbs transport
#
Summary:	Clustered File Storage that can scale to peta bytes
Summary(pl.UTF-8):	Klastrowy system przechowywania plików skalujący się do petabajtów
Name:		glusterfs
Version:	1.3.7
Release:	2
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.zresearch.com/pub/gluster/glusterfs/1.3/%{name}-%{version}.tar.gz
# Source0-md5:	ede5fe1e17e7c333536400e138a084f1
Source1:	glusterfsd.init
Patch0:		%{name}-link.patch
URL:		http://gluster.org/glusterfs.php
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libfuse-devel >= 2.6
BuildRequires:	libtool
%{?with_ibverbs:BuildRequires:	libibverbs-devel >= 1.0.4}
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file system in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
userspace and easily manageable.

%description -l pl.UTF-8
GlusterFS to klastrowy system plików skalujący się do petabajtów.
Scala różne kawałki miejsca po łączach Infiniband RDMA lub TCP/IP
w jeden duży, równoległy sieciowy system plików. GlusterFS to
jeden z najbardziej wyszukanych systemów plików jeśli chodzi o
możliwości i rozszerzalność. Zapożycza potężną ideę o nazwie
Translators z jądra GNU Hurd. Duża część kodu GlusterFS działa w
przestrzeni użytkownika i jest łatwo zarządzalna.

%package common
Summary:	GlusterFS Library and Translators
Summary(pl.UTF-8):	Biblioteka i translatory GlusterFS-a
Group:		Libraries

%description common
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file system in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
userspace and easily manageable.

This package includes libglusterfs and glusterfs translator modules
common to both GlusterFS server and client framework.

%description common -l pl.UTF-8
GlusterFS to klastrowy system plików skalujący się do petabajtów.
Scala różne kawałki miejsca po łączach Infiniband RDMA lub TCP/IP
w jeden duży, równoległy sieciowy system plików. GlusterFS to
jeden z najbardziej wyszukanych systemów plików jeśli chodzi o
możliwości i rozszerzalność. Zapożycza potężną ideę o nazwie
Translators z jądra GNU Hurd. Duża część kodu GlusterFS działa w
przestrzeni użytkownika i jest łatwo zarządzalna.

Ten pakiet zawiera libglusterfs i moduły translatorów glusterfs
wspólne dla klienta jak i serwera GlusterFS-a.

%package devel
Summary:	GlusterFS development files
Summary(pl.UTF-8):	Pliki programistyczne GlusterFS-a
Group:		Development/Libraries
Requires:	%{name}-common = %{version}-%{release}

%description devel
This package provides the development files for GlusterFS library.

%description devel -l pl.UTF-8
Ten pakiet udostępnia pliki programistyczne biblioteki GlusterFS-a.

%package static
Summary:	Static GlusterFS library
Summary(pl.UTF-8):	Statyczna biblioteka GlusterFS-a
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GlusterFS library.

%description static -l pl.UTF-8
Statyczna biblioteka GlusterFS-a.

%package transport-ibverbs
Summary:	InfiniBand "verbs" transport plugins for GlusterFS
Summary(pl.UTF-8):	Wtyczki transportu "verbs" InfiniBand dla GlusterFS-a
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}
Requires:	libibverbs >= 1.0.4

%description transport-ibverbs
InfiniBand "verbs" transport plugins for GlusterFS.

%description transport-ibverbs -l pl.UTF-8
Wtyczki transportu "verbs" InfiniBand dla GlusterFS-a.

%package server
Summary:	GlusterFS Server
Summary(pl.UTF-8):	Serwer GlusterFS-a
Group:		Daemons
Requires:	%{name}-common = %{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description server
This package provides the glusterfs server daemon.

%description server -l pl.UTF-8
Ten pakiet zawiera część serwerową GlusterFS-a.

%package client
Summary:	GlusterFS Client
Summary(pl.UTF-8):	Klient GlusterFS
Group:		Applications/System
Requires:	%{name}-common = %{version}-%{release}
Requires:	libfuse >= 2.6

%description client
This package provides the FUSE based GlusterFS client.

%description client -l pl.UTF-8
Ten pakiet udostępnia opartego na FUSE klienta GlusterFS-a.

%prep
%setup -q
%patch0 -p1

cp -l doc/examples/README README.examples

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_ibverbs:--disable-ibverbs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/glusterfsd

rm -r $RPM_BUILD_ROOT%{_docdir}/glusterfs/examples

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README README.examples doc/*.vol.sample doc/examples/*.vol
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_libdir}/libglusterfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglusterfs.so.0
%dir %{_libdir}/glusterfs
%dir %{_libdir}/glusterfs/%{version}
%dir %{_libdir}/glusterfs/%{version}/scheduler
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/scheduler/*.so
%dir %{_libdir}/glusterfs/%{version}/transport
%dir %{_libdir}/glusterfs/%{version}/transport/ib-sdp
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/ib-sdp/client.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/ib-sdp/server.so
%dir %{_libdir}/glusterfs/%{version}/transport/tcp
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/tcp/client.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/tcp/server.so
%dir %{_libdir}/glusterfs/%{version}/xlator
%dir %{_libdir}/glusterfs/%{version}/xlator/cluster
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/cluster/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/debug
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/debug/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/encryption
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/encryption/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/features
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/features/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/performance
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/performance/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/protocol
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/protocol/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/storage
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/storage/*.so
%dir /var/log/glusterfs

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglusterfs.so
%{_libdir}/libglusterfs.la
#%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libglusterfs.a

%if %{with ibverbs}
%files transport-ibverbs
%defattr(644,root,root,755)
%dir %{_libdir}/glusterfs/%{version}/transport/ib-verbs
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/ib-verbs/client.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/ib-verbs/server.so
%endif

%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(754,root,root) /etc/rc.d/init.d/glusterfsd
%attr(755,root,root) %{_sbindir}/glusterfsd

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/glusterfs
%attr(755,root,root) /sbin/mount.glusterfs
