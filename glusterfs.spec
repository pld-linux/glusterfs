# TODO:
# - Find pidfiles killproc --pidfile ${PIDFILE} -TERM instead of kill -TERM ${PID}
# - Check transport-ibverbs package and ibverbs bcond
# - Add passing options from /etc/sysconfig/glusterfsd to glusterfsd
# - package /etc/glusterfs/glusterfs-logrotate as logrotate config
# - Fix/provide working systemd service files. 
#   As for 3.7.11, package provided seems be non-working.
# - configuration for firewalld? (--enable-firewalld, but checks for firewalld executable)
#
# Conditional build:
%bcond_without	ibverbs		# ib-verbs transport
%bcond_without	systemtap	# systemtap/dtrace support
%bcond_without	system_fuse	# system fusermount
#
Summary:	Clustered File Storage that can scale to peta bytes
Summary(pl.UTF-8):	Klastrowy system przechowywania plików skalujący się do petabajtów
Name:		glusterfs
Version:	6.10
Release:	2
License:	LGPL v3+ or GPL v2 (libraries), GPL v3+ (programs)
Group:		Applications/System
Source0:	https://download.gluster.org/pub/gluster/glusterfs/6/%{version}/glusterfs-%{version}.tar.gz
# Source0-md5:	43e4e6c017cb2ade77bc644034146215
Source1:	glusterfsd.init
Patch0:		%{name}-noquiet.patch
Patch1:		systemd.patch
URL:		https://www.gluster.org/
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison
#BuildRequires:	cmocka-devel >= 1.0.1 for unittest
BuildRequires:	curl-devel
# for bd-xlator
BuildRequires:	device-mapper-devel >= 2.02.79
BuildRequires:	flex
BuildRequires:	libaio-devel
%{?with_ibverbs:BuildRequires:	libibverbs-devel >= 1.0.4}
%{?with_ibverbs:BuildRequires:	librdmacm-devel >= 1.0.15}
BuildRequires:	libselinux-devel
BuildRequires:	libtirpc-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 1:2.6.19
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.2
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	readline-devel
BuildRequires:	rpcsvc-proto
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	userspace-rcu-devel >= 0.8
BuildRequires:	zlib-devel >= 1.2.0
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
Summary:	GlusterFS common files including Translators
Summary(pl.UTF-8):	Wspólne pliki GlusterFS-a, w tym translatory
Group:		Libraries
Requires:	libxml2 >= 1:2.6.19
Requires:	zlib >= 1.2.0

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

%package libs
Summary:	GlusterFS libraries
Summary(pl.UTF-8):	Biblioteki GlusterFS-a
Group:		Libraries
Conflicts:	glusterfs-common < 3.4.0

%description libs
GlusterFS libraries.

%description libs -l pl.UTF-8
Biblioteki GlusterFS-a.

%package devel
Summary:	GlusterFS development files
Summary(pl.UTF-8):	Pliki programistyczne GlusterFS-a
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
# -lfl
Requires:	flex
Requires:	libtirpc-devel
Requires:	openssl-devel
Obsoletes:	glusterfs-static

%description devel
This package provides the development files for GlusterFS library.

%description devel -l pl.UTF-8
Ten pakiet udostępnia pliki programistyczne biblioteki GlusterFS-a.

%package -n python3-gluster
Summary:	Python 3 interface to GlusterFS libraries
Summary(pl.UTF-8):	Interfejs Pythona 3 do bibliotek GlusterFS
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	python-gluster < 6.6

%description -n python3-gluster
Python 3 interface to GlusterFS libraries.

%description -n python3-gluster -l pl.UTF-8
Interfejs Pythona 3 do bibliotek GlusterFS.

%package transport-ibverbs
Summary:	InfiniBand "verbs" transport plugins for GlusterFS
Summary(pl.UTF-8):	Wtyczki transportu "verbs" InfiniBand dla GlusterFS-a
Group:		Libraries
Requires:	%{name}-common = %{version}-%{release}
Requires:	libibverbs >= 1.0.4
Requires:	librdmacm >= 1.0.15

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
Requires:	python3-modules 

%description server
This package provides the glusterfs server daemon.

%description server -l pl.UTF-8
Ten pakiet zawiera część serwerową GlusterFS-a.

%package client
Summary:	GlusterFS Client
Summary(pl.UTF-8):	Klient GlusterFS
Group:		Applications/System
Requires:	%{name}-common = %{version}-%{release}
%{?with_system_fuse:Requires:	libfuse >= 2.6}

