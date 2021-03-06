%define		php_name	php%{?php_suffix}
%define		modname	bbcode
%define		status		stable
Summary:	%{modname} - parsing extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie parsujące
Name:		%{php_name}-pecl-%{modname}
Version:	1.1.0
Release:	8
License:	PHP / BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-1.0.2.tgz
Patch0:		cvs2svn.patch
Patch1:		branch.diff
# Source0-md5:	1fb6971b2758a50785f188964991ddf9
URL:		http://pecl.php.net/package/bbcode/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-bbcode < 1.1.0-7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a quick and efficient BBCode Parsing Library.

It provides various tag types, high speed tree based parsing, callback
system, tag position restriction, Smiley Handling, Subparsing.

It will force closing BBCode tags in the good order, and closing
terminating tags at the end of the string this is in order to ensure
HTML Validity in all case.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Pakiet ten dostarcza prostego i efektywnego rozszerzenia parsującego
kod BBCode.

Umożliwia stosowanie różnego rodzaju typy znaczników, szybkie
parsowanie, system wywołań callback, ograniczanie stosowania
znaczników, obsługe emotikon, podparsowanie.

Moduł ten wymusi stosowanie znaczników zamykających BBCode w
odpowiedniej kolejności, oraz stosowanie znaczników kończących w celu
zapewnienia zgodności z HTML.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-1.0.2/* .
%undos -f c,h
%patch0 -p1
%patch1 -p0

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc CREDITS TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
