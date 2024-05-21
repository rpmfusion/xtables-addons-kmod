# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:		xtables-addons-kmod
Summary:	Kernel module (kmod) for xtables-addons
Version:	2.13
Release:	3%{?dist}
License:	GPLv2
Group:		System Environment/Kernel
URL:		http://xtables-addons.sourceforge.net
Source0:	http://dl.sourceforge.net/xtables-addons/Xtables-addons/xtables-addons-%{version}.tar.xz
#Source11:	xtables-addons-kmodtool-excludekernel-filterfile
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:	%{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Xtables-addons provides extra modules for iptables not present in the kernel, 
and is the successor of patch-o-matic. Extensions includes new targets like 
TEE, TARPIT, CHAOS, or modules like geoip, ipset, and account.

This package provides the xtables-addons kernel modules. You must also install 
the xtables-addons package in order to make use of these modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
for kernel_version in %{?kernel_versions} ; do
	cp -a xtables-addons-%{version} _kmod_build_${kernel_version%%___*}
	%if 0%{?rhel}
	# FIXME!!! TARPIT doesn't build with the rhel kernel
	sed -i 's/build_TARPIT=m//' _kmod_build_${kernel_version%%___*}/mconfig
	%endif
done


%build
for kernel_version  in %{?kernel_versions} ; do
	export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
	make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
for kernel_version  in %{?kernel_versions} ; do
	export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
	make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions _emodinst_ INSTALL_MOD_PATH=%{buildroot}%{_prefix} ext-mod-dir=%{kmodinstdir_postfix}
done
%{?akmod_install}

%clean
rm -rf %{buildroot}

%changelog
* Tue May 21 2024 Nicolas Chauvet <kwizart@gmail.com> - 2.13-3
- Rebuilt

* Tue Sep 03 2019 Leigh Scott <leigh123linux@gmail.com> - 2.13-2
- Rebuild for new el7 kernel

* Mon Jul 03 2017 Nicolas Chauvet <kwizart@gmail.com> - 2.13-1
- Update to 2.13
- Avoid xt_TARPIT on rhel kernel

* Wed Jun 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.48
- Rebuilt for kernel

* Tue Jun 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.47
- Rebuilt for kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.46
- Rebuilt for kernel

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.45
- Rebuilt for kernel

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.44
- Rebuilt for kernel

* Sat May 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.43
- Rebuilt for kernel

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.42
- Rebuilt for kernel

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.41
- Rebuilt for kernel

* Mon Mar 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.40
- Rebuilt for kernel

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.39
- Rebuilt for kernel

* Fri Mar 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.38
- Rebuilt for kernel

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.37
- Rebuilt for kernel

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.36
- Rebuilt for kernel

* Wed Feb 04 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.35
- Rebuilt for kernel

* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.34
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.33
- Rebuilt for kernel

* Thu Dec 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.32
- Rebuilt for kernel

* Sat Dec 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.31
- Rebuilt for kernel

* Sun Nov 23 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.30
- Rebuilt for kernel

* Sun Nov 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.29
- Rebuilt for kernel

* Mon Nov 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.28
- Rebuilt for kernel

* Fri Oct 31 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.27
- Rebuilt for kernel

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.26
- Rebuilt for kernel

* Thu Oct 16 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.25
- Rebuilt for kernel

* Fri Oct 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.24
- Rebuilt for kernel

* Tue Oct 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.23
- Rebuilt for kernel

* Fri Sep 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.22
- Rebuilt for kernel

* Thu Sep 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.21
- Rebuilt for kernel

* Tue Sep 09 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.20
- Rebuilt for kernel

* Sat Aug 30 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.19
- Rebuilt for kernel

* Wed Aug 20 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.18
- Rebuilt for kernel

* Wed Aug 20 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.17
- Rebuilt for kernel

* Fri Aug 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.16
- Rebuilt for kernel

* Wed Aug 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.15
- Rebuilt for kernel

* Sat Aug 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.14
- Rebuilt for kernel

* Fri Aug 01 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.13
- Rebuilt for kernel

* Fri Jul 18 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.12
- Rebuilt for kernel

* Thu Jul 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.11
- Rebuilt for kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.10
- Rebuilt for kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.9
- Rebuilt for kernel

* Tue Jul 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.8
- Rebuilt for kernel

* Tue Jun 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.7
- Rebuilt for kernel

* Fri Jun 13 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.6
- Rebuilt for kernel

* Sun Jun 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.5
- Rebuilt for kernel

* Tue Jun 03 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.4
- Rebuilt for kernel

* Thu May 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.3
- Rebuilt for kernel

* Thu May 08 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.2
- Rebuilt for kernel

* Wed Apr 30 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1.1
- Rebuilt for kernel

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.5-1
- Update to 2.5

* Sun Jan 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4-1
- Update to 2.4

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-4.1
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-3.1
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-2.1
- Rebuilt for current kernel

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-1.1
- Rebuilt for f20 final kernel

* Tue Jun 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3-1
- Update to 2.3

* Thu Apr 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.2-1
- Update to 2.2

* Mon Jan 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1-1
- Update to 2.1

* Mon Jan 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.6
- Rebuilt for updated kernel

* Sun Jan 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.5
- Rebuilt for updated kernel

* Thu Jan 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.4
- Rebuilt for f18 final kernel

* Fri Dec 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.3
- Rebuilt for current f18 kernel

* Wed Dec 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.2
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1.1
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.47.1-1
- Update to 1.47.1
- Rebuilt for Fedora 18 Beta kernel

* Wed Oct 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.46-1
- Update to 1.46

* Tue Jul 31 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.45-1
- Update to 1.45

* Thu May 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-2
- Fix build

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.4
- rebuild for updated kernel

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.3
- rebuild for updated kernel

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.2
- rebuild for updated kernel

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1.1
- rebuild for updated kernel

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.42-1
- Update to 1.42

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-2
- rebuild for beta kernel

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-1.1
- Rebuild for UsrMove

* Tue Jan 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.41-1
- Update to 1.41

* Thu Nov 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.39-1
- Update to 1.39

* Wed Oct 27 2010 Chen Lei <supercyper@163.com> - 1.30-1
- update to 1.30

* Sun Jul 25 2010 Chen Lei <supercyper@163.com> - 1.28-1
- update to 1.28

* Mon Jun 28 2010 Chen Lei <supercyper@163.com> - 1.27-2
- rebuild for kernel 2.6.35

* Mon May 31 2010 Chen Lei <supercyper@163.com> - 1.27-1
- update to 1.27

* Thu May 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.4
- rebuild for new kernel

* Mon May 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.3
- rebuild for new kernel

* Fri May 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.2
- rebuild for new kernel

* Tue May 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.26-1.1
- rebuild for new kernel

* Sun May 02 2010 Chen Lei <supercyper@163.com> - 1.26-1
- update to 1.26

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.25-1.1
- rebuild for new kernel

* Mon Apr 26 2010 Chen Lei <supercyper@163.com> - 1.25-1
- update to 1.25

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.24-1.1
- rebuild for new kernel

* Thu Mar 18 2010 Chen Lei <supercyper@163.com> - 1.24-1
- initial rpm build
