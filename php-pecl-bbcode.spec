%define		_modname	bbcode
%define		_status		stable
Summary:	%{_modname} - parsing extension
Summary(pl.UTF-8):	%{_modname} - rozszerzenie parsujące
Name:		php-pecl-%{_modname}
Version:	1.0.2
Release:	2
License:	PHP / BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1fb6971b2758a50785f188964991ddf9
URL:		http://pecl.php.net/package/bbcode/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a quick and efficient BBCode Parsing Library.

It provides various tag types, high speed tree based parsing, callback
system, tag position restriction, Smiley Handling, Subparsing.

It will force closing BBCode tags in the good order, and closing
terminating tags at the end of the string this is in order to ensure
HTML Validity in all case.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Pakiet ten dostarcza prostego i efektywnego rozszerzenia parsującego
kod BBCode.

Umożliwia stosowanie różnego rodzaju typy znaczników, szybkie
parsowanie, system wywołań callback, ograniczanie stosowania
znaczników, obsługe emotikon, podparsowanie.

Moduł ten wymusi stosowanie znaczników zamykających BBCode w
odpowiedniej kolejności, oraz stosowanie znaczników kończących w celu
zapewnienia zgodności z HTML.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{CREDITS,TODO}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
