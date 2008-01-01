# TODO: Package examples ?
Summary:	Clustered File Storage that can scale to peta bytes
Summary(pl.UTF-8):	Klastrowy system przechowywania plików skalujący się do petabajtów
Name:		glusterfs
Version:	1.3.7
Release:	0.1
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
w jeden duży, równoległy sieciowy system plików. GlusterFS to jeden z
najbardziej wyszukanych systemów plików jeśli chodzi o możliwości i
rozszerzalność. Zapożycza potężną ideę o nazwie Translators z jądra
GNU Hurd. Duża część kodu GlusterFS działa w przestrzeni użytkownika i
jest łatwo zarządzalna.

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

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README 
%attr(755,root,root) %{_libdir}/*.so.*
%dir %{_libdir}/glusterfs/*
%dir %{_libdir}/glusterfs/*/*
%attr(755,root,root) %{_libdir}/glusterfs/*/*/*so
%dir %{_libdir}/glusterfs/*/*/*
%attr(755,root,root) %{_libdir}/glusterfs/*/*/*/*so

%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}/%{name}*
%attr(755,root,root) /sbin/mount.*
