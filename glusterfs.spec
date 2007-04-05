Summary:	Clustered File Storage that can scale to peta bytes
#Summary(pl.UTF-8):	-
Name:		glusterfs
Version:	1.2.3
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://ftp.zresearch.com/pub/gluster/glusterfs/1.2/%{name}-%{version}.tar.gz
# Source0-md5:	f0a545f10176a77d93472b64db061781
Patch0:		%{name}-DESTDIR.patch
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

#description -l pl.UTF-8

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/*.so
%dir %{_libdir}/glusterfs/*
%attr(755,root,root) %{_libdir}/glusterfs/*/*so
%dir %{_libdir}/glusterfs/*/*
%attr(755,root,root) %{_libdir}/glusterfs/*/*/*so
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}/%{name}*
%attr(755,root,root) /sbin/mount.*