%description client
This package provides the FUSE based GlusterFS client.

%description client -l pl.UTF-8
Ten pakiet udostępnia opartego na FUSE klienta GlusterFS-a.

%package resource-agents
Summary:	OCF Resource Agents for GlusterFS processes
Summary(pl.UTF-8):	Agenci OCF do monitorowania procesów GlusterFS-a
Group:		Applications/System
Requires:	%{name}-server = %{version}-%{release}
Requires:	resource-agents

%description resource-agents
OCF Resource Agents for GlusterFS processes.

%description resource-agents -l pl.UTF-8
Agenci OCF do monitorowania procesów GlusterFS-a.

%package events
Summary:	GlusterFS Events
Summary(pl.UTF-8):	Obsługa zdarzeń dla GlusterFS-a
Group:		Applications/File
Requires:	%{name}-server = %{version}-%{release}
Requires:	python3-gluster = %{version}-%{release}
Requires:	python3-prettytable
Requires:	python3-requests

%description events
GlusterFS Events.

%description events -l pl.UTF-8
Obsługa zdarzeń dla GlusterFS-a.

%package geo-replication
Summary:	GlusterFS Geo-replication
Summary(pl.UTF-8):	Geo-replikacja dla GlusterFS-a
Group:		Applications/File
Requires:	%{name}-server = %{version}-%{release}
Requires:	python3-gluster = %{version}-%{release}
Requires:	python3-prettytable
Requires:	rsync

%description geo-replication
GlusterFS support for geo-replication.

%description geo-replication -l pl.UTF-8
Obsługa geo-replikacji dla GlusterFS-a.

%package thin-arbiter
Summary:	GlusterFS thin-arbiter module
Summary(pl.UTF-8):	Moduł thin-arbiter dla GlusterFS-a
Group:		Applications/File
Requires:	%{name}-server = %{version}-%{release}

%description thin-arbiter
This package provides a tie-breaker functionality to GlusterFS
replicate volume. It includes translators required to provide the
functionality, and also few other scripts required for getting the
setup done.

This package provides the glusterfs thin-arbiter translator.

%description thin-arbiter -l pl.UTF-8
Ten pakiet dodaje funkcję dogrywki do replikacji wolumenów GlusterFS.
Zawiera moduły tłumaczące wymagane do zapewniania tej funkcji oraz
kilka skryptów wymaganych do konfiguracji.

Ten pakiet zawiera moduł tłumaczący thin-arbiter.

%package -n emacs-glusterfs-mode
Summary:	Emacs mode to edit GlusterFS configuration
Summary(pl.UTF-8):	Tryb Emacsa do edycji konfiguracji GlusterFS-a
Group:		Applications/Editors
Requires:	%{name}-common = %{version}-%{release}
Requires:	emacs-common

%description -n emacs-glusterfs-mode
Emacs mode to edit GlusterFS configuration.

%description -n emacs-glusterfs-mode -l pl.UTF-8
Tryb Emacsa do edycji konfiguracji GlusterFS-a.

%package -n vim-syntax-glusterfs
Summary:	Vim syntax file to edit GlusterFS configuration
Summary(pl.UTF-8):	Plik składni Vima do edycji konfiguracji GlusterFS-a
Group:		Applications/Editors
Requires:	%{name}-common = %{version}-%{release}
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-glusterfs
Vim syntax file to edit GlusterFS configuration.

%description -n vim-syntax-glusterfs -l pl.UTF-8
Plik składni Vima do edycji konfiguracji GlusterFS-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python3} \
	%{?with_system_fuse:--disable-fusermount} \
	--disable-silent-rules \
	--enable-gnfs \
	%{!?with_ibverbs:--disable-ibverbs} \
	--enable-systemtap%{!?with_systemtap:=no} \
	--with-initdir=/etc/rc.d/init.d \
	--with-systemddir=%{systemdunitdir}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# No idea why installs elsewhere than later expects to be
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/glusterd.vol $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/glusterfsd.vol

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/glusterfsd
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >>$RPM_BUILD_ROOT%{systemdtmpfilesdir}/gluster.conf <<EOF
d /var/run/gluster 0755 root root -
EOF

install -d $RPM_BUILD_ROOT%{_datadir}/{emacs/site-lisp,vim/syntax}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/glusterfs/glusterfs.vim $RPM_BUILD_ROOT%{_datadir}/vim/syntax
%{__mv} $RPM_BUILD_ROOT%{_docdir}/glusterfs/glusterfs-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

