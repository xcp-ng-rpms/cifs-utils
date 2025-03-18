#% define pre_release rc1
%define pre_release %nil

Name:            cifs-utils
Version:         6.2
Release:         10%{pre_release}%{?dist}
Summary:         Utilities for mounting and managing CIFS mounts

Group:           System Environment/Daemons
License:         GPLv3
URL:             http://linux-cifs.samba.org/cifs-utils/
BuildRoot:       %{_tmppath}/%{name}-%{version}%{pre_release}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   libcap-ng-devel libtalloc-devel krb5-devel keyutils-libs-devel autoconf automake libwbclient-devel

Requires:        keyutils
Requires(post):  /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

Source0:         ftp://ftp.samba.org/pub/linux-cifs/cifs-utils/%{name}-%{version}%{pre_release}.tar.bz2
Patch1:          0001-get-setcifsacl-fix-bad-bit-shifts.patch
Patch2:          0002-getcifsacl-remove-some-dead-code.patch
Patch3:          0003-asn1-remove-some-usused-functions.patch
Patch4:          0004-data_blob-clean-out-unused-functions.patch
Patch5:          0005-mount.cifs-fix-bad-free-of-string-returned-by-dirnam.patch
Patch6:          0001-asn1-fix-use-after-free-in-asn1_write.patch
Patch7:          0001-cifs-use-krb5_kt_default-to-determine-default-keytab.patch
Patch8:          0001-autoconf-fix-link-of-libwbclient.patch
Patch9:          0002-mount.cifs-on-2nd-try-mount.cifs-must-also-uppercase.patch
Patch10:         0003-mtab.c-include-paths.h-for-_PATH_MOUNTED.patch
Patch11:         0004-manpage-clarify-use-of-backupuid-and-backupgid-in-mo.patch
Patch12:         0005-mount.cifs-ignore-x-mount-options.patch
Patch13:         0001-autoconf-Use-DEFS-when-building-idmapwb.so.patch
Patch14:         0007-aclocal-fix-typo-in-idmap.m4.patch
Patch15:         0008-mount.cifs-Removed-extra-comma-in-front-of-domain.patch
Patch16:         0009-mount.cifs-Accept-empty-domains-on-the-command-line.patch
Patch17:         0010-mount.cifs-Fixed-command-line-parsing-and-aligned-wi.patch
Patch18:         0011-mount.cifs-Remove-unneeded-stdbool-header-include.patch
Patch19:         0012-manpage-document-mfsymlinks-in-the-mount.cifs-man-pa.patch

%description
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains tools for mounting
shares on Linux using the SMB/CIFS protocol. The tools in this package
work in conjunction with support in the kernel to allow one to mount a
SMB/CIFS share onto a client and use it as if it were a standard Linux
file system.

%package devel
Summary:        Files needed for building plugins for cifs-utils
Group:          Development/Libraries

%description devel
The SMB/CIFS protocol is a standard file sharing protocol widely deployed
on Microsoft Windows machines. This package contains the header file
necessary for building ID mapping plugins for cifs-utils.

%prep
%setup -q -n %{name}-%{version}%{pre_release}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%build
%configure --prefix=/usr ROOTSBINDIR=%{_sbindir}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.idmap.conf %{buildroot}%{_sysconfdir}/request-key.d
install -m 644 contrib/request-key.d/cifs.spnego.conf %{buildroot}%{_sysconfdir}/request-key.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
%{_bindir}/getcifsacl
%{_bindir}/setcifsacl
%{_bindir}/cifscreds
%{_sbindir}/mount.cifs
%{_sbindir}/cifs.upcall
%{_sbindir}/cifs.idmap
%{_libdir}/%{name}/idmapwb.so
%{_mandir}/man1/getcifsacl.1.gz
%{_mandir}/man1/setcifsacl.1.gz
%{_mandir}/man1/cifscreds.1.gz
%{_mandir}/man8/cifs.upcall.8.gz
%{_mandir}/man8/cifs.idmap.8.gz
%{_mandir}/man8/mount.cifs.8.gz
%{_mandir}/man8/idmapwb.8.gz
%ghost %{_sysconfdir}/cifs-utils/idmap-plugin
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.idmap.conf
%config(noreplace) %{_sysconfdir}/request-key.d/cifs.spnego.conf

