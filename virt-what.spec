Name:           virt-what
Version:        1.3
Release:        4.4%{?dist}
Summary:        Detect if we are running in a virtual machine

Group:          Applications/Emulators
License:        GPLv2+
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

URL:            http://people.redhat.com/~rjones/virt-what/
Source0:        http://people.redhat.com/~rjones/virt-what/files/%{name}-%{version}.tar.gz

# Include the .gitignore file from 1.3 so that the patches below can
# patch this file.
Source1:        gitignore-1.3

Patch0001:      0001-Add-detection-of-IBM-PowerVM-Lx86-Linux-x86-emulator.patch
Patch0002:      0002-Detect-Microsoft-Hyper-V.patch
Patch0003:      0003-Add-detection-of-Hitachi-Virtualization-Manager-HVM-.patch
Patch0004:      0004-Set-LANG-C-when-running-external-dmidecode-command.patch
Patch0005:      0005-Add-a-test-for-baremetal.patch
Patch0006:      0006-Add-test-for-VMware-with-data-from-ESX-4.1-thanks-Ma.patch
Patch0007:      0007-Add-tests-for-KVM-and-QEMU.patch
Patch0008:      0008-Add-test-files-to-EXTRA_DIST.patch
Patch0009:      0009-Fix-tests-Add-proc-self-status-to-test-roots.patch
Patch0010:      0010-Add-regression-test-for-RHEL-5-Xen-Dom0.patch
Patch0011:      0011-Add-regression-test-for-RHEL-5-Xen-DomU-paravirt.patch
Patch0012:      0012-Add-regression-test-for-RHEL-5-Xen-DomU-HVM-aka-full.patch
Patch0013:      0013-Add-missing-files-to-EXTRA_DIST.patch
Patch0014:      0014-Add-support-for-Linux-kernels-with-pv_ops-running-on.patch
Patch0015:      0015-Add-sys-hypervisor-files-from-RHEL-5-Xen-DomU-to-EXT.patch
Patch0016:      0016-Add-sys-hypervisor-test-files-from-RHEL-5-Xen-Dom0.patch
Patch0017:      0017-Add-test-for-z-VM-on-IBM-SystemZ-mainframes-thanks-D.patch
Patch0018:      0018-Add-additional-facts-about-IBM-SystemZ-mainframes-th.patch
Patch0019:      0019-Confirm-Microsoft-Hyper-V-and-add-a-regression-test.patch
Patch0020:      0020-Various-improvements-to-the-manual-page-RHBZ-672285.patch

# This is provided by the build root, but we make it explicit
# anyway in case this was dropped from the build root in future.
BuildRequires:  /usr/bin/pod2man

# virt-what script uses dmidecode and getopt (from util-linux-ng).
# RPM cannot detect this so make the dependencies explicit here.
%ifarch %{ix86} x86_64 ia64
Requires:       dmidecode
%endif
%if 0%{?rhel} >= 6
Requires:       util-linux-ng
%endif


%description
virt-what is a shell script which can be used to detect if the program
is running in a virtual machine.

The program prints out a list of "facts" about the virtual machine,
derived from heuristics.  One fact is printed per line.

If nothing is printed and the script exits with code 0 (no error),
then it can mean either that the program is running on bare-metal or
the program is running inside a type of virtual machine which we don't
know about or cannot detect.

Current types of virtualization detected:
KVM, Xen, unaccelerated QEMU, VMWare, VirtualBox, VirtualPC,
OpenVZ, Virtuozzo, User-Mode Linux (UML).


%prep
%setup -q

cp %{SOURCE1} .gitignore

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1

# Patch doesn't set +x permissions on new files so we have to
# do it manually:
chmod +x tests/test-*.sh tests/*/sbin/*

# Grrr patch refuses to create empty files:
mkdir tests/esx4.1/proc/self
touch tests/esx4.1/proc/self/status
mkdir tests/qemu/proc/self
touch tests/qemu/proc/self/status
touch tests/rhel5-xen-dom0/proc/xen/privcmd
touch tests/rhel5-xen-dom0/proc/xen/xenbus
touch tests/rhel5-xen-domU-pv/proc/xen/capabilities
touch tests/rhel5-xen-domU-pv/proc/xen/privcmd
touch tests/rhel5-xen-domU-pv/proc/xen/xenbus


%build
%configure
make


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_sbindir}/virt-what
%{_libexecdir}/virt-what-cpuid-helper
%{_mandir}/man1/*.1*


%changelog
* Mon Jan 31 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.4
- Various improvements to the wording in the manual page.
  resolves: rhbz#672285
- Confirm support for Microsoft HyperV and add a regression test.
  resolves: rhbz#670272

* Mon Jan 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.3
- Don't depend on util-linux-ng on RHEL 5.

* Mon Jan 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.2
- Add support for Microsoft HyperV (RHBZ#670272).
- Add support for Hitachi Virtage (RHBZ#670530).
- Add support for EC2 (Xen) instances (RHBZ#671126).  This includes
  backporting the test framework and enabling tests.
- Add support for IBM Systemz z/VM, LPAR (RHBZ#671132).

* Mon Jan 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3-4.1
- Add support for IBM PowerVM Lx86 Linux/x86 emulator (RHBZ#668857).
- Move configure into build (not prep).

* Tue Dec 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Rebuild on all architectures.

* Thu Oct 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- Initial import into Fedora.

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Make changes suggested by reviewer (RHBZ#644259).

* Tue Oct 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial release.