%{__rm} $RPM_BUILD_ROOT%{_libdir}/glusterfs/%{version}/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/glusterfs/%{version}/*/*/*.la

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/glusterfs/benchmarking
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/glusterfs/python/syncdaemon/README.md
# example, installed as /var/lib/glusterd/groups/virt
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/glusterfs/group-virt.example

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs	-p /sbin/ldconfig
%postun	libs	-p /sbin/ldconfig

%if 0
# TODO: verify these scripts (see also included glusterfs.spec)
%post server
# note: glusterfsd.init vs glusterd.service
/sbin/chkconfig --add glusterfsd
%service glusterfsd restart
%systemd_post glusterd.service
# TODO?
#glusterd --xlator-option *.upgrade=on -N

%preun server
if [ "$1" = "0" ]; then
	%service -q glusterfsd stop
	/sbin/chkconfig --del glusterfsd
fi
%systemd_preun glusterd

%postun server
%systemd_reload

%post events
%systemd_post glustereventsd

%preun events
%systemd_preun glustereventsd

%postun events
%systemd_reload

%post geo-replication
%service glusterd restart
%endif

%files common
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/glusterfind
%attr(755,root,root) %{_sbindir}/glfsheal
# NOTE: glusterfs is link to glusterfsd and is needed by client mount
%attr(755,root,root) %{_sbindir}/glusterfs
%attr(755,root,root) %{_sbindir}/glusterfsd
%dir %{_sysconfdir}/%{name}

%dir %{_libdir}/glusterfs

%dir %{_libdir}/glusterfs/%{version}
%dir %{_libdir}/glusterfs/%{version}/auth
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/auth/addr.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/auth/login.so

%dir %{_libdir}/glusterfs/%{version}/cloudsync-plugins
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/cloudsync-plugins/cloudsyncs3.so

%dir %{_libdir}/glusterfs/%{version}/rpc-transport
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/rpc-transport/socket.so

