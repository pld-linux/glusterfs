# TODO: Find pidfiles killproc --pidfile ${PIDFILE} -TERM
#       instead of kill -TERM ${PID}
# TODO: Check transport-ibverbs package and ibverbs bcond
# TODO: Add passing options from /etc/sysconfig/glusterfsd
#       to glusterfsd
#
# Conditional build:
%bcond_without	ibverbs		# ib-verbs transport
#
Summary:	Clustered File Storage that can scale to peta bytes
Summary(pl.UTF-8):	Klastrowy system przechowywania plików skalujący się do petabajtów
Name:		glusterfs
Version:	3.3.1
Release:	1
License:	LGPL v3+ or GPL v2 (libraries), GPL v3+ (programs)
Group:		Applications/System
Source0:	http://download.gluster.org/pub/gluster/glusterfs/LATEST/glusterfs-%{version}.tar.gz
# Source0-md5:	4c9f291de887b1193d5d1acac4003360
Source1:	glusterfsd.init
Patch0:		%{name}-parallel-build.patch
Patch1:		%{name}-workdir.patch
Patch2:		%{name}-link.patch
URL:		http://www.gluster.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libaio-devel
BuildRequires:	libfuse-devel >= 2.6
%{?with_ibverbs:BuildRequires:	libibverbs-devel >= 1.0.4}
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.19
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.4
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
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
Scala różne kawałki miejsca po łączach Infiniband RDMA lub TCP/IP w
jeden duży, równoległy sieciowy system plików. GlusterFS to jeden z
najbardziej wyszukanych systemów plików jeśli chodzi o możliwości i
rozszerzalność. Zapożycza potężną ideę o nazwie Translators z jądra
GNU Hurd. Duża część kodu GlusterFS działa w przestrzeni użytkownika i
jest łatwo zarządzalna.

%package common
Summary:	GlusterFS Library and Translators
Summary(pl.UTF-8):	Biblioteka i translatory GlusterFS-a
Group:		Libraries
Requires:	libxml2 >= 1:2.6.19

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
Scala różne kawałki miejsca po łączach Infiniband RDMA lub TCP/IP w
jeden duży, równoległy sieciowy system plików. GlusterFS to jeden z
najbardziej wyszukanych systemów plików jeśli chodzi o możliwości i
rozszerzalność. Zapożycza potężną ideę o nazwie Translators z jądra
GNU Hurd. Duża część kodu GlusterFS działa w przestrzeni użytkownika i
jest łatwo zarządzalna.

Ten pakiet zawiera libglusterfs i moduły translatorów glusterfs
wspólne dla klienta jak i serwera GlusterFS-a.

%package devel
Summary:	GlusterFS development files
Summary(pl.UTF-8):	Pliki programistyczne GlusterFS-a
Group:		Development/Libraries
Requires:	%{name}-common = %{version}-%{release}
# -lfl
Requires:	flex
Requires:	openssl-devel
Obsoletes:	glusterfs-static

%description devel
This package provides the development files for GlusterFS library.

%description devel -l pl.UTF-8
Ten pakiet udostępnia pliki programistyczne biblioteki GlusterFS-a.

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
Requires:	%{name}-client = %{version}-%{release}
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
%patch0 -p0
%patch1 -p1
%patch2 -p1
find xlators rpc -name Makefile.am | xargs %{__sed} -i -e 's|-avoidversion|-avoid-version|g'

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-fusermount \
	%{!?with_ibverbs:--disable-ibverbs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_var}/lib/glusterd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# No idea why installs elsewhere than later expects to be
mv $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/glusterd.vol $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/glusterfsd.vol

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/glusterfsd

%{__rm} $RPM_BUILD_ROOT%{_libdir}/glusterfs/%{version}/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/glusterfs/%{version}/*/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/glusterfs/%{version}/*/*/*/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	common	-p /sbin/ldconfig
%postun	common	-p /sbin/ldconfig

%files common
%defattr(644,root,root,755)
%doc ChangeLog NEWS README THANKS doc/*.vol.sample
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_libdir}/libgfrpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfrpc.so.0
%attr(755,root,root) %{_libdir}/libgfxdr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfxdr.so.0
%attr(755,root,root) %{_libdir}/libglusterfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglusterfs.so.0
# NOTE: glusterfs is link to glusterfsd and is needed by client mount
%attr(755,root,root) %{_sbindir}/glusterfs
%attr(755,root,root) %{_sbindir}/glusterfsd

%dir %{_libdir}/glusterfs

%dir %{_libdir}/glusterfs/%{version}
%dir %{_libdir}/glusterfs/%{version}/auth
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/auth/addr.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/auth/login.so

%dir %{_libdir}/glusterfs/%{version}/rpc-transport
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/rpc-transport/socket.so

%dir %{_libdir}/glusterfs/%{version}/xlator
%dir %{_libdir}/glusterfs/%{version}/xlator/cluster
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/cluster/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/debug
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/debug/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/encryption
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/encryption/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/features
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/features/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/mount
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mount/fuse.so
%dir %{_libdir}/glusterfs/%{version}/xlator/mgmt
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mgmt/glusterd.so
%dir %{_libdir}/glusterfs/%{version}/xlator/mount
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mount/fuse.so
%dir %{_libdir}/glusterfs/%{version}/xlator/nfs
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/nfs/server.so
%dir %{_libdir}/glusterfs/%{version}/xlator/performance
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/performance/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/protocol
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/protocol/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/storage
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/storage/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/system
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/system/posix-acl.so
%dir %{_libdir}/glusterfs/%{version}/xlator/testing
%dir %{_libdir}/glusterfs/%{version}/xlator/testing/performance
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/testing/performance/*.so

%attr(755,root,root) %{_libdir}/glusterfs/gsyncd

%dir %{_libdir}/glusterfs/python
%dir %{_libdir}/glusterfs/python/syncdaemon
# gsyncd.py is a script, the rest probably don't require *.py
%{_libdir}/glusterfs/python/syncdaemon/*.py*

# disabled in sources
#%{_mandir}/man8/glusterfs.8*
#%{_mandir}/man8/glusterfsd.8*
%dir %{_var}/log/glusterfs

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglusterfs.so
%{_libdir}/libglusterfs.la
%attr(755,root,root) %{_libdir}/libgfrpc.so
%{_libdir}/libgfrpc.la
%attr(755,root,root) %{_libdir}/libgfxdr.so
%{_libdir}/libgfxdr.la

%if %{with ibverbs}
%files transport-ibverbs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/rpc-transport/rdma.so
%endif

%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/glusterfsd.vol
%attr(754,root,root) /etc/rc.d/init.d/glusterfsd
%attr(755,root,root) %{_sbindir}/glusterd
# disabled in sources
#%{_mandir}/man8/glusterd.8*
%dir %{_var}/lib/glusterd

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fusermount-glusterfs
%attr(755,root,root) /sbin/mount.glusterfs
%attr(755,root,root) %{_sbindir}/gluster
%{_mandir}/man8/gluster.8*
# disabled in sources
#%{_mandir}/man8/mount.glusterfs.8*
