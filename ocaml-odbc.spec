%define		strange_version		%(echo %{version} | tr . _)

Summary:	ODBC binding for OCaml
Summary(pl):	Wi�zania ODBC dla OCamla
Name:		ocaml-odbc
Version:	2.6
Release:	1
License:	GPL/LGPL
Group:		Libraries
Vendor:		Maxence Guesdon <maxence.guesdon@inria.fr>
URL:		http://pauillac.inria.fr/~guesdon/Tools/ocamlodbc/ocamlodbc.html
Source0:	http://pauillac.inria.fr/~guesdon/Tools/Tars/ocamlodbc_%{strange_version}.tar.gz
# Source0-md5:	1375ce7bb9f34d4d516b335416914833
BuildRequires:	unixODBC-devel
BuildRequires:	ocaml >= 3.07
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCamlODBC is a library allowing to acces databases via an Open
DataBase Connectivity (ODBC) driver from OCaml programs. This package
contains files needed to run bytecode executables using OCamlODBC.

%description -l pl
OCamlODBC jest bibliotek� umo�liwiaj�ca dost�p do baz danych poprzez
sterownik Open DataBase Connectivity (ODBC) z program�w napisanych w
OCamlu. Pakiet ten zawiera binaria potrzebne do uruchamiania program�w
u�ywaj�cych OCamlODBC.

%package devel
Summary:	ODBC binding for OCaml - development part
Summary(pl):	Wi�zania ODBC dla OCamla - cze�� programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
OCamlODBC is a library allowing to acces databases via an Open
DataBase Connectivity (ODBC) driver from OCaml programs. This package
contains files needed to develop OCaml programs using OCamlODBC.

%description devel -l pl
OCamlODBC jest bibliotek� umo�liwiaj�ca dost�p do baz danych poprzez
sterownik Open DataBase Connectivity (ODBC) z program�w napisanych w
OCamlu. Pakiet ten zawiera pliki niezb�dne do tworzenia program�w
u�ywaj�cych OCamlODBC.

%prep
%setup -q -n ocamlodbc-%{version}

%build
# configure.in is not included, it dosn't matter much anyway
%configure2_13

# it is also possible to build psql, mysql and db2 drivers, but:
#   -- they cannot be compiled simultonetely
#   -- there are specialzed bindings for msql and psql
#   -- postgresql-odbc-devel conflicts with unixODBC-devel

%{__make} CC="%{__cc} %{rpmcflags} -fpic" unixodbc

# ok, I have my own opinion how to make libraries ;)
ocamlmklib -o ocamlodbc ocaml_odbc.cm[xo] ocamlodbc.cm[xo] \
	ocaml_odbc_c.o -lodbc

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{ocamlodbc,stublibs}
install *.cm[ixa]* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlodbc
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s ocamlodbc/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r Exemples Biniki $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# META for findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlodbc
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlodbc/META <<EOF
# Specifications for the "ocamlodbc" library:
requires = "unix"
version = "%{version}"
directory = "+ocamlodbc"
archive(byte) = "ocamlodbc.cma"
archive(native) = "ocamlodbc.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc *.mli LICENCE
%dir %{_libdir}/ocaml/ocamlodbc
%{_libdir}/ocaml/ocamlodbc/*.cm[ixa]*
%{_libdir}/ocaml/ocamlodbc/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/ocamlodbc
