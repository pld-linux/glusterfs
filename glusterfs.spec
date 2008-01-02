# TODO: package docs
Summary:	Clustered File Storage that can scale to peta bytes
Summary(pl.UTF-8):	Klastrowy system przechowywania plików skalujący się do petabajtów
Name:		glusterfs
Version:	1.3.7
Release:	0.2
License:	GPL v2
Group:		Applications/System
Source0:	http://ftp.zresearch.com/pub/gluster/glusterfs/1.3/%{name}-%{version}.tar.gz
# Source0-md5:	ede5fe1e17e7c333536400e138a084f1
URL:		http://gluster.org/glusterfs.php
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libfuse-devel
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
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
Group:		Applications/System

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
Pakiet zawiera libglusterfs i moduly translatorow glusterfs wspolne
dla klienta jak i serwera GlusterFS.

%package server
Summary:	GlusterFS Server
Group:		Applications/System
Requires:	%{name}-common = %{version}


%description server
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file system in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
userspace and easily manageable.

This package provides the glusterfs server daemon.

%description server -l pl.UTF-8
Pakiet zawiera czesc serwerowa GlusterFS.


%package client
Summary:	GlusterFS Client
Group:		Applications/System
Requires:	%{name}-common = %{version}

%description client
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file system in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
userspace and easily manageable.

This package provides the FUSE based GlusterFS client.

%description client -l pl.UTF-8
Pliki bazujacego na FUSE klienta GlusterFS.

%package devel
Summary:	GlusterFS Development Libraries
Group:		Development/Libraries
Requires:	%{name}-common = %{version}

%description devel
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file system.
GlusterFS is one of the most sophisticated file system in terms of
features and extensibility. It borrows a powerful concept called
Translators from GNU Hurd kernel. Much of the code in GlusterFS is in
userspace and easily manageable.

This package provides the development libraries.

%description devel -l pl.UTF-8
Pliki i biblioteki potrzebne do rozwoju GlusterFS.


%prep
%setup -q

%build
%configure \
	--disable-ibverbs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

##%{_sysconfdir}/%{name}/%{name}*


%files common
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README

%attr(755,root,root) %{_libdir}/libglusterfs.so.*
%dir %{_libdir}/glusterfs/%{version}
%dir %{_libdir}/glusterfs/%{version}/scheduler
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/scheduler/*.so
%dir %{_libdir}/glusterfs/%{version}/transport
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/transport/*/*.so
%dir %{_libdir}/glusterfs/%{version}/xlator
%dir %{_libdir}/glusterfs/%{version}/xlator/*
%attr(755,root,root) %{_libdir}/glusterfs/%{version}/xlator/*/*.so

##%dir %{_libdir}/glusterfs/%{version}/*
##%dir %{_libdir}/glusterfs/%{version}/*/*
##%attr(755,root,root) %{_libdir}/glusterfs/%{version}/*/*/*.so
##%attr(755,root,root) %{_libdir}/glusterfs/*/*/*/*so
%dir /var/log/glusterfs


%files server
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*
%attr(755,root,root) %{_sbindir}/glusterfsd


%files client
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README
%attr(755,root,root) %{_sbindir}/glusterfs
%attr(755,root,root) /sbin/mount.glusterfs

%files devel
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS
%{_libdir}/libglusterfs.a
%{_libdir}/libglusterfs.la
##%{_includedir}/*.h
