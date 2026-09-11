Summary:	OWASP Core Rule Set activation for nginx ModSecurity
Summary(pl.UTF-8):	Aktywacja OWASP Core Rule Set dla modułu ModSecurity nginx-a
Name:		nginx-mod_http_modsecurity_crs
# loader layout follows CRS 4 (plugins/*-{config,before,after}.conf), not a CRS release
Version:	4.0
Release:	1
License:	Apache v2.0
Group:		Daemons
Source0:	%{name}.conf
URL:		https://coreruleset.org/
# crs-setup.conf.example is copied at build time
BuildRequires:	modsecurity-crs >= 4
BuildRequires:	rpmbuild(macros) >= 1.268
# /etc/nginx/modsecurity/rules.d loaded by main.conf
Requires:	nginx-mod_http_modsecurity >= 1.31.5-2
Requires:	modsecurity-crs >= 4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nginx

%description
Loads the OWASP Core Rule Set (modsecurity-crs package) into nginx
ModSecurity: CRS setup, plugins and rules in the order CRS requires.
The CRS setup file for nginx lives in
/etc/nginx/modsecurity/crs-setup.conf.

%description -l pl.UTF-8
Ładuje OWASP Core Rule Set (pakiet modsecurity-crs) do modułu
ModSecurity nginx-a: konfigurację CRS, wtyczki i reguły w kolejności
wymaganej przez CRS. Plik konfiguracyjny CRS dla nginx-a to
/etc/nginx/modsecurity/crs-setup.conf.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modsecurity/rules.d

cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/modsecurity/rules.d/10_crs.conf
# rule 901001 rejects every request unless a setup file is loaded before rules/
cp -p %{_datadir}/modsecurity-crs/crs-setup.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/modsecurity/crs-setup.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q nginx reload

%postun
if [ "$1" = "0" ]; then
	%service -q nginx reload
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modsecurity/crs-setup.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modsecurity/rules.d/10_crs.conf
