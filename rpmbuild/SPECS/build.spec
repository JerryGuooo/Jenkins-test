##### HEADER SECTION #####
Name:           %{pkg_name}
Version:        %{pkg_version}
Release:        %{pkg_release}
Summary:        Rpm package for %{name}

License:        GPL
URL:            https://www.cyberx.com
Source0:        %{name}-%{version}-%{release}.jar
Source1:	%{name}.service
Source2:	bootstrap.yml

Requires:       shadow-utils,bash
BuildRequires:	systemd
%{?systemd_requires}

BuildArch:      noarch

%description
%{summary}

##### PREPARATION SECTION #####
%prep

# empty section

##### BUILD SECTION #####
%build

# empty section

##### PREINSTALL SECTION #####
%pre

## create cyberx-ems service user
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -s /sbin/nologin \
    -c "Useful comment about the purpose of this account" %{name}
exit 0

##### INSTALL SECTION #####
%install

app_dir=%{buildroot}/opt/%{name}
config_dir=%{buildroot}/opt/%{name}/config
service_dir=%{buildroot}%{_unitdir}

# cleanup build root
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# create app folder
mkdir -p $app_dir

# create data folder
mkdir -p $config_dir

# create service folder
mkdir -p $service_dir

# copy all files
cp %{SOURCE0} $app_dir
cp %{SOURCE1} $service_dir
cp %{SOURCE2} $config_dir
##### FILES SECTION #####
%files

# define default file attributes, (file mode, user, group, dir mode)
%defattr(-,%{name},%{name},-)

# list of directories that are packaged
# %dir %attr(660, -, -) /var/opt/spring-starter

# list of files that are packaged
/opt/%{name}/%{name}-%{version}-%{release}.jar
/opt/%{name}/config/bootstrap.yml
/usr/lib/systemd/system/%{name}.service

##### POST INSTALL SECTION #####
%post

# ensure Spring Starter service is enabled and running
%systemd_post %{name}.service
%{_bindir}/systemctl enable %{name}.service
%{_bindir}/systemctl start %{name}.service

##### UNINSTALL SECTION #####
%preun

# ensure Spring Starter service is disabled and stopped
%systemd_preun %{name}.service

%postun

case "$1" in
	0) # This is a package remove
		# remove app and data folders
		rm -rf %{app_dir}/%{name}-%{version}.jar
		rm -rf /usr/lib/systemd/system/%{name}.service
	;;
	1) # This is a package upgrade
		# do nothing
	;;
esac

# ensure Spring Starter service restartet if an upgrade is performed
%systemd_postun_with_restart %{name}.service

##### CHANGELOG SECTION #####
%changelog

* Wed Mar 20 2019 Janik vonRotz <ops@cyberx.com> - 2.2.0-1
- First cyberx-ems package