%post
/usr/sbin/alternatives --install /etc/cifs-utils/idmap-plugin cifs-idmap-plugin %{_libdir}/%{name}/idmapwb.so 10

%preun
if [ $1 = 0 ]; then
	/usr/sbin/alternatives --remove cifs-idmap-plugin %{_libdir}/%{name}/idmapwb.so
fi

%files devel
%{_includedir}/cifsidmap.h

%changelog
* Mon Apr 03 2017 Sachin Prabhu <sprabhu@redhat.com> - 6.2-10
- aclocal: fix typo in idmap.m4
- mount.cifs: Removed extra comma in front of domain
- mount.cifs: Accept empty domains on the command line
- mount.cifs: Fixed command line parsing and aligned with kernel
- mount.cifs: Remove unneeded stdbool header include
- manpage: document mfsymlinks in the mount.cifs man page

* Thu Jun 30 2016 Sachin Prabhu <sprabhu@redhat.com> - 6.2-9
- Use $(DEFS) when building idmapwb.so

* Thu Jun 30 2016 Sachin Prabhu <sprabhu@redhat.com> - 6.2-8
- Prevent unnecessary linking of libwbclient
- Uppercase orig_dev on 2nd try at mounting
- Include paths.h in mtab.c
- Clarify use of backupuid/backupgid in manpage
- Ignore x-* mount options