%dir %{_libdir}/glusterfs/%{version}/xlator
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/meta.so
%dir %{_libdir}/glusterfs/%{version}/xlator/cluster
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/cluster/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/debug
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/debug/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/features
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/features/*.so
%exclude %{_libdir}/glusterfs/%{version}/xlator/features/thin-arbiter.so
%dir %{_libdir}/glusterfs/%{version}/xlator/mgmt
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mgmt/glusterd.so
%dir %{_libdir}/glusterfs/%{version}/xlator/mount
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mount/api.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/mount/fuse.so
%dir %{_libdir}/glusterfs/%{version}/xlator/nfs
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/nfs/server.so
%dir %{_libdir}/glusterfs/%{version}/xlator/performance
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/performance/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator/playground
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/playground/template.so
%dir %{_libdir}/glusterfs/%{version}/xlator/protocol
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/protocol/client.so
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/protocol/server.so
%dir %{_libdir}/glusterfs/%{version}/xlator/storage
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/storage/posix.so
%dir %{_libdir}/glusterfs/%{version}/xlator/system
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/system/posix-acl.so

%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/glusterfs
%endif
%attr(755,root,root) %{_libexecdir}/glusterfs/peer_add_secret_pub

%dir %{_libexecdir}/glusterfs/glusterfind
%attr(755,root,root) %{_libexecdir}/glusterfs/glusterfind/S57glusterfind-delete-post.py
%attr(755,root,root) %{_libexecdir}/glusterfs/glusterfind/brickfind.py
%attr(755,root,root) %{_libexecdir}/glusterfs/glusterfind/changelog.py
%attr(755,root,root) %{_libexecdir}/glusterfs/glusterfind/nodeagent.py
%{_libexecdir}/glusterfs/glusterfind/__init__.py
%{_libexecdir}/glusterfs/glusterfind/changelogdata.py
%{_libexecdir}/glusterfs/glusterfind/conf.py
%{_libexecdir}/glusterfs/glusterfind/gfind_py2py3.py
%{_libexecdir}/glusterfs/glusterfind/libgfchangelog.py
%{_libexecdir}/glusterfs/glusterfind/main.py
%{_libexecdir}/glusterfs/glusterfind/utils.py
%{_libexecdir}/glusterfs/glusterfind/tool.conf
%{_libexecdir}/glusterfs/glusterfind/__pycache__

%dir %{_libexecdir}/glusterfs/python

%dir %{_datadir}/glusterfs
%dir %{_datadir}/glusterfs/scripts
%attr(755,root,root) %{_datadir}/glusterfs/scripts/control-cpu-load.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/control-mem.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/post-upgrade-script-for-quota.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/pre-upgrade-script-for-quota.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/stop-all-gluster-processes.sh

%{_mandir}/man8/glusterfs.8*
%{_mandir}/man8/glusterfsd.8*
%dir %{_var}/log/glusterfs

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgfapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfapi.so.0
%attr(755,root,root) %{_libdir}/libgfchangelog.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfchangelog.so.0
%attr(755,root,root) %{_libdir}/libgfrpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfrpc.so.0
%attr(755,root,root) %{_libdir}/libgfxdr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfxdr.so.0
%attr(755,root,root) %{_libdir}/libglusterfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglusterfs.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgfapi.so
%attr(755,root,root) %{_libdir}/libgfchangelog.so
%attr(755,root,root) %{_libdir}/libgfrpc.so
%attr(755,root,root) %{_libdir}/libgfxdr.so
%attr(755,root,root) %{_libdir}/libglusterfs.so
%{_libdir}/libgfapi.la
%{_libdir}/libgfchangelog.la
%{_libdir}/libgfrpc.la
%{_libdir}/libgfxdr.la
%{_libdir}/libglusterfs.la
%dir %{_includedir}/glusterfs
%{_includedir}/glusterfs/api
%{_includedir}/glusterfs/gfchangelog
%{_includedir}/glusterfs/rpc
%{_includedir}/glusterfs/server
%{_includedir}/glusterfs/*.h
%{_pkgconfigdir}/glusterfs-api.pc
%{_pkgconfigdir}/libgfchangelog.pc

%files -n python3-gluster
%defattr(644,root,root,755)
%dir %{py3_sitescriptdir}/gluster
%{py3_sitescriptdir}/gluster/__init__.py
%{py3_sitescriptdir}/gluster/__pycache__
%{py3_sitescriptdir}/gluster/cliutils
# created only when using py_build/py_install in xlators/features/glupy/src
#%{py3_sitescriptdir}/glusterfs_glupy-%{version}-py*.egg-info

%if %{with ibverbs}
%files transport-ibverbs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/rpc-transport/rdma.so
%endif

%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/glusterfsd.vol
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-db-workload
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-distributed-virt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-gluster-block
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-metadata-cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-nl-cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/group-samba
%attr(754,root,root) /etc/rc.d/init.d/glusterfsd
%attr(755,root,root) %{_sbindir}/conf.py
%attr(755,root,root) %{_sbindir}/gcron.py
%attr(755,root,root) %{_sbindir}/gf_attach
%attr(755,root,root) %{_sbindir}/gluster-setgfid2path
%attr(755,root,root) %{_sbindir}/glusterd
%attr(755,root,root) %{_sbindir}/snap_scheduler.py
%attr(755,root,root) %{_libexecdir}/glusterfs/mount-shared-storage.sh
%{systemdunitdir}/glusterd.service
%{systemdunitdir}/glusterfssharedstorage.service
%{systemdtmpfilesdir}/gluster.conf

%{_mandir}/man8/gluster-setgfid2path.8*
%{_mandir}/man8/glusterd.8*
%dir %{_var}/lib/glusterd
%dir %{_var}/lib/glusterd/groups
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/db-workload
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/distributed-virt
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/gluster-block
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/metadata-cache
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/nl-cache
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/samba
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/groups/virt
%dir %{_var}/lib/glusterd/hooks
%dir %{_var}/lib/glusterd/hooks/1
%dir %{_var}/lib/glusterd/hooks/1/add-brick
%dir %{_var}/lib/glusterd/hooks/1/add-brick/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/add-brick/post/S10selinux-label-brick.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/add-brick/post/S13create-subdir-mounts.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/add-brick/post/disabled-quota-root-xattr-heal.sh
%dir %{_var}/lib/glusterd/hooks/1/add-brick/pre
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/add-brick/pre/S28Quota-enable-root-xattr-heal.sh
%dir %{_var}/lib/glusterd/hooks/1/create
%dir %{_var}/lib/glusterd/hooks/1/create/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/create/post/S10selinux-label-brick.sh
%dir %{_var}/lib/glusterd/hooks/1/delete
%dir %{_var}/lib/glusterd/hooks/1/delete/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/delete/post/S57glusterfind-delete-post
%dir %{_var}/lib/glusterd/hooks/1/delete/pre
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/delete/pre/S10selinux-del-fcontext.sh
%dir %{_var}/lib/glusterd/hooks/1/set
%dir %{_var}/lib/glusterd/hooks/1/set/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/set/post/S30samba-set.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/set/post/S32gluster_enable_shared_storage.sh
%dir %{_var}/lib/glusterd/hooks/1/start
%dir %{_var}/lib/glusterd/hooks/1/start/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/start/post/S29CTDBsetup.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/start/post/S30samba-start.sh
%dir %{_var}/lib/glusterd/hooks/1/stop
%dir %{_var}/lib/glusterd/hooks/1/stop/pre
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/stop/pre/S29CTDB-teardown.sh
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/stop/pre/S30samba-stop.sh
%dir %{_var}/run/gluster

%files client
%defattr(644,root,root,755)
%{!?with_system_fuse:%attr(755,root,root) %{_bindir}/fusermount-glusterfs}
%attr(755,root,root) /sbin/mount.glusterfs
%attr(755,root,root) %{_sbindir}/gluster
%{_mandir}/man8/gluster.8*
%{_mandir}/man8/mount.glusterfs.8*

%files resource-agents
%defattr(644,root,root,755)
%dir %{_prefix}/lib/ocf/resource.d/glusterfs
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/glusterfs/glusterd
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/glusterfs/volume

%files events
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/glusterfs/eventsconfig.json
%attr(755,root,root) %{_sbindir}/gluster-eventsapi
%attr(755,root,root) %{_sbindir}/glustereventsd
%dir %{_libexecdir}/glusterfs/gfevents
%attr(755,root,root) %{_libexecdir}/glusterfs/gfevents/glustereventsd.py
%{_libexecdir}/glusterfs/gfevents/__init__.py
%{_libexecdir}/glusterfs/gfevents/eventsapiconf.py
%{_libexecdir}/glusterfs/gfevents/eventtypes.py
%{_libexecdir}/glusterfs/gfevents/gf_event.py
%{_libexecdir}/glusterfs/gfevents/handlers.py
%{_libexecdir}/glusterfs/gfevents/utils.py
%{_libexecdir}/glusterfs/gfevents/__pycache__
%{_libexecdir}/glusterfs/peer_eventsapi.py
%{_datadir}/glusterfs/scripts/eventsdash.py
%{systemdunitdir}/glustereventsd.service

%files geo-replication
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/gsyncd.conf
%attr(755,root,root) %{_sbindir}/gfind_missing_files
%attr(755,root,root) %{_sbindir}/gluster-georep-sshkey
%attr(755,root,root) %{_sbindir}/gluster-mountbroker
%attr(755,root,root) %{_libexecdir}/glusterfs/gsyncd
%attr(755,root,root) %{_libexecdir}/glusterfs/gverify.sh
%attr(755,root,root) %{_libexecdir}/glusterfs/peer_georep-sshkey.py*
%attr(755,root,root) %{_libexecdir}/glusterfs/peer_gsec_create
%attr(755,root,root) %{_libexecdir}/glusterfs/peer_mountbroker
%attr(755,root,root) %{_libexecdir}/glusterfs/peer_mountbroker.py*
%attr(755,root,root) %{_libexecdir}/glusterfs/set_geo_rep_pem_keys.sh
%dir %{_libexecdir}/glusterfs/gfind_missing_files
%attr(755,root,root) %{_libexecdir}/glusterfs/gfind_missing_files/*
%dir %{_libexecdir}/glusterfs/python/syncdaemon
%{_libexecdir}/glusterfs/python/syncdaemon/*.py
%{_libexecdir}/glusterfs/python/syncdaemon/__pycache__
%attr(755,root,root) %{_datadir}/glusterfs/scripts/generate-gfid-file.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/get-gfid.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/gsync-sync-gfid
%attr(755,root,root) %{_datadir}/glusterfs/scripts/gsync-upgrade.sh
%attr(755,root,root) %{_datadir}/glusterfs/scripts/schedule_georep.py
%attr(755,root,root) %{_datadir}/glusterfs/scripts/slave-upgrade.sh
%dir %{_var}/lib/glusterd/hooks/1/gsync-create
%dir %{_var}/lib/glusterd/hooks/1/gsync-create/post
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_var}/lib/glusterd/hooks/1/gsync-create/post/S56glusterd-geo-rep-create-post.sh

%files thin-arbiter
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/thin-arbiter.vol
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/features/thin-arbiter.so
%attr(755,root,root) %{_datadir}/glusterfs/scripts/setup-thin-arbiter.sh
%{systemdunitdir}/gluster-ta-volume.service

%files -n emacs-glusterfs-mode
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/glusterfs-mode.el

%files -n vim-syntax-glusterfs
%defattr(644,root,root,755)
%{_datadir}/vim/syntax/glusterfs.vim
