%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:           ipmi-configurator
Version:        0.1
Release:        1%{?dist}
Summary:        Enforce PEF filter for IPMI
Group:          Monitoring

License:        GPL 3.0
URL:            https://git.gsi.de/m.dessalvi/ipmi-configurator
Source0:        %{name}-%{version}.tar.gz

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%{?systemd_requires}
BuildRequires:  systemd

BuildRoot:      %{_tmppath}/%{name}-%{version}-1-root

%description
Set IPMI PEF & Thresholds.

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -vp  %{buildroot}
mkdir -vp %{buildroot}%{_unitdir}/
cp usr/lib/systemd/system/%{name}.service %{buildroot}%{_unitdir}/
cp usr/lib/systemd/system/%{name}.timer %{buildroot}%{_unitdir}/

# in builddir
cp -a * %{buildroot}

%clean
rm -rf %{buildroot}
 
%post
systemctl enable %{name}.timer
systemctl start %{name}.timer

%preun
%systemd_preun %{name}.timer

%postun
%systemd_postun_with_restart %{name}.service
%systemd_postun_with_restart %{name}.timer

%files
%defattr(-,root,root,-)
%config /etc/ipmi-configurator/ipmi_sensors.ini
%doc usr/share/doc/ipmi-configurator-%{version}/README.md
%{_bindir}/ipmi_configurator.py
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer

%changelog
* Fri Feb 23 2018 Matteo <m.dessalvi@gsi.de> - 0.1
- Full commit history: https://git.gsi.de/m.dessalvi/ipmi-configurator/commits/master