* Fri Aug 29 2014 Sachin Prabhu <sprabhu@redhat.com> - 6.2-7
-  use krb5_kt_default() to determine default keytab location (bz#1083795)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 6.2-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.2-5
- Mass rebuild 2013-12-27

* Mon Oct 14 2013 Jeff Layton <jlayton@redhat.com> 6.2-4
- fix use-after-free in asn1_write

* Fri Oct 11 2013 Jeff Layton <jlayton@redhat.com> 6.2-3
- fixes for bugs reported by coverity:
- update bad bit shift patch with one that patches getcifsacl.c too
- remove some dead code from getcifsacl.c, asn1.c, and data_blob.c
- fix bad handling of allocated memory in del_mtab in mount.cifs.c

* Wed Oct 09 2013 Jeff Layton <jlayton@redhat.com> 6.2-2
- fix bad bit shift in setcifsacl.c (bz#1016932)

* Mon Oct 07 2013 Jeff Layton <jlayton@redhat.com> 6.2-1
- update to 6.2 release

* Tue Jul 16 2013 Jeff Layton <jlayton@redhat.com> 6.1-3
- allow setcifsacl to work if plugin can't be loaded (#985067)

* Tue Jul 16 2013 Jeff Layton <jlayton@redhat.com> 6.1-2
- Convert idmapping plugin symlink to use alternatives system (#984643)

* Wed Jul 03 2013 Jeff Layton <jlayton@redhat.com> 6.1-1
- update to 6.1 release

* Mon Mar 25 2013 Jeff Layton <jlayton@redhat.com> 6.0-1
- update to 6.0 release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Jeff Layton <jlayton@redhat.com> 5.9-3
- comment fixes in cifsidmap.h

* Sun Jan 13 2013 Jeff Layton <jlayton@redhat.com> 5.9-2
- fix regression in credential file handling

* Mon Jan 07 2013 Jeff Layton <jlayton@redhat.com> 5.9-1
- update to 5.9
- move mount.cifs to /usr/sbin per new packaging guidelines
- add -devel package to hold cifsidmap.h

* Sun Nov 11 2012 Jeff Layton <jlayton@redhat.com> 5.8-1
- update to 5.8

* Wed Nov 07 2012 Jeff Layton <jlayton@redhat.com> 5.7-3
- update to latest patches queued for 5.8. More idmapping and ACL tool fixes.

* Sun Nov 04 2012 Jeff Layton <jlayton@redhat.com> 5.7-2
- update to latest patches queued for 5.8. Mostly idmapping and ACL tool fixes.

* Tue Oct 09 2012 Jeff Layton <jlayton@redhat.com> 5.7-1
- update to 5.7

* Fri Aug 24 2012 Jeff Layton <jlayton@redhat.com> 5.6-2
- update to current upstream head

* Thu Jul 26 2012 Jeff Layton <jlayton@redhat.com> 5.6-1
- update to 5.6

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Jeff Layton <jlayton@redhat.com> 5.5-2
- remove -Werror flag
- enable PIE and RELRO

* Wed May 30 2012 Jeff Layton <jlayton@redhat.com> 5.5-1
- update to 5.5

* Wed Apr 25 2012 Jeff Layton <jlayton@redhat.com> 5.4-2
- rebuild to fix dependencies due to libwbclient changes

* Wed Apr 18 2012 Jeff Layton <jlayton@redhat.com> 5.4-1
- update to 5.4
- add patch to fix up more warnings

* Mon Mar 19 2012 Jeff Layton <jlayton@redhat.com> 5.3-4
- fix tests for strtoul success (bz# 800621)

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-3
- revert mount.cifs move. It's unnecessary at this point.

* Wed Feb 08 2012 Jeff Layton <jlayton@redhat.com> 5.3-2
- move mount.cifs to /usr/sbin per new packaging guidelines

* Sat Jan 28 2012 Jeff Layton <jlayton@redhat.com> 5.3-1
- update to 5.3

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-2
- add /etc/request-key.d files

* Fri Dec 09 2011 Jeff Layton <jlayton@redhat.com> 5.2-1
- update to 5.2

* Fri Sep 23 2011 Jeff Layton <jlayton@redhat.com> 5.1-1
- update to 5.1
- add getcifsacl and setcifsacl to package

* Fri Jul 29 2011 Jeff Layton <jlayton@redhat.com> 5.0-2
- mount.cifs: fix check_newline retcode check (bz# 726717)

* Wed Jun 01 2011 Jeff Layton <jlayton@redhat.com> 5.0-1
- update to 5.0

* Mon May 16 2011 Jeff Layton <jlayton@redhat.com> 4.9-2
- mount.cifs: pass unadulterated device string to kernel (bz# 702664)

* Fri Mar 04 2011 Jeff Layton <jlayton@redhat.com> 4.9-1
- update to 4.9

* Tue Feb 08 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-4
- mount.cifs: reenable CAP_DAC_READ_SEARCH when mounting (bz# 675761)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-2
- mount.cifs: don't update mtab if it's a symlink (bz# 674101)

* Fri Jan 21 2011 Jeff Layton <jlayton@redhat.com> 4.8.1-1
- update to 4.8.1

* Sat Jan 15 2011 Jeff Layton <jlayton@redhat.com> 4.8-1
- update to 4.8

* Tue Oct 19 2010 Jeff Layton <jlayton@redhat.com> 4.7-1
- update to 4.7

* Fri Jul 30 2010 Jeff Layton <jlayton@redhat.com> 4.6-1
- update to 4.6

* Tue Jun 01 2010 Jeff Layton <jlayton@redhat.com> 4.5-2
- mount.cifs: fix parsing of cred= option (BZ#597756)

* Tue May 25 2010 Jeff Layton <jlayton@redhat.com> 4.5-1
- update to 4.5

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-3
- mount.cifs: fix regression in prefixpath patch

* Thu Apr 29 2010 Jeff Layton <jlayton@redhat.com> 4.4-2
- mount.cifs: strip leading delimiter from prefixpath

* Wed Apr 28 2010 Jeff Layton <jlayton@redhat.com> 4.4-1
- update to 4.4

* Sat Apr 17 2010 Jeff Layton <jlayton@redhat.com> 4.3-2
- fix segfault when address list is exhausted (BZ#583230)

* Fri Apr 09 2010 Jeff Layton <jlayton@redhat.com> 4.3-1
- update to 4.3

* Fri Apr 02 2010 Jeff Layton <jlayton@redhat.com> 4.2-1
- update to 4.2

* Tue Mar 23 2010 Jeff Layton <jlayton@redhat.com> 4.1-1
- update to 4.1

* Mon Mar 08 2010 Jeff Layton <jlayton@redhat.com> 4.0-2
- fix bad pointer dereference in IPv6 scopeid handling

* Wed Mar 03 2010 Jeff Layton <jlayton@redhat.com> 4.0-1
- update to 4.0
- minor specfile fixes

* Fri Feb 26 2010 Jeff Layton <jlayton@redhat.com> 4.0-1rc1
- update to 4.0rc1
- fix prerelease version handling

* Mon Feb 08 2010 Jeff Layton <jlayton@redhat.com> 4.0a1-1
- first RPM package build

