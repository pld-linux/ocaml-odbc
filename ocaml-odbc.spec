%define		strange_version		%(echo %{version} | sed -e 's/\\./_/')

Summary:	ODBC binding for OCaml
Summary(pl):	Wi±zania ODBC dla OCamla
Name:		ocaml-odbc
Version:	2.5
Release:	1
License:	LGPL
Group:		Development/Libraries
Vendor:		Maxence Guesdon <maxence.guesdon@inria.fr>
URL:		http://pauillac.inria.fr/~guesdon/Tools/ocamlodbc/ocamlodbc.html
Source0:	http://pauillac.inria.fr/~guesdon/Tools/Tars/ocamlodbc_%{strange_version}.tar.gz
BuildRequires:	unixODBC-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCamlODBC is a library allowing to acces databases via an Open
DataBase Connectivity (ODBC) driver from OCaml programs. This package
contains files needed to run bytecode executables using OCamlODBC.

%description -l pl
OCamlODBC jest bibliotek± umo¿liwiaj±ca dostêp do baz danych poprzez
sterownik Open DataBase Connectivity (ODBC) z programów napisanych w
OCamlu. Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych LablGtk.

%package devel
Summary:	ODBC binding for OCaml - development part
Summary(pl):	Wi±zania ODBC dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
OCamlODBC is a library allowing to acces databases via an Open
DataBase Connectivity (ODBC) driver from OCaml programs. This package
contains files needed to develop OCaml programs using LablTk.

%description devel -l pl
OCamlODBC jest bibliotek± umo¿liwiaj±ca dostêp do baz danych poprzez
sterownik Open DataBase Connectivity (ODBC) z programów napisanych w
OCamlu. Pakiet ten zawiera pliki niezbêdne do tworzenia programów
u¿ywaj±cych LablTk.

%prep
%setup -q -n ocamlodbc-%{version}

%build
# configure.in is not included, it dosn't matter much anyway
%configure2_13

# it is also possible to build psql, mysql and db2 drivers, but:
#   -- they cannot be compiled simultonetely
#   -- there are specialzed bindings for msql and psql
#   -- postgresql-odbc-devel conflicts with unixODBC-devel

%{__make} unixodbc

# ok, I have my own opinion how to make libraries ;)
ocamlmklib -o ocamlodbc ocaml_odbc.cm[xo] ocamlodbc.cm[xo] \
	ocaml_odbc_c.o -lodbc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlodbc
install *.cm[ixa]* *.a dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlodbc
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlodbc && ln -s dll*.so ..)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r Exemples Biniki $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

gzip -9nf LICENCE *.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/ocamlodbc/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc *.gz
%dir %{_libdir}/ocaml/ocamlodbc
%{_libdir}/ocaml/ocamlodbc/*.cm[ixa]*
%{_libdir}/ocaml/ocamlodbc/*.a
%{_examplesdir}/%{name}-%{version}
