%define name sqliteodbc
%define version 0.61
%define release 1

Name: %{name}
Summary: ODBC driver for SQLite
Version: %{version}
Release: %{release}
Source: http://www.ch-werner.de/sqliteodbc/%{name}-%{version}.tar.gz
Group: System/Libraries
URL: http://www.ch-werner.de/sqliteodbc
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
ODBC driver for SQLite interfacing SQLite 2.x using unixODBC
or iODBC. See http://www.hwaci.com/sw/sqlite for a description of
SQLite, http://www.unixodbc.org for a description of unixODBC.

%prep
%setup -q

%build
CFLAGS="%optflags" ./configure --prefix=%{_prefix}
make

%install
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib
make install prefix=$RPM_BUILD_ROOT%{_prefix}
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/libsqliteodbc*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post
test -x /usr/bin/odbcinst && {
   INST=/tmp/sqliteinst$$
   cat > $INST << 'EOD'
[SQLITE]
Description=SQLite ODBC
Driver=%{_prefix}/lib/libsqliteodbc.so
Setup=%{_prefix}/lib/libsqliteodbc.so
FileUsage=1
EOD
   /usr/bin/odbcinst -i -d -n SQLITE -f $INST || true
   rm -f $INST
}

%preun
if [ $1 = 0 ] ; then
    test -x /usr/bin/odbcinst && {
	/usr/bin/odbcinst -u -d -n SQLITE || true
    }
fi

%files
%defattr(-, root, root)
%doc README license.terms ChangeLog
%{_libdir}/*.so*

