# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmods

Name:		xtables-addons-kmod
Summary:	Kernel module (kmod) for xtables-addons
Version:	1.25
Release:	1%{?dist}
License:	GPLv2
Group:		System Environment/Kernel
URL:		http://xtables-addons.sourceforge.net
Source0:	http://downloads.sourceforge.net/xtables-addons/xtables-addons-%{version}.tar.bz2
Source11:	xtables-addons-kmodtool-excludekernel-filterfile
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:	%{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:	i586 i686 x86_64 ppc ppc64

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

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
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
for kernel_version in %{?kernel_versions} ; do
	cp -a xtables-addons-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
	export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
	make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
rm -rf %{buildroot}
for kernel_version  in %{?kernel_versions} ; do
	find _kmod_build_${kernel_version%%___*}/extensions -name "*.ko" -exec mv {} _kmod_build_${kernel_version%%___*}/extensions ";"
	install -dm 755 %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
	install -pm 755 _kmod_build_${kernel_version%%___*}/extensions/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done
chmod u+x %{buildroot}/lib/modules/*/extra/*/*
%{?akmod_install}

%clean
rm -rf %{buildroot}


%changelog
* Mon Apr 26 2010 Chen Lei <supercyper@163.com> - 1.25-1
- update to 1.25

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.24-1.1
- rebuild for new kernel

* Thu Mar 18 2010 Chen Lei <supercyper@163.com> - 1.24-1
- initial rpm build
