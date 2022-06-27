# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:       xtables-addons-kmod
Summary:    Kernel module (kmod) for xtables-addons
Version:    3.21
Release:    1%{?dist}
License:    GPLv2
URL:        https://inai.de/projects/xtables-addons/
Source0:    https://inai.de/files/xtables-addons/xtables-addons-%{version}.tar.xz
Patch0:     el8_fix.patch

BuildRequires:    %{_bindir}/kmodtool
%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

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

%autosetup -c -T -a 0 -p 0
ls
for kernel_version in %{?kernel_versions} ; do
    cp -a xtables-addons-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" \
    M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p  $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 0755 _kmod_build_${kernel_version%%___*}/extensions/*.ko \
         $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Mon Jun 27 2022 Leigh Scott <leigh123linux@gmail.com> - 3.21-1
- Release 3.21

* Sun Apr 17 2022 Leigh Scott <leigh123linux@gmail.com> - 3.20-1
- Release 3.20

* Tue Mar 22 2022 Leigh Scott <leigh123linux@gmail.com> - 3.19-1
- Release 3.19

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 27 2021 Leigh Scott <leigh123linux@gmail.com> - 3.18-3
- Manually install .ko files

* Tue Jun 08 2021 Nicolas Chauvet <kwizart@gmail.com> - 3.18-2
- rebuilt

* Sun Mar 21 2021 Leigh Scott <leigh123linux@gmail.com> - 3.18-1
- Release 3.18

* Tue Feb 23 2021 Leigh Scott <leigh123linux@gmail.com> - 3.15-1
- Release 3.15

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Leigh Scott <leigh123linux@gmail.com> - 3.13-1
- Release 3.13

* Wed Oct 28 2020 Leigh Scott <leigh123linux@gmail.com> - 3.11-2
- Fix module path for fedora < 33 and el

* Wed Oct 28 2020 Leigh Scott <leigh123linux@gmail.com> - 3.11-1
- Release 3.11

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Aug 08 2020 Leigh Scott <leigh123linux@gmail.com> - 3.10-1
- Release 3.10

* Wed Apr 22 2020 Leigh Scott <leigh123linux@gmail.com> - 3.9-1
- Release 3.9

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 3.7-1
- Release 3.7

* Sun Oct 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 3.5-1
- Release 3.5

* Mon Sep 02 2019 Leigh Scott <leigh123linux@gmail.com> - 3.3-3
- Patch for kernel-5.2 (rfbz #5376)

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 02 2019 Robert-André Mauchin <zebob.m@gmail.com>- 3.3-1
- Release 3.3

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.2-1
- Update to 3.2
- Remove Group tag
- Remove clean section

* Sat Sep 01 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-1
- Update to 3.1

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.0-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.0-1
- Update to 3.0

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.14-1
- Update to 2.14

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Nicolas Chauvet <kwizart@gmail.com> - 2.13-1
- Update to 2.13

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Nicolas Chauvet <kwizart@gmail.com> - 2.12-1
- Update to 2.12

* Sat Oct 01 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.11-2
- Switch to akmod build

* Wed Jun 22 2016 Nicolas Chauvet <kwizart@gmail.com> - 2.11-1
- Update to 2.11

* Sun Jan 03 2016 Nicolas Chauvet <kwizart@gmail.com> - 2.10-1
- Update to 2.10

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.9-1
- Update to 2.9

* Tue Oct 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.6
- Rebuilt for kernel

* Wed Sep 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.5
- Rebuilt for kernel

* Wed Sep 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.4
- Rebuilt for kernel

* Fri Aug 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.3
- Rebuilt for kernel

* Thu Aug 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.2
- Rebuilt for kernel

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1.1
- Rebuilt for kernel

* Thu Jul 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.7-1
- Update to 2.7

* Thu Jul 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.29
- Rebuilt for kernel

* Fri Jul 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.28
- Rebuilt for kernel

* Thu Jul 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.27
- Rebuilt for kernel

* Thu Jul 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.26
- Rebuilt for kernel

* Sun Jun 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.25
- Rebuilt for kernel

* Wed Jun 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.24
- Rebuilt for kernel

* Tue Jun 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.23
- Rebuilt for kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.22
- Rebuilt for kernel

* Wed May 20 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.21
- Rebuilt for kernel

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.20
- Rebuilt for kernel

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.19
- Rebuilt for kernel

* Sat May 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.18
- Rebuilt for kernel

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.17
- Rebuilt for kernel

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.16
- Rebuilt for kernel

* Mon Mar 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.15
- Rebuilt for kernel

* Fri Mar 27 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.14
- Rebuilt for kernel

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.13
- Rebuilt for kernel

* Sat Mar 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.12
- Rebuilt for kernel

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.11
- Rebuilt for kernel

* Fri Mar 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.10
- Rebuilt for kernel

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.9
- Rebuilt for kernel

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.8
- Rebuilt for kernel

* Wed Feb 04 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.7
- Rebuilt for kernel

* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.6
- Rebuilt for kernel

* Wed Jan 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.5
- Rebuilt for kernel

* Thu Jan 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.4
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.3
- Rebuilt for kernel

* Fri Dec 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.2
- Rebuilt for kernel

* Sun Dec 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1.1
- Rebuilt for kernel

* Fri Dec 05 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.6-1
- Rebuilt for f21 final kernel

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
