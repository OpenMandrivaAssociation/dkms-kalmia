%define	modname	kalmia

Name:		dkms-%{modname}
Version:	0.1
Release:	2
Summary:	Driver for Kalmia-based 4G/LTE modems
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		https://github.com/mkotsbak/Samsung-GT-B3730-linux-driver
Source0:	%{modname}-%{version}.tar.xz
#CVSID:		796fd38b68167f527980ed75a5cbfe0d802d4ece
Requires(post):	dkms
Requires(preun):dkms
BuildArch:	noarch
Suggests:	minicom

%description
This package provides the kernel driver for 4G/LTE modems using the Kalmia
chipset, ie. such as Samsung's GT-B3710 & GT-B3730.

%prep
%setup -qn %{modname}-%{version}

%build

%install
install -d %{buildroot}%{_docdir}/%{modname}
install -m644 README *.txt %{buildroot}%{_docdir}/%{modname}
install -m755 chat.sh connect_lte.sh %{buildroot}%{_docdir}/%{modname}

# DKMS stuff
install -d %{buildroot}%{_usrsrc}/%{modname}-%{version}
install -m644 Makefile kalmia.c %{buildroot}%{_usrsrc}/%{modname}-%{version}

# Configuration for dkms
cat > %{buildroot}%{_usrsrc}/%{modname}-%{version}/dkms.conf << 'EOF'
PACKAGE_NAME=%{modname}
PACKAGE_VERSION=%{version}
BUILT_MODULE_NAME="%{modname}"
DEST_MODULE_LOCATION="/kernel/drivers/usb/net"
AUTOINSTALL=yes
EOF

%post
dkms add -m %{modname} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{modname} -v %{version} --rpm_safe_upgrade || :
dkms install -m %{modname} -v %{version} --rpm_safe_upgrade || :

%preun
dkms remove -m %{modname} -v %{version} --all --rpm_safe_upgrade || :

%files
%dir %{_docdir}/%{modname}
%doc %{_docdir}/%{modname}/README
%{_docdir}/%{modname}/*.txt
%{_docdir}/%{modname}/*.sh
%{_usrsrc}/%{modname}-%{version}

